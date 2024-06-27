"""
URL configuration for jira_like project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from clients.views import ClientItemView, ClientsListView
from projects.views import ProjectDetailsView, ProjectItemView, ProjectsListView
from tasks.views import TaskItemView, TasksListView

schema_view = get_schema_view(
    openapi.Info(
        title="JIRA API",
        default_version="v1",
        description="API to manage clients, projects and tasks",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("clients/<str:id>", ClientItemView.as_view()),
    path("clients", ClientsListView.as_view()),
    path("projects", ProjectsListView.as_view()),
    path("projects/<str:id>", ProjectItemView.as_view()),
    path("projects/<str:id>/details", ProjectDetailsView.as_view()),
    path("tasks", TasksListView.as_view()),
    path("tasks/<str:id>", TaskItemView.as_view()),
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
