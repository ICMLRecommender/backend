from django.conf import settings
from couchdb import Server
from couchdb.client import Database
from couchdb.mapping import Document, TextField

_DB_CREDENTIALS = getattr(settings, 'COUCHDB_SERVER', 'http://admin:admin@127.0.0.1:5984')

# set up connection to couchdb in code
SERVER = Server(_DB_CREDENTIALS)

# Name of databases
DB_PASSWORD_RESET = 'password_reset'
DB_USER = '_users'
DB_PAPERS = 'papers'
DB_SESSIONS = 'sessions'

DB_COMMENTS = 'usercomments'
DB_LIKES = 'userlikes'

def get_database(name):
    # return Database(_DB_CREDENTIALS + '/{}'.format(name))
    return SERVER[name]