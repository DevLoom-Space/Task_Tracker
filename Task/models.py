from django.db import models
from django.conf import settings
from django.utils import timezone    



# Create your models here.

class Task(models.Model):

      #status choices
    class Status(models.TextChoices):
        TODO = 'TODO', 'To Do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'
        BLOCKED = 'BLOCKED', 'Blocked'

      #core fields
    title = models.CharField(max_length=200)

      #relationship to user
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    
    description = models.TextField(blank=True)

    
        #status field with choices
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )

        #Dates 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at', 'is_archived', '-updated_at']  #order tasks by creation date, newest first
        indexes = [
            models.Index(fields=['owner', 'is_archived', 'status']),  #index on status for faster filtering
            models.Index(fields=['owner']),   #index on owner for faster lookups
            models.Index(fields=['due_date']), #index on due date for sorting and filtering
        ]

    def save(self, *args, **kwargs):
        # If the task is marked as done and completed_at is not set, set it to now
        if self.status == self.Status.DONE and self.completed_at is None:
            self.completed_at = timezone.now()
        # If the task is not done, clear completed_at
        if self.status != self.Status.DONE and self.completed_at is not None:
            self.completed_at = None
            
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return self.title
