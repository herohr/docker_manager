"""DockerManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from dm.docker_manager.views import container

container_urlpatterns = [
    path("container/create", container.ContainersCreateView.as_view()),
    path("container/list", container.ContainersListView.as_view()),
    path("container/get", container.ContainersGetView.as_view()),
    path("container/logs", container.ContainerLogsView.as_view()),
    path("container/pause", container.ContainerPauseView.as_view()),
    path("container/unpause", container.ContainerUnpauseView.as_view()),
    path("container/remove", container.ContainerRemoveView.as_view()),
    path("container/restart", container.ContainerRestartView.as_view()),
    path("container/rename", container.ContainerRenameView.as_view()),
    path("container/start", container.ContainerStartView.as_view()),
    path("container/stop", container.ContainerStopView.as_view()),
    path("container/top", container.ContainerTopView.as_view()),
]

urlpatterns = [
    path('admin/', admin.site.urls),

] + container_urlpatterns


