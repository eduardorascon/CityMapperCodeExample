import webapp2
import urllib, json
import os
from google.appengine.ext import db
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