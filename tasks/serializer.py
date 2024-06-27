from rest_framework import serializers
from tasks.models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            "id",
            "name",
            "status",
            "project_id",
            "created_at",
            "updated_at",
            "created_by",
            "description",
            "assigned_to",
        ]
        extra_kwargs = {
            "name": {"allow_blank": False, "required": True},
            "project_id": {"required": True},
            "description": {"allow_blank": False, "required": True},
            "created_by": {"allow_blank": False, "required": True},
        }
