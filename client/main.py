import osquery
import json
import helpers
import requests
import logging

class Client():
    def __init__(self):
        self.instance = osquery.SpawnInstance()

        try:
            self.instance.open()
        except Exception as e:
            logging.error(e)

        self.uuid = self.__identifier()
        self.private_ip, self.public_ip = self.__fetch_network_info()
        self.kernel_version = self.__fetch_kernel_info()
        self.installed_packages = self.__fetch_installed_packages()

    def __identifier(self):
        uuid = self.instance.client.query('select uuid from system_info').response[0]['uuid']

        return uuid

    def __hostname(self):
        hostname = self.instance.client.query('select hostname from system_info').response[0]['hostname']

        return hostname

    def __fetch_network_info(self):
        private_ip = self.instance.client.query('select address from interface_addresses where interface = \'eth0\'').response[0]['address']
        public_ip = helpers.public_ip()

        return (private_ip, public_ip)

    def __fetch_kernel_info(self):
        kernel_version = self.instance.client.query('select version from kernel_info').response[0]['version']

        return kernel_version


    def __fetch_installed_packages(self):
        packages = self.instance.client.query('select name, version from deb_packages').response

        return packages


    def upsert_device(self):
        _endpoint = 'http://lookoutstation-api:8080/assets'

        insert_device = requests.post(_endpoint,
                                    json = {
                                        'uuid': self.uuid,
                                        'hostname': self.hostname
                                        'private_ip': self.private_ip,
                                        'public_ip': self.public_ip,
                                        'kernel_version': self.kernel_version
                                    }
        )

        if insert_device.status_code == 201:
            #logging.info(insert_software.text)
            print("Yay, created device.")
            return True

        elif insert_device.status_code == 200:
            #logging.error(insert_device.text)
            print('Oh no, device already exists. Ignoring...')
            return True

        elif insert_device.status_code == 500:
            #logging.error(insert_device.text)
            print(f'Something went wrong...No one likes exceptions!')
            return False

        return None

    def upsert_software(self):
        _endpoint = f'http://lookoutstation-api:8080/assets/{self.uuid}'

        insert_software = requests.put(_endpoint,
                                    json = {
                                        'software': self.installed_packages
                                    }
        )

        if insert_software.status_code == 200:
            #logging.info(insert_software.text)
            print("Yay, inserted software.")
            return True

        elif insert_software.status_code == 404:
            #logging.error(insert_software.text)
            print('No device found with this UUID.')
            return False

        elif insert_software.status_code == 400:
            #logging.error(insert_software.text)
            print('Invalid data passed.')
            return False

        elif insert_software.status_code == 500:
            breakpoint()
            #logging.error(insert_software.text)
            print('Something went wrong..No one likes exceptions!')
            return False


    def process(self):
        if not self.upsert_device():
            #logging.error('Something went wrong with creating the device...')
            print('Something went wrong with creating the device...')

        if not self.upsert_software():
            #logging.error('Something went wrong with inserting the software...')
            print('Something went wrong with inserting the software...')


client = Client()
client.process()