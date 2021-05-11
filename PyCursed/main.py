from typing import List, Type
from urls import Url
import re
from exceptions import NotFound, NotAllowed
from views import View
from requests import Request
from PyCursed.response import Response
from PyCursed.miiddleware import BaseMiddleWare

class PyCursed:

    __slots__ = ('url', 'settings', 'middlewares')

    def __init__(self, urls: List[Url], settings: dict, middlewares: List[Type[BaseMiddleWare]]):
        self.urls = urls
        self.settings = settings
        self.middlewares = middlewares

    def __call__(self, environ: dict, start_response):
        view = self._get_view(environ)
        request = self._get_request(environ)
        self._apply_middleware_to_request(request)
        response = self._get_response(environ, view, request)
        self._apply_middleware_to_response(response)
        start_response(str(response.status_code), response.headers.items())
        return iter([response.body])

    def _prepare_url(self, url: str):
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        url = self._prepare_url(raw_url)
        for path in self.urls:
            if re.match(path.url, url) is not None:
                return path.view
        raise NotFound

    def _get_view(self, environ) -> View:
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)
        return view

    def _get_request(self, environ: dict):
        return Request(environ)

    def _get_response(self, environ: dict, view: View, request: Request) -> Response:
        method = environ['REQUEST_METHOD'].lower()
        if not hasattr(view, method):
            raise NotAllowed
        return getattr(view, method)(request)

    def _apply_middleware_to_request(self, request: Request):
        for middleware in self.middlewares:
            middleware.to_request(request)

    def _apply_middleware_to_response(self, response: Response):
        for middleware in self.middlewares:
            middleware.to_response(response)
