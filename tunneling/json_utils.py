import json

from tunneling.models.station import Station
from tunneling.models.creds import UsernamePasswordCreds


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.to_json()
        except Exception:
            return obj


class JSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            if obj.get('type') == Station.TYPE:
                return Station.from_json(obj)
            elif obj.get('type') == UsernamePasswordCreds.TYPE:
                return UsernamePasswordCreds.from_json(obj)
        return obj
