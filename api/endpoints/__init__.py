# import logging
from fastapi import FastAPI
from importlib import import_module

TAGS_METADATA: list[dict] = [  # for better documentation in openapi spec
    # Note: Add metadata as needed here
    # { "name": "<Capitalised Router name>", }
    {
        "name": "Health",
        "description": "Public endpoints for checking health of api server",
    },
    {
        "name": "User",
        "description": "Endpoints for Users of the application",
    },
    {
        "name": "News",
        "description": "Endpoint to fetch doping news",
    },
    {
        "name": "Chat",
        "description": "Endpoint for chatbot",
    
    },
    {
        "name": "Post",
        "description": "Endpoint for posts",
    },
    {
        "name": "Games",
        "description": "Endpoint for games",
    },
    {
        "name": "Upload",
        "description": "Endpoints for uploads",
    },
    {
        "name": "Image",
        "description": "Endpoint for image",
    },
    {
        "name": "Messages",
        "description": "Endpoint for messages",
    },
    {
        "name": "Comments",
        "description": "Endpoint for comments",
    },
]


def route_setup(app: FastAPI):
    """
    This method is used to set all the routers to the ASGI app
    To add new routes to the application,
    Add your file name (Capitalised without extension) in the TAGS_METADATA list
    """
    print("Setting up the routes ...")
    for tags in TAGS_METADATA:
        # TODO: logging.info(f"Setting up {tag_name} Route ...")
        tag_name: str = tags["name"]
        module = import_module(f".{tag_name.lower()}", "api.endpoints")
        route = getattr(module, f"{tag_name.lower()}_router")
        app.include_router(route, tags=[tag_name])
