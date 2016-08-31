import webapp2
from apicalls import ecobici
class CronJobsPage(webapp2.RequestHandler):
	def post(self):
		#Request data from Ecobici API every 30 seconds.

		#Save data to DataStore

