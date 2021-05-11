from PyCursed.request import Request
from PyCursed.response import Response
from uuid import uuid4
from urllib.parse import parse_qs


class BaseMiddleWare:

    def to_request(self, request: Request):
        return

    def to_response(self, response: Response):
        return


class Session(BaseMiddleWare):

    def to_request(self, request: Request):
        cookie = request.environ.get('HTTP_COOKIE', None)
        if not cookie:
            return
        session_id = parse_qs(cookie)['session_id'][0]
        request.extra['session_id'] = session_id

    def to_response(self, response: Response):
        if not response.request.sessiion_id:
            response.update_headers(
                {'Set-Cookie': f'session_id{uuid4()}'}
            )


middlewares = [
    Session
]
