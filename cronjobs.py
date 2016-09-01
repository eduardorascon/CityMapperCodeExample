import webapp2, json
import apicalls

class CronJobsPage(webapp2.RequestHandler):
	def post(self):
		#Request data from Ecobici API every 30 seconds.
        obj = apicalls.get_ecobici_stations()
		#Save data to DataStore
        status_list = []
        for station_status in obj["stationsStatus"]:
            status = EcobiciStationStatus()
            status.timestamp = "20160901130000"
            station.id = station_status["id"]
            station.status =  station_status["status"]
            station.slots_occupied = station_status["availability"]["bikes"]
            station.slots_available = station_status["availability"]["slots"]
            status_list.append(status)

        ndb.put_multi(status_list)

class EcobiciStationStatus(ndb.Model):
    timestamp = ndb.StringProperty()
    station_id = ndb.IntegerProperty()
    station_status = ndb.StringProperty()
    slots_occupied = ndb.IntegerProperty()
    slots_available = ndb.IntegerProperty()