from google.appengine.ext import ndb

class EcobiciCredentials(ndb.Model):
    id = ndb.StringProperty()
    secret = ndb.StringProperty()
    access_token = ndb.StringProperty()
    refresh_token = ndb.StringProperty()