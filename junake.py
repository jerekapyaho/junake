import os 
from flask import Flask

import json
import codecs
import requests
import datetime
import argparse
import arrow

app = Flask(__name__)

API = 'http://rata.digitraffic.fi/api/v1'
ENDPOINT_LIVE_TRAINS = '/live-trains'
ENDPOINT_COMPOSITIONS = '/compositions'
ENDPOINT_STATIONS = '/metadata/station'
ENDPOINT_SCHEDULES = '/schedules'

def load_stations():
    """Load the station list."""
    url = '%s%s' % (API, ENDPOINT_STATIONS)
    print('Getting stations from "%s"' % url)
    r = requests.get(url)
    stations = r.json()
    for s in stations:
        #print(s['stationName'])
        pass
    print('Got %d stations' % len(stations))
    return stations
 
 
def load_trains_for_station(station, arriving_count=20, departing_count=20):
    """Load the trains for a given station code.
    Optionally limits the number of arriving and departing trains.
    """
    params = { 'station': station,
               'arriving_trains': arriving_count,
               'departing_trains': departing_count }

    url = '%s%s' % (API, ENDPOINT_LIVE_TRAINS)
    print('Loading train data from "%s", params = %s' % (url, params))

    r = requests.get(url, params=params)
    print(r.url)
    json_data = r.json()
    #print(json_data)

    trains = json_data
    print('Got %d trains' % len(trains))

    arrivals = []
    departures = []

    for t in trains:
        train_number = t['trainNumber']
        train_type = t['trainType']
        #print('%s%d' % (train_type, train_number))
    
        rows = t['timeTableRows']
        #print('Number of timetable rows = %d' % len(rows))

        scheduled_time = None
        actual_time = None
        estimated_time = None
    
        stops = []
        
        for r in rows:
            current_station = r['stationShortCode']
            stopping = r['trainStopping']
            cancelled = r['cancelled']
            stop_type = r['type']
        
            if current_station == station and stopping and not cancelled:
                stops.append(station)

                train_info = { 'train_type': train_type,
                               'train_number': train_number }

                if 'scheduledTime' in r:
                    scheduled_time = arrow.get(r['scheduledTime']).to('local')
                    train_info['scheduled_time'] = scheduled_time
                if 'actualTime' in r:
                    actual_time = arrow.get(r['actualTime']).to('local')
                    train_info['actual_time'] = actual_time
                if 'liveEstimateTime' in r:
                    estimated_time = arrow.get(r['liveEstimateTime']).to('local')
                    train_info['estimated_time'] = estimated_time
            
                if stop_type == 'ARRIVAL':
                    arrivals.append(train_info)
                elif stop_type == 'DEPARTURE':
                    departures.append(train_info)
    
    return (arrivals, departures)
    
    
def station_trains(station):
    (arrivals, departures) = load_trains_for_station(station)
    
    print('\nArrivals')
    for i in arrivals:
        actual = '?'
        if 'actual_time' in i:
            actual = i['actual_time'].format('HH.mm')
        print('%s%d\ts=%s\ta=%s' % (i['train_type'], i['train_number'], i['scheduled_time'].format('HH.mm'), actual))

    print('\nDepartures')
    for i in departures:
        actual = '?'
        if 'actual_time' in i:
            actual = i['actual_time'].format('HH.mm')
        print('%s%d\ts=%s\ta=%s' % (i['train_type'], i['train_number'], i['scheduled_time'].format('HH.mm'), actual))
    
   
def load_trains_for_route(route_from, route_to):
    params = { 'departure_station': route_from,
               'arrival_station': route_to,
               'include_nonstopping': False }

    url = '%s%s' % (API, ENDPOINT_SCHEDULES)
    print('Loading schedule data from "%s", params = %s' % (url, params))

    r = requests.get(url, params=params)
    print(r.url)
    json_data = r.json()
    #print(json_data)

    trains = json_data
    print('Route %s-%s has %d trains' % (route_from, route_to, len(trains)))
    
    train_strings = []
    
    for t in trains:
        train_str = ''
                
        train_number = t['trainNumber']
        train_type = t['trainType']
        train_str += ('%s%d:\n' % (train_type, train_number))        
    
        rows = t['timeTableRows']
        #print('Number of timetable rows = %d' % len(rows))

        scheduled_time = None
        actual_time = None
        estimated_time = None
    
        stops = []

        for r in rows:
            current_station = r['stationShortCode']
            stopping = r['trainStopping']
            cancelled = r['cancelled']
            stop_type = r['type']

            if stop_type == 'ARRIVAL':
                train_str += '>'
            elif stop_type == 'DEPARTURE':
                train_str += '<'
            train_str += current_station + ' '
            
            if 'scheduledTime' in r:
                scheduled_time = arrow.get(r['scheduledTime']).to('local')
                train_str += scheduled_time.format('HH.mm')

            if 'actualTime' in r:
                actual_time = arrow.get(r['actualTime']).to('local')
                train_str += ' -> ' + actual_time.format('HH.mm')

            if 'liveEstimateTime' in r:
                estimated_time = arrow.get(r['liveEstimateTime']).to('local')
                train_str += ' ~' + estimated_time.format('HH.mm')

            train_str += '\n'
            
        #train_str += '\n'
        train_strings.append(train_str)
        
    return train_strings
    
def route_trains(route_from, route_to):
    train_strings = load_trains_for_route(route_from, route_to)
    for ts in train_strings:
        print(ts + '\n')


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, world!'
    
@app.route('/live-trains')
def live_trains():
    return 'Live trains!'
    
if __name__ == '__main__':
    app.debug = True
    app.run()
