import requests
import json
from enum import Enum

def send_test_message():
    return requests.post(
        "https://api.mailgun.net/v3/icml.papro.org.uk/messages",
        auth=("api", "key-2a940124dc9ca22210d6278b6d0f12bd"),
        data={"from": "Mailgun Test <postmaster@icml.papro.org.uk>",
              "to": ["hptruong93@gmail.com"],
              "subject": "Hello HP Truong",
              "text": "Congratulations HP Truong, you just sent an email with Mailgun!  You are truly awesome!"})

# def send_email(dest, subject, text):
#     return requests.post(
#         "https://api.mailgun.net/v3/icml.papro.org.uk/messages",
#         auth=("api", "key-2a940124dc9ca22210d6278b6d0f12bd"),
#         data={"from": "ICML team <postmaster@icml.papro.org.uk>",
#               "to": "<{}>".format(dest),
#               "subject": subject,
#               "text": text})

class ApiClient:
    apiUri = 'https://api.elasticemail.com/v2'
    apiKey = '5c1961a9-965e-4298-b083-f5cdddd0a15d'

    def Request(method, url, data):
        data['apikey'] = ApiClient.apiKey
        if method == 'POST':
            result = requests.post(ApiClient.apiUri + url, params = data)
        elif method == 'PUT':
            result = requests.put(ApiClient.apiUri + url, params = data)
        elif method == 'GET':
            attach = ''
            for key in data:
                attach = attach + key + '=' + data[key] + '&'
            url = url + '?' + attach[:-1]
            result = requests.get(ApiClient.apiUri + url)

        jsonMy = result.json()

        if jsonMy['success'] is False:
            return jsonMy['error']

        return jsonMy['data']

def Send(subject, EEfrom, fromName, to, bodyText, isTransactional = True):
    return ApiClient.Request('POST', '/email/send', {
        'subject': subject,
        'from': EEfrom,
        'fromName': fromName,
        'to': to,
        'bodyText': bodyText,
        'isTransactional': isTransactional})

def send_email(dest, subject, text):
    return Send(subject,
                "postmaster@icml.papro.org.uk",
                "ICML 2017 Team",
                dest,
                text + "\n\n")
