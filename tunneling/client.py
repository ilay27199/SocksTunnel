from typing import List

import requests
import json

from tunneling.consts import TUNNEL_STATION_IPS
from tunneling.json_utils import JSONEncoder
from tunneling.models.creds import UsernamePasswordCreds, Creds
from tunneling.models.station import Station


def create_add_request(station: Station):
    request_dict = {
        'command_type': 'add_station',
        'station': station
    }
    return request_dict


def create_del_request(ip):
    request_dict = {
        'command_type': 'del_station',
        'station_ip': ip
    }
    return request_dict


def create_set_tunnel_request(tunnel_stations_ips: List[str]):
    request_dict = {
        'command_type': 'set_tunnel',
        TUNNEL_STATION_IPS: tunnel_stations_ips
    }
    return request_dict


class TunnelClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port

    def send_request(self, request):
        json_request = json.dumps(request, cls=JSONEncoder)
        print(json_request)
        response = requests.get(f'http://{self.server_ip}:{self.server_port}', data=json_request)
        response_content = response.content
        return response_content

    def add_station(self, ip: str, port: int, creds: Creds):
        station = Station(ip=ip, port=port, creds=creds)
        add_request = create_add_request(station)
        return self.send_request(add_request)

    def del_station(self, ip):
        del_station_request = create_del_request(ip)
        return self.send_request(del_station_request)

    def set_tunnel(self, tunnel_stations):
        set_tunnel_request = create_set_tunnel_request(tunnel_stations)
        return self.send_request(set_tunnel_request)


def main():
    # Test
    client = TunnelClient('127.0.0.1', '9990')
    creds1 = UsernamePasswordCreds(username='ubuntu1', password='Password1')
    creds3 = UsernamePasswordCreds(username='ubuntu3', password='Password1')
    response = client.add_station('192.168.57.128', 1337, creds1)
    print(response)
    response = client.add_station('192.168.57.130', 1337, creds3)
    print(response)
    response = client.set_tunnel(['192.168.57.128', '192.168.57.130'])
    print(response)


if __name__ == '__main__':
    main()
