from http import HTTPStatus
from rest_framework.test import APITestCase
from clients.models import Clients
from clients.serializer import ClientsSerializer
from unittest.mock import patch


class ClientsTestCase(APITestCase):
    def create_client(self):
        return self.client.post("/clients", data={"name": "John Doe"})

    def test_get_by_id(self):
        client_saved = self.create_client()
        client_id = client_saved.data.get("id")

        response = self.client.get(f"/clients/{client_id}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_by_id_not_found(self):
        response = self.client.get("/clients/1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Client not found"})

    @patch("clients.views.Clients.objects.filter")
    def test_get_by_id_with_error(self, mock_all):
        mock_all.side_effect = Exception("GET Internal error")

        response = self.client.get("/clients/invalid_id")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "GET Internal error"})

    def test_put(self):
        client_saved = self.create_client()
        client_id = client_saved.data.get("id")

        response = self.client.put(f"/clients/{client_id}", data={"name": "Jane Doe"})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        client = Clients.objects.get(id=client_id)
        self.assertEqual(client.name, "Jane Doe")

    def test_put_not_found(self):
        response = self.client.put("/clients/1", data={"name": "Jane Doe"})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Client not found"})

    @patch("clients.views.Clients.objects.filter")
    def test_put_with_error(self, mock_all):
        mock_all.side_effect = Exception("PUT Internal error")

        response = self.client.put("/clients/invalid_id", data={"name": "Jane Doe"})
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "PUT Internal error"})

    def test_delete(self):
        client_saved = self.create_client()
        client_id = client_saved.data.get("id")

        response = self.client.delete(f"/clients/{client_id}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_delete_not_found(self):
        response = self.client.delete("/clients/1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Client not found"})

    @patch("clients.views.Clients.objects.filter")
    def test_delete_with_error(self, mock_all):
        mock_all.side_effect = Exception("DELETE Internal error")

        response = self.client.delete("/clients/invalid_id")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "DELETE Internal error"})

    def test_get_all_clients(self):
        response = self.client.get("/clients")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("clients.views.Clients.objects.all")
    def test_get_with_exception(self, mock_all):
        mock_all.side_effect = Exception("GET Internal error")

        response = self.client.get("/clients")

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "GET Internal error"})

    def test_post(self):
        client_data = {"name": "John Doe"}
        response = self.client.post("/clients", data=client_data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(Clients.objects.filter(name="John Doe").exists())

        client = Clients.objects.get(name="John Doe")
        serializer = ClientsSerializer(client)
        self.assertEqual(response.data, serializer.data)

    def test_post_with_empty_data(self):
        response = self.client.post("/clients", data={})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.json(), {"msg": {"name": ["This field is required."]}}
        )

    @patch("clients.views.ClientsSerializer.is_valid")
    def test_post_with_exception(self, mock_is_valid):
        mock_is_valid.side_effect = Exception("POST Internal error")

        client_data = {"name": "John Doe"}
        response = self.client.post("/clients", data=client_data)

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "POST Internal error"})
