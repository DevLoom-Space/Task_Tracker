from django.contrib import admin
from .models import Task

  #model admin for Task with list display, filters, and search
class TaskAdmin(admin.ModelAdmin):
    #fields/ columns to display in admin list view
    list_display = ('title', 'owner', 'status', 'created_at', 'due_date')

    #Sidebar filters for quick filtering by status, creation date, and due date
    # You can click on these filters to quickly narrow down the list of tasks based on their status or when they were created/due.
    list_filter = ('status', 'created_at', 'due_date')

    #Search box to search tasks by title, description, or owner's username 
    search_fields = ('title', 'description')

    ordering = ('is_archived', '-updated_at')  #order tasks by archived status and then by last updated date

    autocomplete_fields = ('owner',)  #enable autocomplete for owner field to quickly find users when assigning tasks


admin.site.register(Task, TaskAdmin)
