import requests
import json
import sys
import argparse

HOST_PREFIX = "http://127.0.0.1:8000"
AUTH_PREFIX = "{0}/rest-auth".format(HOST_PREFIX)
ICML_PREFIX = "{0}/icml".format(HOST_PREFIX)

def is_success(r): # Only check for status code for now
    if r.status_code != 200:
        print r.__dict__
        return False

    return True


def check_registration(session):
    url = '{0}/registration/'.format(AUTH_PREFIX)
    data = {
                'username' : 'hptruong',
                'password1' : 'supersecret',
                'password2' : 'supersecret',
                'email' : 'hptruong93@gmail.com'
            }
    r = session.post(url, data = data)

    if not is_success(r):
        return False

    print "Success"
    print r.json()

    return True

def check_login(session):
    url = '{0}/login/'.format(AUTH_PREFIX)
    data = {
                'username' : 'hptruong',
                'password' : 'supersecret',
                'email' : 'hptruong93@gmail.com'
            }

    r = session.post(url, data = data)

    if not is_success(r):
        return False

    return r

def check_logout(session, csrf_token):
    url = '{0}/logout/'.format(AUTH_PREFIX)
    data = { 'csrfmiddlewaretoken' : csrf_token }
    r = session.post(url, data = data)

    if not is_success(r):
        return False

    print "Logout"
    return r.json()

def check_index_page(session, csrf_token):
    url = '{0}/'.format(ICML_PREFIX)

    r = session.get(url)
    if not is_success(r):
        return False
    print r.json()

    data = { 'csrfmiddlewaretoken' : csrf_token }
    r = session.post(url, data = data)

    if not is_success(r):
        return False
    print r.json()

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Django test client')
    parser.add_argument('-f', type = int, nargs = '+', dest='actions', required = True, default = [0], help = 'Action to take')
    args = parser.parse_args()

    session = requests.Session()

    if 0 in args.actions:
        check_registration(session)

    if 1 in args.actions:
        response = check_login(session)
        key = response.json()['key']
        csrf_token = response.cookies['csrftoken']

    if 2 in args.actions:
        result = check_index_page(session, csrf_token)

    if 20 in args.actions:
        result = check_logout(session, csrf_token)
        print result