import json
import os
from typing import List

from tunneling.consts import STATIONS_DB_FILE
from tunneling.json_utils import JSONDecoder, JSONEncoder
from tunneling.models.station import Station


def init_stations_file():
    save_stations_to_file([])


def get_stations_from_file() -> List[Station]:
    if not os.path.exists(STATIONS_DB_FILE):
        init_stations_file()

    with open(STATIONS_DB_FILE, 'r') as stations_db_file:
        return json.load(stations_db_file, cls=JSONDecoder)


def save_stations_to_file(stations: List[Station]):
    with open(STATIONS_DB_FILE, 'w') as stations_db_file:
        json.dump(stations, stations_db_file, cls=JSONEncoder)


def station_already_in_db(station: Station):
    stations = get_stations_from_file()
    return station in stations


def add_station_to_db(station: Station):
    stations = get_stations_from_file()
    if station not in stations:
        stations.append(station)
        save_stations_to_file(stations)


def remove_station_from_db_by_ip(ip: str):
    stations = get_stations_from_file()
    for station in stations:
        if station.ip == ip:
            stations.remove(station)
    save_stations_to_file(stations)
