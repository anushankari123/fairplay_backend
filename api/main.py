from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.db import initiate as init_db
from api.middleware import custom_middleware_setup
from api.endpoints import TAGS_METADATA, route_setup


async def lifespan(app: FastAPI):
    # On startup
    # TODO: Change print to logger
    route_setup(app)
    print("Route Setup Done")
    await init_db()
    print("DB Loaded")
    yield
    # On Shutdown


def create_api() -> FastAPI:
    # description for the openapi doc is set in Markdown language
    # Add more description if needed
    description = """
## BACKEND FOR DOPING
DOPING API provides access for users to \
manage doping information.

The API is intended to be used by both mobile and web frontend applications.
    """

    # TODO: Load env variables here.
    # set FastAPI app to be set to DEBUG mode if triggered locally

    app: FastAPI = FastAPI(  # TODO: Fix the name later
        title="BACKEND FOR DOPING",
        description=description,
        openapi_tags=TAGS_METADATA,
        lifespan=lifespan,
    )

    # TODO: Initialise Logger

    # TODO: Add global middleware to the Server here (if any) ...
    custom_middleware_setup(app)

    # Add CORS Middleware to the application
    # TODO: Analyse customer usage and limit the origin
    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    return app


app: FastAPI = create_api()
