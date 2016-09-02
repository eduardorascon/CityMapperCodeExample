import webapp2, json
import apicalls

class CronJobsPage(webapp2.RequestHandler):
	def post(self):
		#Request data from Ecobici API every 30 seconds.
        obj = apicalls.get_ecobici_stations()
		#Save data to DataStore
        status_list = []
        for station_status in obj["stationsStatus"]:
            status = __CreateStatusEntity(station_status)
            status_list.append(status)

        ndb.put_multi(status_list)

    def __CreateStatusEntity(stationStatus):
        s = EcobiciStationStatus()
        s.timestamp = "20160901130000"
        s.id = station_status["id"]
        s.status =  station_status["status"]
        s.slots_occupied = station_status["availability"]["bikes"]
        s.slots_available = station_status["availability"]["slots"]

        return s

class EcobiciStationStatus(ndb.Model):
    timestamp = ndb.StringProperty()
    id = ndb.IntegerProperty()
    status = ndb.StringProperty()
    slots_occupied = ndb.IntegerProperty()
    slots_available = ndb.IntegerProperty()