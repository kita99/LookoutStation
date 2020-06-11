import smtplib
import settings
import requests
import json

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
        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.SMTP_EMAIL, self.SMTP_PASSWORD)

            subject = 'Here\'s your daily asset report...'
            body = f'Device do crl: {device}\nIp do crl: {ip}\nSoftware do crl: {software}'

            msg = f'Subject: {subject}\n\n{body}'

            for email in emails:
                smtp.sendmail(self.SMTP_EMAIL, email, msg)

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
            break
        #print(json.dumps(data, indent=4, sort_keys=True))

email = Emailer()
email.process()
