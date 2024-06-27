from django.db import models

from jira_like.constants import TASK_STATUS_OPTIONS
from projects.models import Projects


# Create your models here.
class Tasks(models.Model):
    """Tasks Model."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=TASK_STATUS_OPTIONS, default="pending"
    )
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.CharField(max_length=255)

    class Meta:
        """Meta class."""

        ordering = ["created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
