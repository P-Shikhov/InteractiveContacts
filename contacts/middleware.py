from threading import current_thread

_requests = {}


class RequestNotFound(Exception):
    def __init__(self, message):
        self.message = message


def get_request():
    thread = current_thread()
    if thread not in _requests:
        raise RequestNotFound('Request error.')
    return _requests[thread]

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        _requests[current_thread()] = request

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response
