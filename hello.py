import cgi
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2
import urllib, json

class HelloPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greeting': 'HOLAHOLA'
        }

        path = os.path.join(os.path.dirname(__file__), 'hello.html')
        self.response.write(template.render(path, template_values))

    def post(self):
        comment = cgi.escape(self.request.get('content'))
        self.response.write('You wrote: ' + comment)

class EcobiciPage(webapp2.RequestHandler):
    def get(self):
        url = 'http://api.labcd.mx/v1/movilidad/estaciones-ecobici'
        response = urllib.urlopen(url)
        obj = json.loads(response.read())
        self.response.write(obj)