import uuid

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django import shortcuts

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import couchdb_api

def index(request):
    return HttpResponse("Test")

@csrf_exempt
@require_POST
def registration(request):
    params = request.POST
    username = params['username']
    password = params['password']

    new_user = couchdb_api.SERVER.add_user(username, password, roles=None)

    # new_user_database = couchdb_api.SERVER.create(username)
    # security_doc = {
    #         "_id" : "_security",
    #         "admins": {
    #             "names": [
    #                 "admin"
    #             ],
    #             "roles": [
    #                 "admins"
    #             ]
    #         },
    #         "members": {
    #             "names": [username],
    #             "roles": [
    #                 "users"
    #             ]
    #         }
    #     }

    # try:
    #     new_user_database.save(security_doc)
    # except KeyError: # Although there's an error, the document is updated
    #     pass

    # print new_user_database['_security']

    return JsonResponse({'status' : True, 'message' : str(new_user)})

@csrf_exempt
@require_POST
def request_reset_password(request):
    params = request.POST

    username = params['username']
    secret = str(uuid.uuid4())

    password_reset_db = couchdb_api.get_database(couchdb_api.DB_PASSWORD_RESET)
    try:
        secret_doc = password_reset_db[username]
    except: # If already exists
        secret_doc = {
            '_id' : username,
            'secret' : secret
        }

    password_reset_db.save(secret_doc)

    # TODO: send out email once we determined which email server to use.

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