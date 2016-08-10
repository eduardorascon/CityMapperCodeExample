import webapp2
import urllib, json
import os
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

class EcobiciPage(webapp2.RequestHandler):
    def get(self):
        url = 'http://api.labcd.mx/v1/movilidad/estaciones-ecobici'
        response = urllib.urlopen(url)
        obj = json.load(response)
        for ecobici_station in obj:
            self.response.write(ecobici_station["location"] + "<br />")

class EcobiciCredentialsPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greeting': 'API CREDENTIALS'
        }

        path = os.path.join(os.path.dirname(__file__), 'credentials.html')
        self.response.write(template.render(path, template_values))

    def post(self):
        entity_key = ndb.Key("EcobiciCredentials", "default_credentials")
        credentials = entity_key.get()

        if credentials == None:
            credentials = EcobiciCredentials(key = entity_key)

        credentials.api_key = self.request.get("api_key")
        credentials.api_secret = self.request.get("api_secret")
        credentials.put()

        self.redirect('/ecobici')


class EcobiciCredentials(ndb.Model):
    api_key = ndb.StringProperty()
    api_secret = ndb.StringProperty()