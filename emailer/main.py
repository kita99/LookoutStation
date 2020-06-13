import settings
import template
import requests
import smtplib
from email.message import EmailMessage

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
        _endpoint = 'http://lookoutstation-api:8080/login'

        return requests.post(_endpoint, json={"username": self.USERNAME, "password": self.PASSWORD}).json()['token']

    def retrieve_emails(self):
        _endpoint = 'http://lookoutstation-api:8080/users/emails'

        return requests.get(_endpoint, headers=self.auth).json()['emails']

    def retrieve_devices(self):
        _endpoint = 'http://lookoutstation-api:8080/assets/devices'

        return requests.get(_endpoint, headers=self.auth).json()['devices']

    def retrieve_public_ips(self, device):
        _endpoint = f'http://lookoutstation-api:8080/assets/ips/public/{device}'

        return requests.get(_endpoint, headers=self.auth).json()['ip']

    def retrieve_software(self, device):
        _endpoint = f'http://lookoutstation-api:8080/assets/devices/{device}'

        return requests.get(_endpoint, headers=self.auth).json()['software']

    def send_email(self, emails, device, ip, software=None):
        for email in emails:
            msg = EmailMessage()
            msg['Subject'] = 'Here\'s your daily Report'
            msg['From'] = self.SMTP_EMAIL
            msg['To'] = email
            msg.add_alternative(template.html, subtype='html')

            with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT) as smtp:
                smtp.login(self.SMTP_EMAIL, self.SMTP_PASSWORD)
                smtp.send_message(msg)

    def process(self):
        _emails = self.retrieve_emails()
        _devices = self.retrieve_devices()

        data = []

        for device in _devices:
            if not device:
                continue

            ip = self.retrieve_public_ips(device)
            software = self.retrieve_software(device)

            # data.append({
            #     'device': device,
            #     'ip': ip,
            #     'software': software
            # })

            if not software:
                print('Sending email without software!!')
                self.send_email(_emails, device, ip)

            print("Sending email with software")
            self.send_email(_emails, device, ip, software)

email = Emailer()
email.process()
