import webapp2

class CronJobsPage(webapp2.RequestHandler):
	def post(self):
		#Request data from Ecobici APi

		#Save data to DataStore