from threading import Thread
from time import sleep

from core.connection import SMTPConnection
from core.templates import Template, TemplateEngine

class Sender(Thread):
    def __init__(self, server: SMTPConnection, timeout: int = 1) -> None:
        super().__init__()
        self.server = server
        self.timeout = timeout
        self.generator = TemplateEngine()

    def set_template(self, template: Template) -> None:
        self.generator.set_template(template)

    def stop(self):
        self.alive = False
        del self.server

    def start(self):
        self.alive = True
        super().start()

class Spammer(Sender):
    def __init__(self, server: SMTPConnection, victims: list, timeout: int = 1) -> None:
        super().__init__(server, timeout)
        self.victims = victims
        self.start()
    
    def run(self) -> None:
        while self.alive:
            try:
                victim = self.victims.pop()
            except:
                break
            email = self.generator.gen_email(victim)
            self.server.sendmail(victim, email)
            sleep(self.timeout)
    
    def sends_left(self) -> int:
        return len(self.victims)

    def stop(self):
        super().stop()
        del self.victims

