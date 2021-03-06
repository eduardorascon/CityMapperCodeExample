import webapp2, json, os
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

class EcobiciPage(webapp2.RequestHandler):
    def get(self):
        obj = get_ecobici_stations()
        for ecobici_station in obj["stations"]:
            name = ecobici_station["name"]
            lat = str(ecobici_station["location"]["lat"])
            lon =str(ecobici_station["location"]["lon"])
            self.response.write("%s<br />lat:%s,lon:%s<br />" % (name, lat, lon))

    def post(self):
        obj = get_ecobici_stations()
        self.response.write(json.dumps(obj))

def get_ecobici_stations():
    url = 'https://pubsbapi.smartbike.com/api/v1/stations.json?access_token=%s'
    response = urlfetch.fetch(url % get_access_token())
    if response.status_code == 401:
        response = urlfetch.fetch(url % update_access_token())

    return json.loads(response.content)

def get_access_token():
    entity_key = ndb.Key("EcobiciCredentials", "default_credentials")
    credentials = entity_key.get()

    return credentials.access_token

def update_access_token():
    entity_key = ndb.Key("EcobiciCredentials", "default_credentials")
    credentials = entity_key.get()
    url = 'https://pubsbapi.smartbike.com/oauth/v2/token?client_id=%s&client_secret=%s&grant_type=client_credentials'
    response = urlfetch.fetch(url % (credentials.id, credentials.secret))    
    obj = json.loads(response.content)
    credentials.access_token = obj["access_token"]
    credentials.refresh_token = obj["refresh_token"]
    credentials.put()

    return credentials.access_token

class EcobiciCredentialsPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greeting': 'API CREDENTIALS'
        }

        path = os.path.join(os.path.dirname(__file__), 'html/credentials.html')
        self.response.write(template.render(path, template_values))

    def post(self):
        entity_key = ndb.Key("EcobiciCredentials", "default_credentials")
        credentials = entity_key.get()

        if credentials == None:
            credentials = EcobiciCredentials(key = entity_key)

        credentials.id = self.request.get("api_id")
        credentials.secret = self.request.get("api_secret")
        credentials.put()

        self.redirect('/ecobici')

class EcobiciCredentials(ndb.Model):
    id = ndb.StringProperty()
    secret = ndb.StringProperty()
    access_token = ndb.StringProperty()
    refresh_token = ndb.StringProperty()

class EcobiciCoveragePolygonPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greeting' : 'COVERAGE'
        }

        path = os.path.join(os.path.dirname(__file__), 'html/coverage.html')
        self.response.write(template.render(path, template_values))