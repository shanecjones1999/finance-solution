import json


class WebApiResponse:
    def __init__(self, status: int, message: str, data, error: str):
        self.status = status
        self.message = message
        self.data = data
        self.error = error

    def to_response(self):
        return json
