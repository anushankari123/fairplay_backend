import uvicorn


def start():
    """
    Expand/Extend this method to work based on the environment
    """
    # add customisation as needed
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
