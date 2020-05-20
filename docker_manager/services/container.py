from docker.models.containers import Container


class Containers:
    def __init__(self, _client):
        self.c = _client or client

    def list(self):
        return [Containers.container_serialize(i) for i in self.c.containers.list()]

    def run(self, image_name: str, command=None):
        return self.c.containers.run(image_name, command)

    def create(self, image_name: str, command=None, name=None):
        r = self.c.containers.create(image_name, command, name=name)
        return self.container_serialize(r)

    def get(self, name_or_id):
        r = self.c.containers.get(name_or_id)
        return self.container_serialize(r)

    def logs(self, name_or_id, *args, **kwargs):
        c = self.get_container_obj(name_or_id)
        return c.logs().decode()

    def pause(self, name_or_id, *args, **kwargs):
        c = self.get_container_obj(name_or_id)
        return c.pause()

    def unpause(self, name_or_id, *args, **kwargs):
        c = self.get_container_obj(name_or_id)
        return c.unpause()

    def remove(self, name_or_id):
        c = self.get_container_obj(name_or_id)
        c.remove()
        return

    def rename(self, name_or_id, new_name):
        c = self.get_container_obj(name_or_id)
        c.rename(new_name)
        return

    def restart(self, name_or_id):
        c = self.get_container_obj(name_or_id)
        c.restart()
        return

    def start(self, name_or_id):
        c = self.get_container_obj(name_or_id)
        c.start()
        return

    def stop(self, name_or_id):
        c = self.get_container_obj(name_or_id)
        c.stop()
        return

    def top(self, name_or_id):
        c = self.get_container_obj(name_or_id)
        r = c.top()
        return r


    @staticmethod
    def container_serialize(container: Container):
        return container.attrs

    def get_container_obj(self, name_or_id):
        return self.c.containers.get(name_or_id)


if __name__ == "__main__":
    from dm.docker_manager.services.client import client

    containers = Containers(client)
    _c = containers.get_container_obj('yapi')