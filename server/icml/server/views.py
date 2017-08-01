import uuid
import datetime
import traceback
import re

import couchdb

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django import shortcuts

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from server import email_utils
from server import couchdb_api

username_regex = re.compile('^([a-z0-9_])+$') # Only allowing lower case letter, and _

def index(request):
    return HttpResponse("There is nothing here.")

@csrf_exempt
@require_POST
def registration(request):
    params = request.POST

    try:
        username = params['username']
        password = params['password']
        email = params['email']
    except:
        return HttpResponseBadRequest('Missing required field(s) during registration.')

    if not username_regex.match(username):
        return HttpResponseBadRequest('Invalid username. It must contain only lower case letter, numbers, or _.')

    try:
        new_user = couchdb_api.SERVER.add_user(username, password, roles=None)
    except couchdb.http.ResourceConflict as e:
        return HttpResponseBadRequest('Username already existed.')

    new_user_database = couchdb_api.SERVER.create(username)
    security_doc = {
            "_id" : "_security",
            "admins": {
                "names": [
                    "admin"
                ],
                "roles": [
                    "admins"
                ]
            },
            "members": {
                "names": [username],
                "roles": [
                    "users"
                ]
            }
        }

    try:
        new_user_database.save(security_doc)
    except KeyError: # Although there's an error, the document is updated
        pass

    secret_doc = {
        '_id' : "secret",
        'value' : uuid.uuid4().hex
    }

    new_user_database.save(secret_doc)

    email_doc = {
        '_id' : 'email',
        'value' : email
    }
    new_user_database.save(email_doc)

    # print new_user_database['_security']

    return JsonResponse({'status' : True, 'message' : str(new_user)})

@csrf_exempt
@require_POST
def request_reset_password(request):
    params = request.POST

    username = params['username']
    try:
        user_db = couchdb_api.get_database(username)
        user_email = user_db['email']['value']
    except:
        return HttpResponseBadRequest('Username or email does not exist.')

    secret = str(uuid.uuid4())

    password_reset_db = couchdb_api.get_database(couchdb_api.DB_PASSWORD_RESET)
    try:
        secret_doc = password_reset_db[username]
        secret_doc['secret'] = secret
    except: # If already exists
        secret_doc = {
            '_id' : username,
            'secret' : secret
        }

    password_reset_db.save(secret_doc)

    # TODO: send out email once we determined which email server to use.
    email_utils.send_email(user_email, 'ICML 2017 Password Reset Secret', 'Hello,\n\nYou have recently requested to reset your password for ICML 2017 web site. Please use this secret key to reset your password: \n{}\n\nIf you did not request a password reset, please ignore this email.\n\nThank you\nThe ICML 2017 Recommender App Team.'.format(secret))

    return JsonResponse({'status' : True, 'message' : 'Registered reset password secret.'})

@csrf_exempt
@require_POST
def reset_password(request):
    params = request.POST

    username = params['username']
    new_password = params['password']
    secret = params['secret'] # Key to identify if this is the user who requested the password change

    # Check for request validity
    password_reset_db = couchdb_api.get_database(couchdb_api.DB_PASSWORD_RESET)
    try:
        change_doc = password_reset_db[username]
        if change_doc['secret'] != secret:
            return HttpResponseBadRequest('Invalid key to change password for this user.')
    except:
        return HttpResponseBadRequest('Invalid key to change password for this user.')

    user_db = couchdb_api.get_database(couchdb_api.DB_USER)
    user = user_db['org.couchdb.user:{}'.format(username)]
    user['password'] = new_password

    user_db.save(user)

    password_reset_db.delete(change_doc)

    return JsonResponse({'status' : True, 'message' : 'Password udpated.'})

############################################################################################################################
############################################End of user authentication section##############################################
############################################################################################################################

def _check_user_secret(authenticated_post_request_params):
    try:
        username = authenticated_post_request_params['username']
        secret = authenticated_post_request_params['secret']
        user_db = couchdb_api.get_database(username)

        return user_db['secret']['value'] == secret
    except:
        traceback.print_exc()
        return False

@csrf_exempt
@require_POST
def post_comment(request):
    params = request.POST

    if not _check_user_secret(params):
        return HttpResponseBadRequest('Unable to verify user identity.')

    paper_id = params['paper_id']
    comment = params['comment']

    comment_db = couchdb_api.get_database(couchdb_api.DB_COMMENTS)

    try:
        paper = comment_db[paper_id]
    except:
        paper = {
            '_id' : paper_id,
            'comments' : []
        }

    comment_object = {
        'id' : str(uuid.uuid4()),
        'time' : datetime.datetime.now().isoformat(),
        'comment' : comment,
        'username' : params['username']
    }
    paper['comments'].append(comment_object)
    comment_db.save(paper)

    return JsonResponse({'status' : True, 'id' : comment_object['id']})

@csrf_exempt
@require_POST
def delete_comment(request):
    params = request.POST

    if not _check_user_secret(params):
        return HttpResponseBadRequest('Unable to verify user identity.')

    paper_id = params['paper_id']
    comment_id = params['comment_id']

    comment_db = couchdb_api.get_database(couchdb_api.DB_COMMENTS)

    try:
        paper = comment_db[paper_id]
    except:
        return HttpResponseBadRequest('Paper does not exist.')

    found_comment = False
    for index, comment in enumerate(paper['comments']):
        if comment['id'] == comment_id:
            found_comment = True
            del paper['comments'][index]
            break

    if found_comment:
        comment_db.save(paper)
        return JsonResponse({'status' : True})
    else:
        return HttpResponseBadRequest('Comment does not exist.')


@csrf_exempt
@require_POST
def like_paper(request):
    params = request.POST

    if not _check_user_secret(params):
        return HttpResponseBadRequest('Unable to verify user identity.')

    username = params['username']
    paper_id = params['paper_id']

    like_db = couchdb_api.get_database(couchdb_api.DB_LIKES)
    reversed_like_db = couchdb_api.get_database(couchdb_api.DB_REVERSED_LIKES)

    try:
        paper = like_db[paper_id]
    except:
        paper = {
            '_id' : paper_id,
            'likes' : {}
        }

    try:
        user = reversed_like_db[username]
    except:
        user = {
            '_id' : username,
            'likes' : {}
        }

    if username in paper['likes']: # Then unlike
        del paper['likes'][username]
        del user['likes'][paper_id]
    else: # Then like
        like_object = {
            'time' : datetime.datetime.now().isoformat(),
        }
        paper['likes'][username] = like_object
        user['likes'][paper_id] = like_object

    like_db.save(paper)
    reversed_like_db.save(user)

    return JsonResponse({'status' : True})
