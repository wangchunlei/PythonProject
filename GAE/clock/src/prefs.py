import webapp2
import models
import logging

class PrefsPage(webapp2.RequestHandler):
    def post(self):
        userprefs = models.get_userprefs()
        try:
            tz_offset = int(self.request.get('tz_offset'))
            userprefs.tz_offset = tz_offset
            userprefs.put()
        except ValueError:
            # User entered a value that wasn`t an interget. Ignore for now.
            logging.error(ValueError.message)
            pass
        
        self.redirect('/')

application = webapp2.WSGIApplication([('/prefs', PrefsPage)], debug=True)
