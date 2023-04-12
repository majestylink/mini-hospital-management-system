from rest_framework.response import Response
from rest_framework import status


class ApiResponse:

    STATUS_MAPPING = {
        200: (True, None),
        201: (True, status.HTTP_201_CREATED),
        400: (False, status.HTTP_400_BAD_REQUEST),
        403: (False, status.HTTP_403_FORBIDDEN),
        404: (False, status.HTTP_404_NOT_FOUND)
    }

    def __init__(self, status_code=200, message=None, data=None):
        self.message = message
        self.data = data
        self.status_code = status_code

    def _fetch_status(self):
        return self.STATUS_MAPPING[self.status_code]

    def response(self):
        status, status_code = self._fetch_status()
        response_data = {"status": status, "message": None, "data": None}
        if self.message:
            response_data['message'] = self.message
        if self.data or self.data == []:
            response_data['data'] = self.data
        return Response(response_data, status_code)