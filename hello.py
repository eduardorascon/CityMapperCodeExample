import cgi
from google.appengine.api import users
import webapp2

class HelloPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("""
        <html>
        <body>
        <form action="/hello" method="POST">
            <textarea name="content" rows="3" cols="60"></textarea>
            <input type="submit" value="Sign Guestbook" />
        </form>
        </body>
        </html>
        """)

    def post(self):
        self.response.write('You wrote: ' + self.request.get('content'))