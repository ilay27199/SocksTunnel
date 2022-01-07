from typing import List
import paramiko as paramiko
from twisted.web import resource
import json

from tunneling.consts import TUNNEL_STATION_IPS
from tunneling.models.station import Station
from tunneling.models.creds import UsernamePasswordCreds
from tunneling.json_utils import JSONDecoder
from stations_db_utils import get_stations_from_file, station_already_in_db, add_station_to_db, \
    remove_station_from_db_by_ip


def connect_to_station(ssh: paramiko.SSHClient, station: Station):
    if isinstance(station.creds, UsernamePasswordCreds):
        ssh.connect(station.ip, 22, station.creds.username, station.creds.password)


def get_local_tunneling_command(curr_station, next_station):
    # TODO: Check if needs to be modular
    socks5_connection_command = f"ssh -f -N -L {curr_station.port}:localhost:{next_station.port} " \
                                f"{next_station.creds['username']}@{next_station.ip}"
    return socks5_connection_command


def get_dynamic_tunneling_command(curr_station, next_station):
    # TODO: Check if needs to be modular
    socks5_connection_command = f"ssh -f -N -D {curr_station.port} {next_station.creds['username']}@{next_station.ip}"
    return socks5_connection_command


def create_ssh_tunnel_from_stations(stations_to_tunnel_ips: List[Station]):
    # TODO: Assuming at least 2 stations
    for curr_station, next_station in zip(stations_to_tunnel_ips[:-1], stations_to_tunnel_ips[1:-1]):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_to_station(ssh_client, curr_station)

        command = get_local_tunneling_command(curr_station, next_station)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdin.write(next_station.creds.password + "\n")

    station_before_last_station = stations_to_tunnel_ips[-2]
    last_station = stations_to_tunnel_ips[-1]
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connect_to_station(ssh_client, station_before_last_station)

    command = get_dynamic_tunneling_command(station_before_last_station, last_station)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    stdin.write(last_station.creds.password + "\n")


def success_response():
    response = {
        'status': 'success'
    }
    return json.dumps(response)


def failed_response(msg, extra=None):
    response = {
        'status': 'failed',
        'msg': msg,
        'extra': extra
    }
    return json.dumps(response)


def add_station(request: dict):
    station = request['station']

    if station_already_in_db(station):
        return failed_response('duplicate station; station already added')

    add_station_to_db(station)
    return success_response()


def del_station(request: dict):
    station_ip = request['station_ip']
    remove_station_from_db_by_ip(station_ip)
    return success_response()


def get_station_by_ip(ip: str, stations: List[Station]):
    for station in stations:
        if station.ip == ip:
            return station
    return None  # no station with that ip


def set_tunnel(request):
    db_stations = get_stations_from_file()
    station_ips_to_tunnel = request[TUNNEL_STATION_IPS]

    stations_to_tunnel = [get_station_by_ip(ip=station_ip, stations=db_stations) for station_ip in
                          station_ips_to_tunnel]
    stations_to_tunnel = [station for station in stations_to_tunnel if station is not None]  # remove Nones

    missing_stations = list(set(stations_to_tunnel) - set(db_stations))
    if not missing_stations:
        return failed_response('station/s are missing in db', extra={
            'stations': missing_stations
        })

    create_ssh_tunnel_from_stations(stations_to_tunnel)
    return success_response()


class Server(resource.Resource):
    def __init__(self):
        super().__init__()
        self.command_to_handler = {'add_station': add_station,
                                   'del_station': del_station,
                                   'set_tunnel': set_tunnel}

    def handle_request(self, request):
        request_command_type = request.pop('command_type')

        request_handler = self.command_to_handler.get(request_command_type)
        if request_handler is None:
            return failed_response('non existent command type', extra={
                'command_type': request_command_type
            })

        return request_handler(request)

    def validate_request(self, request):
        pass

    isLeaf = True

    def render_GET(self, request):
        request_str = request.content.read()
        request = json.loads(request_str, cls=JSONDecoder)

        # if self.validate_request(request_str) is False:
        #     return  # TODO: Handle with not valid requests

        response = self.handle_request(request)
        bytes_format_response = bytes(response, 'utf-8')
        return bytes_format_response
