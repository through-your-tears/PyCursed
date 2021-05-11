from PyCursed.views import View
from PyCursed.request import Request
from PyCursed.response import Response
from PyCursed.template_engine import build_template

class Base(View):

    def get(self, request, *args, **kwargs):
        return Response(request=request, body='Hey, you successfully installed PyCursed framework')

class PostRequest(View):
    def get(self, request: Request, *args, **kwargs):
        body = build_template(request, {'name': 'idk'}, 'hello.html')
        return Response(request=request, body=body)

    def post(self, request: Request, *args, **kwargs):
        #переделать
        raw_name = request.POST.get('name_of_form_var')
        name = raw_name if raw_name else "None"
        body = build_template(request, {'name': name}, 'hello.html')
        return Response(request=request, body=body)
