from core import app


def url_for(route: str, **kwargs):
    return app.url_path_for(route, **kwargs)
