import os
import re

from PyCursed.request import Request

HTML_FOR = re.compile(r'{% for (?P<variable>[a-zA-z]+) in (?P<seq>[a-z][A-Z]+) %}(?P<content>[\s][\S]+)(?={% endblock %}){% endblock %}')
HTML_VAR = re.compile(r' {{')
HTML_IF = re.compile(r' if (?P<variable>[a-z][A-Z]+) %}(?P<content>[\s][\S]+)(?={% endblock %}){% endblock %}')


class Engine:

    def __init__(self, base_dir, template_dir):
        self.template_dir = os.path.join(base_dir, template_dir)

    def _get_template_as_string(self, template_name):
        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.isfile(template_path):
            raise Exception(f'{template_path} is not file')
        with open(template_path) as file:
            return file.read()

    def _build_block(self, context: dict, raw_template_block: str) -> str:
        used_vars = HTML_VAR.findall(raw_template_block)
        if used_vars is None:
            return raw_template_block

        for var in used_vars:
            var_in_template = '{{ %s }}' % var
            raw_template_block = re.sub(var_in_template, str(context.get(var, '')), raw_template_block)
        return raw_template_block

    def _build_for_block(self, context: dict, raw_template: str):
        for_block = HTML_FOR.search(raw_template)
        if for_block is None:
            return raw_template
        build_for_block = ''
        for var in context.get(for_block.group('seq'), []):
            build_for_block += self._build_block(
                {**context, for_block.group('variable'): var},
                for_block.group('content')
            )
        return HTML_FOR.sub(build_for_block, raw_template)

    def _build_if_block(self, context: dict, raw_template: str):
        pass

    def buld(self, context: dict, template_name: str) -> str:
        raw_template = self._get_template_as_string(template_name)
        raw_template = self._build_for_block(context, raw_template)
        raw_template = self._build_if_block(context, raw_template)
        return self._build_block(context, raw_template)

def build_template(request: Request, context: dict, template_name: str):
    assert request.settings.get('BASE_DIR')
    assert request.settings.get('TEMPLATE_DIR_NAME')

    engine = Engine(
        request.settings.get('BASE_DIR'),
        request.settings.get('TEMPLATE_DIR_NAME')
    )
    return engine.buld(context, template_name)
