from rest_framework import exceptions, status


class DifferentPasswordsException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'your password and entered password are different'

