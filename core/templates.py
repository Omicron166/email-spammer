from copy import deepcopy

class Template(object):
    def __init__(self, template: str = "Hello %victim%", settings: dict = {}) -> None:
        self.base = template
        self.settings = settings
        

class TemplateEngine(object):
    def __init__(self) -> None:
        self.template = Template()

    def set_template(self, template: Template) -> None:
        self.template = template

    def gen_email(self, email: str) -> str:
        result = deepcopy(self.template.base)
        result.replace(
            '%victim%',
            email.split('@')[0]
        )

        for key in self.template.settings.keys():
            result.replace(
                '%' + key + '%',
                self.template.settings[key]
            )
        return result
