import json
from models import EcobiciCredentials
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

def get_ecobici_stations():
    url = 'https://pubsbapi.smartbike.com/api/v1/stations.json?access_token=%s'
    response = urlfetch.fetch(url % __get_access_token())
    if response.status_code == 401:
        response = urlfetch.fetch(url % __update_access_token())

    return json.loads(response.content)

def get_ecobici_status():
    url = 'https://pubsbapi.smartbike.com/api/v1/stations/status.json?access_token=%s'
    response = urlfetch.fetch(url % __get_access_token())
    if response.status_code == 401:
        response = urlfetch.fetch(url % __update_access_token())

    return json.loads(response.content)

def __get_access_token():
    entity_key = ndb.Key("EcobiciCredentials", "default_credentials")
    credentials = entity_key.get()

    return credentials.access_token

def __update_access_token():
    entity_key = ndb.Key("EcobiciCredentials", "default_credentials")
    credentials = entity_key.get()
    url = 'https://pubsbapi.smartbike.com/oauth/v2/token?client_id=%s&client_secret=%s&grant_type=client_credentials'
    response = urlfetch.fetch(url % (credentials.id, credentials.secret))    
    obj = json.loads(response.content)
    credentials.access_token = obj["access_token"]
    credentials.refresh_token = obj["refresh_token"]
    credentials.put()

    return credentials.access_token