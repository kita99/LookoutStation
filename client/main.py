import osquery
import json
import helpers

class Client():
    def __init__(self):
        self.instance = osquery.SpawnInstance()

        try:
            self.instance.open()
        except Exception as e:
            logging.error(e)

        self.uuid = self.instance.client.query("select uuid from system_info")


    def fetch_network_info(self):
        self.hostname = self.instance.client.query("select hostname from system_info")
        self.private_ip = self.instance.client.query("select address from arp_cache")
        self.public_ip = helpers.public_ip()


    def fetch_kernel_info(self):
        self.kernel_version = self.instance.client.query("select version from kernel_info")


    def fetch_installed_packages(self):
        self.pkg_name = self.instance.client.query("select name from deb_packages")
        self.pkg_version = self.instance.client.query("select version from deb_packages")


