import functools
import json
import logging

from django.http import JsonResponse


class ApiView:
    def __init__(self, *args, **kwargs):
        pass

    def handler(self, request):
        logging.debug(request.body)
        if request.method.lower() in ("post", "put", "delete"):
            try:
                body_data = request.body.decode()
                if body_data:
                    json_data = json.loads(request.body.decode())
                    setattr(request, "json", json_data)

            except json.JSONDecodeError:
                logging.debug("Json parse error, request: {}".format(request))
                return self.json_decode_error(request)

        try:
            resp = getattr(self, request.method.lower())(request)
        except Exception as e:
            logging.exception("Server error: {}\nTraceback: {}".format(e, e.__traceback__))
            # raise e
            return ErrorResponse(500, "Server error, Exception: {}".format(e))

        if isinstance(resp, JsonResponse):
            return resp
        else:
            try:
                return Response(resp)
            except TypeError:
                logging.error("{} is not a Json Serializable object".format(resp))
                return ErrorResponse(500, "Server error, return type is not Json")
            # return ErrorResponse(500, "Unknown Error")

    def get(self, request):
        return self.method_not_allowed_error()

    def post(self, request):
        return self.method_not_allowed_error()

    def put(self, request):
        return self.method_not_allowed_error()

    def delete(self, request):
        return self.method_not_allowed_error()

    @staticmethod
    def method_not_allowed_error():
        return ErrorResponse(405, "Method not allowed")

    def json_decode_error(self, request, reason=""):
        return ErrorResponse(400, "Json decode error. {}".format(reason))

    @classmethod
    def as_view(cls, *args, **kwargs):
        ins = cls(*args, **kwargs)
        return lambda request: ins.handler(request)


class ErrorResponse(JsonResponse):
    def __init__(self, error_code, error_msg, error_entity=None, **kwargs):
        # if error_entity is not None:
        data = {
            "code": error_code,
            "msg": error_msg,
        }
        if error_entity is not None:
            data["error"] = error_entity

        super().__init__(data, status=error_code, **kwargs)


class Response(JsonResponse):
    def __init__(self, data, code=200, msg="OK", error_entity=None, **kwargs):
        data = {
            "data": data,
            "code": code,
            "msg": msg,
        }
        if error_entity is not None:
            data["error"] = error_entity

        super().__init__(data, **kwargs)


class FieldRequiredError(ErrorResponse):
    def __init__(self, field_name, **kwargs):
        super().__init__(402, "field {} must be give out".format(field_name), **kwargs)


class ApiViewMeta(type):
    def __new__(mcs, name, bases, attrs):
        handlers = {}
        if name == "AdapterViewMixin":
            return type.__new__(mcs, name, bases, attrs)
        for action, func in attrs.items():
            if action == "handlers":
                continue
            if action.startswith("__"):
                continue
            handlers[action] = func
        attrs["handlers"] = handlers
        return type.__new__(mcs, name, bases, attrs)


class AdapterViewMixin(metaclass=ApiViewMeta):
    def __init__(self, *args, **kwargs):
        super(AdapterViewMixin, self).__init__(*args, **kwargs)

    def post(self, request):
        action = request.json.get("action")
        handler = self.handlers.get(action)
        if handler is None:
            return ErrorResponse(404, "Action Not Found")
        else:
            return handler(self, request)
