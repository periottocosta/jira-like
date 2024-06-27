"""Tasks views module."""

from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from tasks.models import Tasks
from tasks.serializer import TasksSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class TaskItemView(APIView):
    """Task view."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TasksSerializer(many=False),
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request: HttpRequest, id: str) -> Response:
        """Get task by id"""
        try:

            task = Tasks.objects.filter(id=id)
            if not task:
                return Response(
                    {"msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = TasksSerializer(task[0])

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=TasksSerializer,
        responses={
            status.HTTP_201_CREATED: TasksSerializer(many=False),
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def put(self, request: HttpRequest, id: str) -> Response:
        """Update task"""
        try:
            task = Tasks.objects.filter(id=id)

            if not task:
                return Response(
                    {"msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND
                )

            task_serializer = TasksSerializer(task[0], data=request.data)
            if task_serializer.is_valid():
                task_serializer.save()
                return Response(task_serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                data={"msg": task_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request: HttpRequest, id: str) -> Response:
        """Delete task"""
        try:
            task = Tasks.objects.filter(id=id)

            if not task:
                return Response(
                    {"msg": "Task not found"}, status=status.HTTP_404_NOT_FOUND
                )

            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TasksListView(APIView, PageNumberPagination):
    """Tasks view."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TasksSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request: HttpRequest) -> Response:
        """Get all tasks"""
        try:
            tasks = Tasks.objects.all()

            project_id = request.query_params.get("project_id", None)
            if project_id:
                tasks = tasks.filter(project_id=project_id)

            results = self.paginate_queryset(tasks, request, view=self)
            serializer = TasksSerializer(results, many=True)

            return self.get_paginated_response(serializer.data)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=TasksSerializer,
        responses={
            status.HTTP_201_CREATED: TasksSerializer(many=False),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def post(self, request: HttpRequest) -> Response:
        """Create task"""

        try:
            task_serializer = TasksSerializer(data=request.data)

            if task_serializer.is_valid():
                task_serializer.save()
                return Response(task_serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                data={"msg": task_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
