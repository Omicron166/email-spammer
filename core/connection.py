import smtplib

class SMTPConnection(smtplib.SMTP):
    def login(self, user: str, password: str, *, initial_response_ok: bool = ...) -> smtplib._Reply:
        self.email = user
        return super().login(user, password, initial_response_ok=initial_response_ok)

    def sendmail(self, to_addrs: str | smtplib.Sequence[str], msg: bytes | str, mail_options: smtplib.Sequence[str] = ..., rcpt_options: smtplib.Sequence[str] = ...) -> smtplib._SendErrs:
        return super().sendmail(self.user, to_addrs, msg, mail_options, rcpt_options)