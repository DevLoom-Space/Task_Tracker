from django.urls import path
from . views import(
    DashboardView,
    TaskDeletePermanentView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskArchiveView,
    ArchivedTaskListView,
    TaskRestoreView,
    TaskToggleDoneView,
    DashboardView
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('archived/', ArchivedTaskListView.as_view(), name='archived_tasks'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('<int:pk>/archive/', TaskArchiveView.as_view(), name='task_archive'),
    path('<int:pk>/restore/', TaskRestoreView.as_view(), name='task_restore'),
    path('<int:pk>/delete-permanent/', TaskDeletePermanentView.as_view(), name='task_delete'),
    path('<int:pk>/toggle-done/', TaskToggleDoneView.as_view(), name='task_toggle_done'),
]

