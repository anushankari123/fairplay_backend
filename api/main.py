from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv  # Import dotenv
import os  # Import os to access environment variables

from api.db import initiate as init_db
from api.middleware import custom_middleware_setup
from api.endpoints import TAGS_METADATA, route_setup


# Load environment variables from .env file
load_dotenv()

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
DOPING API provides access for users to manage doping information.

The API is intended to be used by both mobile and web frontend applications.
    """

    # Load the environment variables
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Debug log to check if the environment variables are loaded
    print(f"GOOGLE_CLIENT_ID: {GOOGLE_CLIENT_ID}")
    print(f"GOOGLE_CLIENT_SECRET: {GOOGLE_CLIENT_SECRET}")
    print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}")

    # Set FastAPI app to be set to DEBUG mode if triggered locally
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


# Create and run the app
app: FastAPI = create_api()
