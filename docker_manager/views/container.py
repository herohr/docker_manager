from dm.docker_manager.services.container import Containers
from dm.docker_manager.views.view import ApiView, AdapterViewMixin
from dm.docker_manager.services.client import client


class ContainersView(ApiView):
    containers = Containers(client)


class ContainersListView(ContainersView):
    def post(self, request):
        return self.containers.list()


class ContainersCreateView(ContainersView):
    def post(self, request):
        data = {
            "image_name": request.json.get("image_name"),
            "command": request.json.get("command"),
            "name": request.json.get("name")
        }

        return self.containers.create(**data)


class ContainersGetView(ContainersView):
    def post(self, request):
        name = request.json.get("name")
        _id = request.json.get("id")

        return self.containers.get(name or _id)


class ContainerView(ApiView):
    containers = Containers(client)

    def get_id(self, request):
        name = request.json.get("name")
        _id = request.json.get("id")
        return name or _id


class ContainerLogsView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.logs(_id)


class ContainerPauseView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.pause(_id)


class ContainerUnpauseView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.unpause(_id)


class ContainerRemoveView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.remove(_id)


class ContainerRestartView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.restart(_id)


class ContainerRenameView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        new_name = request.json.get("new_name")
        return self.containers.rename(_id, new_name)


class ContainerStartView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.start(_id)


class ContainerStopView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.stop(_id)


class ContainerTopView(ContainerView):
    def post(self, request):
        _id = self.get_id(request)
        return self.containers.top(_id)
