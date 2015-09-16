import cherrypy
import os
import requests

class Junake(object):
    @cherrypy.expose
    def index(self):
        return "Hello, world!"

    @cherrypy.expose
    def stations(self):
        return "stations (coming soon)"

    @cherrypy.expose
    def live_trains(self):
        return "live-trains (coming soon)"
        # Note that underscore in function name works out of the box for the dash in the URL
        
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
    cherrypy.quickstart(Junake())
