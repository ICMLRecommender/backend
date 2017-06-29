import requests

def send_test_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd0c8caef9e7c4fabbfddc3a36b7de13a.mailgun.org/messages",
        auth=("api", "key-2a940124dc9ca22210d6278b6d0f12bd"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd0c8caef9e7c4fabbfddc3a36b7de13a.mailgun.org>",
              "to": "HP Truong <hptruong93@gmail.com>",
              "subject": "Hello HP Truong",
              "text": "Congratulations HP Truong, you just sent an email with Mailgun!  You are truly awesome!"})



def send_email(dest, subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxd0c8caef9e7c4fabbfddc3a36b7de13a.mailgun.org/messages",
        auth=("api", "key-2a940124dc9ca22210d6278b6d0f12bd"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxd0c8caef9e7c4fabbfddc3a36b7de13a.mailgun.org>",
              "to": "<{}>".format(dest),
              "subject": subject,
              "text": text})

