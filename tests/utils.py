from starlette.datastructures import URLPath

from core import app


def reverse(route: str, **kwargs) -> URLPath:
    return app.url_path_for(route, **kwargs)
