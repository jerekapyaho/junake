import cherrypy
import os
import requests
import json

BASE_URL = 'http://rata.digitraffic.fi/api/v1'
STATIONS_ENDPOINT = '/metadata/station'
LIVE_TRAINS_ENDPOINT = '/live-trains'

class Junake(object):
    @cherrypy.expose
    def index(self):
        return "Hello, world!"

    @cherrypy.expose
    def stations(self):
        r = requests.get(BASE_URL + STATIONS_ENDPOINT)
        
        return json.dumps(r.json(), indent=4)

    @cherrypy.expose
    def live_trains(self, station=None, arriving_trains=None, departing_trains=None):
        params = {}
        if station != None:
            params['station'] = station
        if arriving_trains != None:
            params['arriving_trains'] = int(arriving_trains)
        if departing_trains != None:
            params['departing_trains'] = int(departing_trains)
        print(params)
        r = requests.get(BASE_URL + LIVE_TRAINS_ENDPOINT, params)
        print(r.url)
        return json.dumps(r.json(), indent=4)
        # Note that underscore in function name works out of the box for the dash in the URL
        # (i.e., 'live-trains' maps to 'live_trains').
        
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
    cherrypy.quickstart(Junake())
