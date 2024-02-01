from core import app


def reverse(route: str, **kwargs):
    return app.url_path_for(route, **kwargs)
