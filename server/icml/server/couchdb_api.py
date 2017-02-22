from django.conf import settings
from couchdb import Server
from couchdb.client import Database
from couchdb.mapping import Document, TextField

# set up connection to couchdb in code
SERVER = Server(getattr(settings, 'COUCHDB_SERVER', 'http://admin:admin@127.0.0.1:5984'))

# Name of databases
DB_PASSWORD_RESET = 'password_reset'
DB_USER = '_users'
DB_PAPERS = 'papers'
DB_SESSIONS = 'sessions'


def get_database(name):
	return Database(getattr(settings, 'COUCHDB_SERVER', 'http://admin:admin@127.0.0.1:5984') + '/{}'.format(name))