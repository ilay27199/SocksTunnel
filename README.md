# SocksTunnel

## Client Requests

```json
{
  "command_type": "add_station",
  "station": {
    "type": "station",
    "ip": "1.1.1.1",
    "port": 1111,
    "creds": {
      "type": "creds",
      "creds_type": "username_password_creds",
      "username": "admin",
      "password": "admin"
    }
  }
}
```

```json
{
  "command_type": "del_station",
  "station_ip": "1.1.1.1"
}
```

```json
{
  "command_type": "set_tunnel",
  "tunnel_station_ips": [
    "1.1.1.1",
    "1.2.3.4",
    "5.5.5.5"
  ]
}
```

## Server Response

success response
```python
response = {
  'status': 'success'
}

```

failed response example
```python
response = {
  'status': 'failed',
  'msg': 'station/s are missing in db',
  'extra': {
      'stations': ['1.2.2.2', '4.4.4.4']
  }
}
```
