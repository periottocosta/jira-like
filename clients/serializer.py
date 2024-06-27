from rest_framework import serializers
from clients.models import Clients


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ["id", "name", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"allow_blank": False, "required": True},
        }
