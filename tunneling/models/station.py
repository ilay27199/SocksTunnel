import ipaddress

from .creds import Creds


class Station:
    TYPE = 'station'

    def __init__(self, ip: str, port: int, creds: Creds):
        self.ip = ip
        self.port = port
        self.creds = creds

    @staticmethod
    def from_json(station_dict):
        return Station(
            ip=station_dict['ip'],
            port=station_dict['port'],
            creds=station_dict['creds']
        )

    def to_json(self):
        return {
            'type': Station.TYPE,
            'ip': self.ip,
            'port': self.port,
            'creds': self.creds
        }

    def __eq__(self, other):
        return self.ip == other.ip

    def __hash__(self):
        return int(ipaddress.IPv4Address(self.ip))
