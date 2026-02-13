from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import TaskForm, SignUpForm
from .models import Task


# Mixin: ensures every query only returns tasks for the logged-in user
class OwnerQuerySetMixin:
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


# -------------------------
# Dashboard
# -------------------------
class DashboardView(LoginRequiredMixin, OwnerQuerySetMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        today = timezone.now().date()

        active = qs.filter(is_archived=False)
        archived = qs.filter(is_archived=True)

        context["total_active"] = active.count()
        context["total_archived"] = archived.count()

        context["todo_count"] = active.filter(status=Task.Status.TODO).count()
        context["in_progress_count"] = active.filter(status=Task.Status.IN_PROGRESS).count()
        context["done_count"] = active.filter(status=Task.Status.DONE).count()
        context["blocked_count"] = active.filter(status=Task.Status.BLOCKED).count()

        # overdue: due_date < today and not DONE
        context["overdue_count"] = (
            active.filter(due_date__lt=today).exclude(status=Task.Status.DONE).count()
        )

        # due soon: due_date within next 7 days (and not DONE)
        context["due_soon"] = (
            active.filter(due_date__gte=today, due_date__lte=today + timezone.timedelta(days=7))
            .exclude(status=Task.Status.DONE)
            .order_by("due_date")[:5]
        )

        return context


# -------------------------
# Task List (active tasks)
# -------------------------
class TaskListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(is_archived=False)

        status = self.request.GET.get("status")
        q = self.request.GET.get("q")
        overdue = self.request.GET.get("overdue")

        if status:
            qs = qs.filter(status=status)

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        # due_date is DateField, so compare with today (date)
        if overdue == "1":
            today = timezone.now().date()
            qs = qs.filter(due_date__lt=today).exclude(status=Task.Status.DONE)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now().date()
        return context


# -------------------------
# Archived Tasks
# -------------------------
class ArchivedTaskListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Task
    template_name = "task_archived.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(is_archived=True)


# -------------------------
# Task Detail
# -------------------------
class TaskDetailView(LoginRequiredMixin, OwnerQuerySetMixin, DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"


# -------------------------
# Create Task
# -------------------------
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "task_form.html"
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.object.pk})


# -------------------------
# Update Task
# -------------------------
class TaskUpdateView(LoginRequiredMixin, OwnerQuerySetMixin, UpdateView):
    model = Task
    template_name = "task_form.html"
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.object.pk})


# -------------------------
# Archive Task (soft delete)
# -------------------------
class TaskArchiveView(LoginRequiredMixin, OwnerQuerySetMixin, View):
    def post(self, request, pk):
        task = self.get_queryset().get(pk=pk)
        task.is_archived = True
        task.save()
        return redirect("task_list")


# -------------------------
# Restore Archived Task
# -------------------------
class TaskRestoreView(LoginRequiredMixin, OwnerQuerySetMixin, View):
    def post(self, request, pk):
        task = self.get_queryset().get(pk=pk)
        task.is_archived = False
        task.save()
        return redirect("archived_tasks")


# -------------------------
# Toggle Done
# -------------------------
class TaskToggleDoneView(LoginRequiredMixin, OwnerQuerySetMixin, View):
    def post(self, request, pk):
        task = self.get_queryset().get(pk=pk)
        task.status = Task.Status.TODO if task.status == Task.Status.DONE else Task.Status.DONE
        task.save()
        return redirect("task_detail", pk=pk)


# -------------------------
# Sign Up
# -------------------------
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


# -------------------------
# Permanent Delete (only from archived page)
# -------------------------
class TaskDeletePermanentView(LoginRequiredMixin, OwnerQuerySetMixin, View):
    def post(self, request, pk):
        task = self.get_queryset().get(pk=pk)
        task.delete()
        return redirect("archived_tasks")
