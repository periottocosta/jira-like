from rest_framework.test import APITestCase
from http import HTTPStatus
from projects.models import Projects
from unittest.mock import patch


class ProjectsTestCase(APITestCase):
    def create_client(self):
        return self.client.post("/clients", data={"name": "John Doe"})

    def sut(self):
        client_saved = self.create_client()
        client_id = client_saved.data.get("id")

        return self.client.post(
            "/projects", {"name": "Project 1", "client_id": client_id}
        )

    def test_get_by_id(self):
        project_saved = self.sut()
        project_id = project_saved.data.get("id")

        response = self.client.get(f"/projects/{project_id}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_by_id_not_found(self):
        response = self.client.get("/projects/1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Project not found"})

    @patch("projects.views.Projects.objects.filter")
    def test_get_by_id_with_error(self, mock_all):
        mock_all.side_effect = Exception("GET Internal error")

        response = self.client.get("/projects/invalid_id")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "GET Internal error"})

    def test_put(self):
        project_saved = self.sut()
        project_id = project_saved.data.get("id")
        client_id = project_saved.data.get("client_id")

        response = self.client.put(
            f"/projects/{project_id}",
            data={"name": "Project 2", "client_id": client_id},
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        project = Projects.objects.get(id=project_id)
        self.assertEqual(project.name, "Project 2")

    def test_put_not_found(self):
        response = self.client.put("/projects/1", data={"name": "Project 2"})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Project not found"})

    @patch("projects.views.Projects.objects.filter")
    def test_put_with_error(self, mock_all):
        mock_all.side_effect = Exception("PUT Internal error")

        response = self.client.put("/projects/invalid_id", data={"name": "Project 2"})
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "PUT Internal error"})

    def test_delete(self):
        project_saved = self.sut()
        project_id = project_saved.data.get("id")

        response = self.client.delete(f"/projects/{project_id}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_delete_not_found(self):
        response = self.client.delete("/projects/1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Project not found"})

    @patch("projects.views.Projects.objects.filter")
    def test_delete_with_error(self, mock_all):
        mock_all.side_effect = Exception("DELETE Internal error")

        response = self.client.delete("/projects/invalid_id")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "DELETE Internal error"})

    def test_get_all_projects(self):
        self.sut()

        response = self.client.get("/projects")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("projects.views.Projects.objects.all")
    def test_get_all_with_exception(self, mock_all):
        mock_all.side_effect = Exception("GET Internal error")

        response = self.client.get("/projects")

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "GET Internal error"})

    def test_post_project(self):
        client_saved = self.create_client()
        client_id = client_saved.data.get("id")

        response = self.client.post(
            "/projects", {"name": "Project 1", "client_id": client_id}
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_post_project_with_empty_data(self):
        response = self.client.post("/projects", data={})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "msg": {
                    "name": ["This field is required."],
                    "client_id": ["This field is required."],
                }
            },
        )

    @patch("projects.views.ProjectsSerializer.is_valid")
    def test_post_project_with_invalid_data(self, mock_is_valid):
        mock_is_valid.side_effect = Exception("Internal error")

        response = self.client.post("/projects", data={})
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "Internal error"})

    def test_get_project_details(self):
        project_saved = self.sut()
        project_id = project_saved.data.get("id")

        response = self.client.get(f"/projects/{project_id}/details")
        self.assertEqual(response.status_code, HTTPStatus.OK)
