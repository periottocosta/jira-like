from rest_framework import serializers
from clients.serializer import ClientsSerializer
from jira_like.constants import GET_CLIENT_INFO_PARAM
from projects.models import Projects


class ProjectsSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "team_name",
            "client_id",
            "client_name",
        ]
        extra_kwargs = {
            "name": {"allow_blank": False, "required": True},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not self.context.get(GET_CLIENT_INFO_PARAM, False):
            ret.pop("client_name", None)
        return ret

    def get_client_name(self, obj):
        if (
            GET_CLIENT_INFO_PARAM in self.context
            and self.context[GET_CLIENT_INFO_PARAM]
        ):

            return ClientsSerializer(obj.client_id).data.get("name")

        return None
