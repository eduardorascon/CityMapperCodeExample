import webapp2
import urllib, json
from google.appengine.ext import db

class EcobiciPage(webapp2.RequestHandler):
    def get(self):
        url = 'http://api.labcd.mx/v1/movilidad/estaciones-ecobici'
        response = urllib.urlopen(url)
        obj = json.load(response)
        for ecobici_station in obj:
            self.response.write(ecobici_station["location"] + "<br />")