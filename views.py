from PyCursed.views import View

class Base(View):

    def get(self, request, *args, **kwargs):
        return 'Hey, you succesfully installed PyCursed framework'