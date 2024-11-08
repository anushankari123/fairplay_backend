from fastapi import Request


def get_session(req: Request):
    yield req.state.session
