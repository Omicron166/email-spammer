from threading import Thread
from time import sleep

from core.connection import SMTPConnection
from core.templates import Template, TemplateEngine
from core.exceptions import TemplateOptionsError

class Sender(Thread):
    def __init__(self, server: SMTPConnection, options: dict, timeout: int = 1) -> None:
        super().__init__()
        self.server = server
        self.timeout = timeout
        self.generator = TemplateEngine()
        self.options = options

    def set_template(self, template: Template) -> None:
        self.generator.set_template(template)

    def stop(self):
        self.alive = False
        del self.server

    def start(self):
        self.alive = True
        super().start()

class Spammer(Sender):
    def __init__(self, server: SMTPConnection, victims: list[str], options: dict, timeout: int = 1) -> None:
        super().__init__(server, options, timeout)
        self.victims = victims
        self.start()
    
    def run(self) -> None:
        #####################################
        # Temporal workaround, replace with
        # native template engine check
        #####################################
        self.options['victim'] = 'dummy'
        self.options['email'] = 'dummy@somewhere.com'
        try:
            self.generator.gen_email(self.options)
        except TemplateOptionsError:
            self.stop()
            return
        #####################################

        while self.alive:
            try:
                victim = self.victims.pop()
            except:
                break
            self.options['victim'] = victim.split('@')[0]
            self.options['email'] = victim
            email = self.generator.gen_email(self.options)
            self.server.sendmail(victim, email)
            sleep(self.timeout)
    
    def sends_left(self) -> int:
        return len(self.victims)

    def stop(self):
        super().stop()
        del self.victims

class Bomber(Sender):
    def __init__(self, server: SMTPConnection, victim: str, options: dict, sends: int, timeout: int = 1) -> None:
        super().__init__(server, options, timeout)
        self.victim = victim
        self.sends = sends
        self.start()
    
    def run(self) -> None:
        #####################################
        # Temporal workaround, replace with
        # native template engine check
        #####################################
        self.options['victim'] = 'dummy'
        self.options['email'] = 'dummy@somewhere.com'
        try:
            self.generator.gen_email(self.options)
        except TemplateOptionsError:
            self.stop()
            return
        #####################################

        self.options['victim'] = self.victim.split('@')[0]
        self.options['email'] = self.victim

        email = self.generator.gen_email(self.options)
        while self.alive and self.sends > 0:
            try:
                self.server.sendmail(self.victim, email)
            except:
                break
            self.sends -= 1
            sleep(self.timeout)

    def sends_left(self) -> int:
        return self.sends

    def stop(self):
        super().stop()
        del self.victim
