import requests

def public_ip():
    ip = requests.get('https://api.ipify.org').text
    return ip
