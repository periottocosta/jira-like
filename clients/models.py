"""Clients Model Module."""

from django.db import models


class Clients(models.Model):
    """Clients Model."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""

        ordering = ["created_at"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"
