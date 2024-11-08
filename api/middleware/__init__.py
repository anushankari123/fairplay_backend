"""
Usually, the middlewares are setup in 3 ways
1. Starlette style - Class Based middleware with Dispatch function
`app.add_middleware(CustomMiddlewareClass)`
2. FastAPI style - Decorator over a function or a callable obj
`app.middleware('http')(callable_middleware)`
3. Starlette style - Middleware dispatch function alone
`app.add_middleware(BaseHTTPMiddleware, dispatch=middleware_fn)`

And as we also want to use the power of Class based object programming,
we will be using the 2nd soln the FastAPI style setup
"""

from typing import Callable, List
from fastapi import FastAPI

from .handler_middleware import HandlerMiddleware


def custom_middleware_setup(app: FastAPI):
    """
    This method is used to set middleware to the app

    To add new middleware to the app,
    import the necessary custom middleware and
    add it to the `middleware_stack`.

    PS: Please note the position of middleware in the stack matters
    as it would affect the internal working
    """
    middleware_stack: List[Callable] = [
        # When you add a new middleware to the list,
        # please remember that it will be added to stack as given order.
        # example: MyCustomMiddlewareClass()
        HandlerMiddleware(),
    ]
    # TODO: logging.info("Setting up Custom Middlewares ...")
    for middleware in middleware_stack:
        app.middleware("http")(middleware)
