from PyCursed.request import Request

class Response:

    def __init__(self, request: Request, status_code: int = 200, headers: dict = None, body: str = ''):
        self.status_code = status_code
        self.headers = {}
        self.body = b''
        self._set_base_headers()
        if headers is not None:
            self.headers.update(headers)
        self._set_body()
        self.request = Request
        self.extra = {}

    def __getattr__(self, item):
        return self.extra.get(item)

    def _set_base_headers(self):
        self.headers = {
            'Content-type': 'text/plain',
            'Content-length': 0
        }

    def _set_body(self, raw_body: str):
        self.body = raw_body.encode('utf-8')
        self.update_headers(
            {'Content-length': str(len(self.body))}
        )

    def update_headers(self, headers: dict):
        self.headers.update(headers)
