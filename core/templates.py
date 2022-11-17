from copy import deepcopy
from re import findall
from core.exceptions import TemplateOptionsError

class Template(object):
    def __init__(self, template: str = "Hello %victim%") -> None:
        self.base = template
        self.settings = findall(r'%(.*?)%', template)
        

class TemplateEngine(object):
    def __init__(self) -> None:
        self.template = Template()

    def set_template(self, template: Template) -> None:
        self.template = template

    def gen_email(self, options: dict) -> str:
        result = deepcopy(self.template.base)

        for key in self.template.settings:
            try:
                result.replace(
                    '%' + key + '%',
                    options[key]
                )
            except KeyError:
                # Detect not configured options
                raise TemplateOptionsError
        return result
