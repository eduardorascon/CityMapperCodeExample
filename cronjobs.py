import webapp2
import apicalls

class CronJobsPage(webapp2.RequestHandler):
	def post(self):
		#Request data from Ecobici API every 30 seconds.

		#Save data to DataStore

