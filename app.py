import cherrypy
import os
import requests
import json
import arrow

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
        """
        Implements the live-trains endpoint.
        Note that an underscore in the function name replaces the dash in the URL
        (i.e., 'live-trains' maps to 'live_trains').
        """

        def relevant_timetable_rows(all_rows):
            """Returns the timetable rows which are relevant to us."""
            # The traditional way
            rows = []
            for r in all_rows:
                row_station = r['stationShortCode']
                is_stopping = r['trainStopping']
                cancelled = r['cancelled']
                stop_type = r['type']
                is_commercial_stop = r['commercialStop']
            
                if row_station == station and is_stopping and is_commercial_stop and not cancelled:
                    rows.append(r)

            # Using list comprehension
            rows = [r for r in all_rows if r['stationShortCode'] == station and r['trainStopping'] and r['commercialStop'] and not r['cancelled']]
            
            return rows
            
        params = {}
        if station != None:
            params['station'] = station
        if arriving_trains != None:
            params['arriving_trains'] = int(arriving_trains)
        if departing_trains != None:
            params['departing_trains'] = int(departing_trains)
        #print(params)
        r = requests.get(BASE_URL + LIVE_TRAINS_ENDPOINT, params)
        #print(r.url)
        
        all_trains = r.json()
        
        arrivals = []
        departures = []
        
        train_set = set(['Long-distance', 'Commuter'])
        
        #
        # Get the trains that match our desired category
        #
        
        # The traditional way
        trains = []
        for t in all_trains:
            if t['trainCategory'] in train_set:
                trains.append(t)
                
        # Using list comprehension
        trains = [t for t in all_trains if t['trainCategory'] in train_set]
        
        for t in trains:  
            train_number = t['trainNumber']
            train_type = t['trainType']
        
            all_rows = t['timeTableRows']
        
            origin_station = all_rows[0]['stationShortCode']
            destination_station = all_rows[-1]['stationShortCode']
        
            rows = relevant_timetable_rows(all_rows)
            
            # Replace the old timetable row list with the new filtered one
            t['timeTableRows'] = rows
       
        return json.dumps(trains, indent=4)
        
if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
    cherrypy.quickstart(Junake())
