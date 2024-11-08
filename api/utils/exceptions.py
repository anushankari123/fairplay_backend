from fastapi import status, HTTPException
from fastapi.responses import JSONResponse


class HTTPError(Exception):
    status_code: status
    detail: str

    def __init__(self):
        if not hasattr(self, "status_code"):
            raise NotImplementedError("Missing status_code")
        if not hasattr(self, "detail"):
            raise NotImplementedError("Missing detail")

    @property
    def full_error(self):
        error_names = []
        error = self.__class__
        while error.__name__ != "Exception":
            error_names.append(error.__name__)
            error = error.__bases__[0]
        return ".".join(reversed(error_names))

    @property
    def error_name(self):
        return self.__class__.__name__.lstrip("_")

    @property
    def json_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content={"exception_detail": self.full_error, "exception": self.error_name, "detail": self.detail},
        )


class NotFoundError(HTTPError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"

    def __init__(self, detail: str = None):
        self.detail = detail if detail else self.detail


class RequestError(HTTPError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str = None):
        self.detail = detail if detail else self.detail


class InvalidParameterError(RequestError):

    def __init__(self, parameter_name: str):
        self.detail = f"Invalid parameter: {parameter_name}"


class DuplicateConstraint(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = detail


class ServiceError(HTTPError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str = None):
        self.detail = detail if detail else self.detail


class RequestForbidden(HTTPError):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, detail: str):
        self.detail = detail


class ServiceException(HTTPError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail: str):
        self.detail = detail


class ServiceConfigurationError(ServiceError):
    def __init__(self, detail: str = None):
        self.detail = detail if detail else self.detail


class ACLError(HTTPError):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, detail: str = None):
        self.detail = detail if detail else self.detail


class ACLDenied(HTTPError):
    def __init__(self, resource: str = None):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "User not permitted to access this resource"
        if resource:
            self.detail += f" [resource={resource}]"


class ACLDeniedCRUD(HTTPError):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "User not permitted to perform this crud action"


class InvalidUserType(ACLError):
    detail = "Not a valid user type"


class InvalidUserPermissions(HTTPError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User not permitted to access this resource"


class _NoCredentialsError(HTTPError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal storage configuration error"


class UnauthorisedUser(ACLError):
    detail = "User not found"
