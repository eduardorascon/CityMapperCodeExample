import webapp2
import urllib, json

class EcobiciPage(webapp2.RequestHandler):
    def get(self):
        url = 'http://api.labcd.mx/v1/movilidad/estaciones-ecobici'
        response = urllib.urlopen(url)
        obj = json.load(response)
        self.response.headers['Content-Type'] = 'application/json'
        for ecobici_station in obj:
            for attribute, value in ecobici_station.iteritems():
                self.response.write(attribute + '::')
            self.response.write('<br />')