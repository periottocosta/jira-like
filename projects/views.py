"""Projects views."""

from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from jira_like.constants import GET_CLIENT_INFO_PARAM
from projects.models import Projects
from projects.serializer import ProjectsSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from tasks.models import Tasks
from tasks.serializer import TasksSerializer


class ProjectItemView(APIView):
    """Project view."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProjectsSerializer(many=False),
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request: HttpRequest, id: str) -> Response:
        """Get project by ID"""
        try:

            project = Projects.objects.filter(id=id)
            if not project:
                return Response(
                    {"msg": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            get_client_info = (
                request.query_params.get(GET_CLIENT_INFO_PARAM, "false").lower()
                == "true"
            )
            serializer = ProjectsSerializer(
                project[0], many=False, context={GET_CLIENT_INFO_PARAM: get_client_info}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=ProjectsSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectsSerializer(many=False),
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def put(self, request: HttpRequest, id: str) -> Response:
        """Update project"""
        try:
            project = Projects.objects.filter(id=id)

            if not project:
                return Response(
                    {"msg": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            project_serializer = ProjectsSerializer(project[0], data=request.data)
            if project_serializer.is_valid():
                project_serializer.save()
                return Response(project_serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                data={"msg": project_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request: HttpRequest, id: str) -> Response:
        """Delete project"""
        try:
            project = Projects.objects.filter(id=id)

            if not project:
                return Response(
                    {"msg": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectsListView(APIView, PageNumberPagination):
    """Projects view."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProjectsSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request: HttpRequest) -> Response:
        """Get all projects"""
        try:

            get_client_info = (
                request.query_params.get(GET_CLIENT_INFO_PARAM, "false").lower()
                == "true"
            )

            projects = Projects.objects.all()
            results = self.paginate_queryset(projects, request, view=self)

            serializer = ProjectsSerializer(
                results, many=True, context={GET_CLIENT_INFO_PARAM: get_client_info}
            )

            return self.get_paginated_response(serializer.data)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=ProjectsSerializer,
        responses={
            status.HTTP_201_CREATED: ProjectsSerializer(many=False),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def post(self, request: HttpRequest) -> Response:
        """Create project"""
        try:
            project_serializer = ProjectsSerializer(data=request.data)

            if project_serializer.is_valid():
                project_serializer.save()
                return Response(project_serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                data={"msg": project_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectDetailsView(APIView, PageNumberPagination):
    """Projects view."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProjectsSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request: HttpRequest, id: str) -> Response:
        """Get project details"""
        try:

            project = Projects.objects.filter(id=id)
            if not project:
                return Response(
                    {"msg": "Project not found"}, status=status.HTTP_404_NOT_FOUND
                )

            tasks = Tasks.objects.filter(project_id=id)
            total_tasks = tasks.count()
            total_done_tasks = tasks.filter(status="done").count()

            serializer = ProjectsSerializer(
                project[0], many=False, context={GET_CLIENT_INFO_PARAM: True}
            )

            return Response(
                {
                    **serializer.data,
                    "total_tasks": total_tasks,
                    "total_done_tasks": total_done_tasks,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
