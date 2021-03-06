import os
import requests
import json
import arrow
from flask import Flask

app = Flask(__name__)

BASE_URL = 'http://rata.digitraffic.fi/api/v1'
STATIONS_ENDPOINT = '/metadata/station'
LIVE_TRAINS_ENDPOINT = '/live-trains'

TRAIN_CATEGORY = {'longDistance': 'Long-distance',
                  'commuter': 'Commuter',
                  'cargo': 'Cargo'}

JSON_MIME_TYPE = 'application/json'

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/stations')
def stations(self):
    r = requests.get(BASE_URL + STATIONS_ENDPOINT)

    js = json.dumps(r.json())
    resp = Response(js, status=200, mimetype=JSON_MIME_TYPE)
    return resp

@app.route(LIVE_TRAINS_ENDPOINT)
def live_trains(self, station=None, arriving_trains=None, departing_trains=None, category='all', epoch=False):
    """Implements the live-trains endpoint."""

    def relevant_timetable_rows(all_rows):
        """Returns the timetable rows which are relevant to us."""
        rows = [r for r in all_rows if r['stationShortCode'] == station 
                                   and r['trainStopping'] 
                                   and not r['cancelled']]
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

    # Parse the category argument. Comma separated. 
    # Allowed values: all, longDistance, commuter, cargo.
    if category == 'all':
        train_set = set([TRAIN_CATEGORY[k] for k in TRAIN_CATEGORY.keys()])
    else:
        train_set = set([TRAIN_CATEGORY[c] for c in category.split(',')])

    #
    # Get the trains that match our desired category
    #
    trains = [t for t in all_trains if t['trainCategory'] in train_set]
        
    for t in trains:  
        train_number = t['trainNumber']
        train_type = t['trainType']
        
        all_rows = t['timeTableRows']
        
        origin_station = all_rows[0]['stationShortCode']
        destination_station = all_rows[-1]['stationShortCode']
        
        rows = relevant_timetable_rows(all_rows)

        # Process the times in the timetable rows.
        # Convert them to epoch time if necessary.
        for r in rows:
            scheduled_time = None
            live_estimate_time = None                
            actual_time = None
                
            # There is always a scheduled time
            scheduled_time = arrow.get(r['scheduledTime'])
                
            # There may be a live estimate time
            if 'liveEstimateTime' in r:                    
                live_estimate_time = arrow.get(r['liveEstimateTime'])
                    
            # There may be an actual time
            if 'actualTime' in r:
                actual_time = arrow.get(r['actualTime'])
                    
            if epoch:
                r['scheduledTime'] = scheduled_time.timestamp
                if live_estimate_time:
                    r['liveEstimateTime'] = live_estimate_time.timestamp
                if actual_time:
                    r['actualTime'] = actual_time.timestamp

        # Replace the old timetable row list with the new filtered one
        t['timeTableRows'] = rows

    #print(len(trains))
    
    js = json.dumps(trains)
    resp = Response(js, status=200, mimetype=JSON_MIME_TYPE)
    return resp

if __name__ == '__main__':
    app.run()
