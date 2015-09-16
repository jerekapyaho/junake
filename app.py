import cherrypy
import os

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello, world!"

cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
