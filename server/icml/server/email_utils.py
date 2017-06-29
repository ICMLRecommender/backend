import requests

def send_test_message():
    return requests.post(
        "https://api.mailgun.net/v3/icml.papro.org.uk/messages",
        auth=("api", "key-2a940124dc9ca22210d6278b6d0f12bd"),
        data={"from": "Mailgun Test <postmaster@icml.papro.org.uk>",
              "to": ["hptruong93@gmail.com"],
              "subject": "Hello HP Truong",
              "text": "Congratulations HP Truong, you just sent an email with Mailgun!  You are truly awesome!"})

def send_email(dest, subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/icml.papro.org.uk/messages",
        auth=("api", "key-2a940124dc9ca22210d6278b6d0f12bd"),
        data={"from": "ICML team <postmaster@icml.papro.org.uk>",
              "to": "<{}>".format(dest),
              "subject": subject,
              "text": text})
