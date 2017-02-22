import requests
import json
import sys
import argparse

HOST_PREFIX = "http://127.0.0.1:8000"
ICML_PREFIX = "{0}/icml".format(HOST_PREFIX)

def is_success(r):
    print r.status_code
    print r

    return r.status_code == 200

def check_registration(session):
    url = '{0}/registration/'.format(ICML_PREFIX)
    data = {
                'username' : 'hptruong',
                'password' : 'supersecret',
            }

    r = session.post(url, data = data)

    assert is_success(r)
    return r

def check_reset_password_request(session):
    url = '{0}/request_reset_password/'.format(ICML_PREFIX)
    data = {
        'username' : 'hptruong'
    }
    r = session.post(url, data = data)

    assert is_success(r)
    return r

def check_password_reset(session):
    url = '{0}/reset_password/'.format(ICML_PREFIX)
    data = {
        'username' : 'hptruong',
        'password' : 'whitefox',
        'secret' : 'd9ea9b4c-a32e-4147-a856-c06d1f4d870c'
    }
    r = session.post(url, data = data)

    assert is_success(r)
    return r

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Django test client')
    parser.add_argument('-f', type = int, nargs = '+', dest='actions', required = True, default = [0], help = 'Action to take')
    args = parser.parse_args()

    session = requests.Session()

    if 0 in args.actions:
        check_registration(session)

    if 1 in args.actions:
        response = check_reset_password_request(session)

    if 2 in args.actions:
        check_password_reset(session)