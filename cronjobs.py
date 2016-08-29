import webapp2

class CronJobsPage(webapp2.RequestHandler):
	def post(self):
		#Request data from Ecobici APi every 30 seconds.

		#Save data to DataStore

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