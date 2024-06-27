from django.db import models

from clients.models import Clients


# Create your models here.
class Projects(models.Model):
    """Projects Model."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    team_name = models.CharField(max_length=255, default="PERIOTTO-TEAM")

    class Meta:
        """Meta class."""

        ordering = ["created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
