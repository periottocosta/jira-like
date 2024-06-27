from http import HTTPStatus
from rest_framework.test import APITestCase
from unittest.mock import patch

from tasks.models import Tasks


class TasksTestCase(APITestCase):
    def create_client(self):
        return self.client.post("/clients", data={"name": "John Doe"})

    def create_project(self):
        client_saved = self.create_client()
        client_id = client_saved.data.get("id")

        return self.client.post(
            "/projects", {"name": "Project 1", "client_id": client_id}
        )

    def sut(self):
        created_project = self.create_project()
        project_id = created_project.data.get("id")
        task_data = {
            "name": "Task 1",
            "project_id": project_id,
            "created_by": "user_test",
            "description": "Description 1",
            "assigned_to": "user_test",
        }
        return self.client.post("/tasks", data=task_data)

    def test_get_by_id(self):
        task_saved = self.sut()
        task_id = task_saved.data.get("id")

        response = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_by_id_not_found(self):
        response = self.client.get("/tasks/1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Task not found"})

    @patch("tasks.views.Tasks.objects.filter")
    def test_get_by_id_with_error(self, mock_all):
        mock_all.side_effect = Exception("GET Internal error")

        response = self.client.get("/tasks/invalid_id")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "GET Internal error"})

    def test_put(self):
        task_saved = self.sut()
        task_id = task_saved.data.get("id")
        project_id = task_saved.data.get("project_id")

        response = self.client.put(
            f"/tasks/{task_id}",
            data={
                "name": "Task 2",
                "project_id": project_id,
                "created_by": "user_test",
                "description": "Description 2",
                "assigned_to": "user_test",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        task = Tasks.objects.get(id=task_id)
        self.assertEqual(task.name, "Task 2")

    def test_put_not_found(self):
        response = self.client.put("/tasks/1", data={"name": "Task 2"})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Task not found"})

    @patch("tasks.views.Tasks.objects.filter")
    def test_put_with_error(self, mock_all):
        mock_all.side_effect = Exception("PUT Internal error")

        response = self.client.put("/tasks/invalid_id", data={"name": "Task 2"})
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "PUT Internal error"})

    def test_delete(self):
        task_saved = self.sut()
        task_id = task_saved.data.get("id")

        response = self.client.delete(f"/tasks/{task_id}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_delete_not_found(self):
        response = self.client.delete("/tasks/1")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json(), {"msg": "Task not found"})

    @patch("tasks.views.Tasks.objects.filter")
    def test_delete_with_error(self, mock_all):
        mock_all.side_effect = Exception("DELETE Internal error")

        response = self.client.delete("/tasks/invalid_id")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "DELETE Internal error"})

    def test_get_all(self):
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("tasks.views.Tasks.objects.all")
    def test_get_all_with_error(self, mock_all):
        mock_all.side_effect = Exception("GET Internal error")

        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "GET Internal error"})

    def test_get_all_by_project_id(self):
        task_saved = self.sut()
        project_id = task_saved.data.get("project_id")

        response = self.client.get(f"/tasks?project_id={project_id}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch("tasks.views.Tasks.objects.all")
    def test_get_all_by_project_id_with_error(self, mock_all):
        mock_all.side_effect = Exception("GET Internal error")

        response = self.client.get("/tasks?project_id=invalid_id")
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "GET Internal error"})

    def test_post(self):
        created_project = self.create_project()
        project_id = created_project.data.get("id")
        task_data = {
            "name": "Task 1",
            "project_id": project_id,
            "created_by": "user_test",
            "description": "Description 1",
            "assigned_to": "user_test",
        }
        response = self.client.post("/tasks", data=task_data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_post_with_empty_data(self):
        response = self.client.post("/tasks", data={})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "msg": {
                    "name": ["This field is required."],
                    "project_id": ["This field is required."],
                    "created_by": ["This field is required."],
                    "description": ["This field is required."],
                    "assigned_to": ["This field is required."],
                }
            },
        )

    @patch("tasks.views.TasksSerializer.is_valid")
    def test_post_with_exception(self, mock_is_valid):
        mock_is_valid.side_effect = Exception("POST Internal error")

        task_data = {
            "name": "Task 1",
            "project_id": 1,
            "created_by": "user_test",
            "description": "Description 1",
            "assigned_to": "user_test",
        }
        response = self.client.post("/tasks", data=task_data)

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"msg": "POST Internal error"})
