import smtplib
import settings


class Emailer():
    def __init__(self):
        self.SMTP_SERVER = settings.SMTP_SERVER
        self.SMTP_PORT = int(settings.SMTP_PORT)
        self.SMTP_EMAIL = settings.SMTP_EMAIL
        self.SMTP_PASSWORD = settings.SMTP_PASSWORD
        self.USERNAME = settings.USERNAME
        self.PASSWORD = settings.PASSWORD

        self.auth = {'Authorization': self.__login()}

    def __login(self):
        _endpoint = 'http://gatherinfo-api:8080/login'

        return requests.post(_endpoint, json={"username": self.USERNAME, "password": self.PASSWORD}).json()['token']

    def retrieve_emails(self):
        _endpoint = 'http://gatherinfo-api:8080/users/emails'

        return requests.get(_endpoint, headers=self.auth).json()['emails']

    def retrieve_public_ips(self):
        _endpoint = 'http://gatherinfo-api:8080/assets/ips/public'

        return requests.get(_endpoint, headers=self.auth).json()['ips']

    def retrieve_devices(self):
        _endpoint = 'http://gatherinfo-api:8080/assets'

        return requests.get(_endpoint, headers=self.auth).json()['devices']

    def send_email(self, emails):
        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.SMTP_EMAIL, self.SMTP_PASSWORD)

            subject =  f'Here\'s your daily asset report...'
            body = ''

            msg = f'Subject: {subject}\n\n{body}'

            for email in emails:
                smtp.sendmail(self.SMTP_EMAIL, email, msg)

    def process(self):
