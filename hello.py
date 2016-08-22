import cgi
import os
from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2

class HelloPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'title': 'City Mapper '
        }

        path = os.path.join(os.path.dirname(__file__), 'html/hello.html')
        self.response.write(template.render(path, template_values))

    def post(self):
        comment = cgi.escape(self.request.get('content'))
        self.response.write('You wrote: ' + comment)