"""Clients views module."""

from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from clients.models import Clients
from clients.serializer import ClientsSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class ClientItemView(APIView):
    """Client view."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ClientsSerializer(many=False),
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request: HttpRequest, id: str) -> Response:
        """Get client by id"""
        try:

            client = Clients.objects.filter(id=id)
            if not client:
                return Response(
                    {"msg": "Client not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = ClientsSerializer(client[0])

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=ClientsSerializer,
        responses={
            status.HTTP_201_CREATED: ClientsSerializer(many=False),
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def put(self, request: HttpRequest, id: str) -> Response:
        """Update client"""
        try:
            client = Clients.objects.filter(id=id)

            if not client:
                return Response(
                    {"msg": "Client not found"}, status=status.HTTP_404_NOT_FOUND
                )

            client_serializer = ClientsSerializer(client[0], data=request.data)
            if client_serializer.is_valid():
                client_serializer.save()
                return Response(client_serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                data={"msg": client_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request: HttpRequest, id: str) -> Response:
        """Delete client"""
        try:
            client = Clients.objects.filter(id=id)

            if not client:
                return Response(
                    {"msg": "Client not found"}, status=status.HTTP_404_NOT_FOUND
                )

            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClientsListView(APIView, PageNumberPagination):
    """Clients view."""

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ClientsSerializer(many=True),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def get(self, request: HttpRequest) -> Response:
        """Get all clients."""
        try:
            clients = Clients.objects.all()

            results = self.paginate_queryset(clients, request, view=self)
            serializer = ClientsSerializer(results, many=True)

            return self.get_paginated_response(serializer.data)
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        request_body=ClientsSerializer,
        responses={
            status.HTTP_201_CREATED: ClientsSerializer(many=False),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        },
    )
    def post(self, request: HttpRequest) -> Response:
        """Save client."""

        try:
            client_serializer = ClientsSerializer(data=request.data)

            if client_serializer.is_valid():
                client_serializer.save()
                return Response(client_serializer.data, status=status.HTTP_201_CREATED)

            return Response(
                data={"msg": client_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"msg": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
