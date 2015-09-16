import cherrypy
import os

class Junake(object):
    @cherrypy.expose
    def index(self):
        return "Hello, world!"

    @cherrypy.expose
    def stations(self):
        return "stations (coming soon)"

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
    cherrypy.quickstart(Junake())
