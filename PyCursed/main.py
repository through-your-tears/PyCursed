from typing import List, Type
from urls import Url
import re
from exceptions import NotFound, NotAllowed
from views import View


class PyCursed:

    __slots__ = ('url',)

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def __call__(self, environ, start_response):
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)
        method = environ['REQUEST_METHOD'].lower()
        if not hasattr(view, method):
            raise NotAllowed
        raw_response = getattr(view, method)(None)
        
        data = b'Hello, world'
        start_response(
            '200 OK',
            ('Content-type', 'text/plain'),
            ('Content-length', len(str(data)))
        )
        return iter([data])

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
