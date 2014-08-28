import webapp2
# from google.appengine.ext.webapp.util import run_wsgi_app
import datetime
import jinja2
import os
import models

from google.appengine.api import users

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class MainPage(webapp2.RequestHandler):       
    def get(self):
        current_time = datetime.datetime.now()
        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)
        
        userprefs = models.get_userprefs()
        if userprefs:
            current_time += datetime.timedelta(0, 0, 0, 0, 0, userprefs.tz_offset)
        template = template_env.get_template('home.html')
        context = {
                 'current_time':current_time,
                 'user':user,
                 'login_url':login_url,
                 'logout_url':logout_url,
                 'userprefs':userprefs,
                 }
        self.response.out.write(template.render(context))
        
#         self.response.headers['Content-Type'] = 'text/html'
#         message = '<p>The time is: %s</p>' % datetime.datetime.now()
#         self.response.out.write(message)


application = webapp2.WSGIApplication([('/', MainPage)], debug=True)


# def main():
#     run_wsgi_app(application)
# 
# if __name__ == "__main__":
#     main()
