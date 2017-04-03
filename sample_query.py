import requests
import json
import sys
import argparse

HOST_PREFIX = "http://127.0.0.1:8000"
ICML_PREFIX = "{0}/icml".format(HOST_PREFIX)

USER_SECRET = '8daae7447f0d4d068429acaef5cd97bc'

def is_success(r):
    if r.status_code != 200:
        print r.status_code
        print r.text

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

############################################################################################################################
############################################End of user authentication section##############################################
############################################################################################################################


def check_post_comments(session):
    url = '{0}/post_comment/'.format(ICML_PREFIX)
    data = {
        'username' : 'hptruong',
        'secret' : USER_SECRET,
        'paper_id' : 'the_testing_id',
        'comment' : 'This is a test comment whose content is nothing.'
    }
    r1 = session.post(url, data = data)

    assert is_success(r1)


    data = {
        'username' : 'hptruong',
        'secret' : USER_SECRET,
        'paper_id' : 'the_testing_id',
        'comment' : 'This is another test comment whose content is nothing.'
    }
    r2 = session.post(url, data = data)

    assert is_success(r2)
    return r1, r2

def check_post_comments_bis(session):
    url = '{0}/post_comment/'.format(ICML_PREFIX)
    data = {
        'username' : 'hptruong',
        'secret' : USER_SECRET,
        'paper_id' : 'the_testing_id',
        'comment' : 'This is the third test comment whose content is nothing.'
    }
    r = session.post(url, data = data)

    assert is_success(r)
    return r

def check_delete_comment(session, ids = []):
    url = '{0}/delete_comment/'.format(ICML_PREFIX)

    for the_id in ids:
        data = {
            'username' : 'hptruong',
            'secret' : USER_SECRET,
            'paper_id' : 'the_testing_id',
            'comment_id' : the_id
        }
        r = session.post(url, data = data)

        assert is_success(r)

    return None


def check_like_paper(session):
    url = '{0}/like_paper/'.format(ICML_PREFIX)
    data = {
        'username' : 'hptruong',
        'secret' : USER_SECRET,
        'paper_id' : 'the_testing_id',
    }
    r = session.post(url, data = data)

    assert is_success(r)
    return r

def check_like_paper_bis(session):
    url = '{0}/like_paper/'.format(ICML_PREFIX)
    data = {
        'username' : 'hptruong',
        'secret' : USER_SECRET,
        'paper_id' : 'the_testing_id',
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

    if 3 in args.actions:
        r1, r2 = check_post_comments(session)
        comment_id1 = r1.json()['id']
        comment_id2 = r2.json()['id']
        comment_id3 = check_post_comments_bis(session).json()['id']

    if 4 in args.actions:
        check_delete_comment(session, [comment_id1, comment_id3])

    if 5 in args.actions:
        check_delete_comment(session, [comment_id2])

    if 6 in args.actions:
        check_like_paper(session)