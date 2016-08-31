import json
from google.appengine.api import urlfetch

class ecobici:
    def get_ecobici_stations():
        url = 'https://pubsbapi.smartbike.com/api/v1/stations.json?access_token=%s'
        response = urlfetch.fetch(url % get_access_token())
        if response.status_code == 401:
            response = urlfetch.fetch(url % update_access_token())

        return json.loads(response.content)

    def get_ecobici_status():
        url = 'https://pubsbapi.smartbike.com/api/v1/stations/status.json?access_token=%s'
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
