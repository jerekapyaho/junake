import json
import codecs
import requests
import datetime
import argparse

# Trying Arrow for date handling
import arrow


API = 'http://rata.digitraffic.fi/api/v1'
ENDPOINT_LIVE_TRAINS = '/live-trains'
ENDPOINT_COMPOSITIONS = '/compositions'
ENDPOINT_STATIONS = '/metadata/station'
STATION = 'HKI'

# Loads the station list
def load_stations():
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
    params = { 'station': station,
               'arrivingTrains': arriving_count,
               'departedTrains': departing_count }

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
            station = r['stationShortCode']
            stopping = r['trainStopping']
            cancelled = r['cancelled']
            stop_type = r['type']
        
            if station == STATION and stopping and not cancelled:
        
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
    
        #print('Composition:')
        #params = 'departure_date=2015-01-29'
        #url = '%s%s/%s?%s' % (API, ENDPOINT_COMPOSITIONS, t['trainNumber'], params)
        #print('About to hit URL %s' % url)
        #response = urllib.request.urlopen(url)

    return (arrivals, departures)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show trains arriving at or departing from a given station.')
    parser.add_argument('-s', '--station', help='Station short code')
    args = parser.parse_args()
    
    stations = load_stations()
    
    (arrivals, departures) = load_trains_for_station(args.station)
    
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
