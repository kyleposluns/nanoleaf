import json


class AuroraException(Exception):

    def __init__(self, status, data):
        super().__init__()
        self.__status = status
        self.__data = data
        self.args = [status, data]

    @property
    def status(self):
        """
        The status returned by the Aurora API
        """
        return self.__status

    @property
    def data(self):
        """
        The (decoded) data returned by the Aurora API
        """
        return self.__data

    def __str__(self):
        return "{status} {data}".format(status=self.status, data=json.dumps(self.data))


class InternalServerError(AuroraException):
    """
    Error raised when there is something wrong with the aurora's server.
    """


class UnprocessableEntityException(AuroraException):
    """
    Exception raised in the case of an entity being unprocessable
    """


class ResourceNotFoundException(AuroraException):
    """
    Exception raised in case of not being able to find resources
    """


class BadRequestException(AuroraException):
    """
    Exception raised in case of bad request
    """


class InvalidCredentialsException(AuroraException):
    """
    Exception raised in case of bad credentials
    """
