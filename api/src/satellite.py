import argparse
import threading

import requests
import uvicorn
from contentrouter import RegisterDevice
import sensor
import time
import fastapi
from fastapi import FastAPI, APIRouter


class Device:

    def __init__(self, pub_id, port):
        self.content_router = ''
        self.location = sensor.Location()
        self.altitude = sensor.Altitude()
        self.angle = sensor.Angle()
        self.speed = sensor.Speed()
        self.eccentricity = sensor.Eccentricity()
        self.temperature = sensor.Temperature()
        self.signal = sensor.Signal()
        self.microwave = sensor.Microwave()
        self.router = APIRouter()
        self.id = pub_id
        self.port = port

        @self.router.get("/get_data/{device_id}/{sensor_id}")
        async def get_data(device_id: str, sensor_id: str):
            if sensor_id == 'Location':
                return self.location
            elif sensor_id == 'Altitude':
                return self.altitude
            elif sensor_id == 'Speed':
                return self.speed
            elif sensor_id == 'Eccentricity':
                return self.eccentricity
            elif sensor_id == 'Temperature':
                return self.temperature
            elif sensor_id == 'Signal':
                return self.signal
            elif sensor_id == 'Microwave':
                return self.microwave

    def join_network(self, controller_addr, controller_port, dev_addr, device_id, sensor_id):
        print(f"registering satellite {device_id} on {controller_addr}:{controller_port}")

        data = RegisterDevice(device_id=device_id, device_address=dev_addr)
        print(f"registering to http://{controller_addr}:{controller_port}/register/device")
        print(data)
        r = requests.post(f"http://{controller_addr}:{controller_port}/register/device",
                          data=data.json())
        cr = r.content.decode().strip('\"')
        self.content_router = cr


def join(pub, controller_addr, controller_port, host, port):
    time.sleep(3)
    pub.join_network(controller_addr, controller_port, f"{host}:{port}", pub.id, '')


parser = argparse.ArgumentParser(description='register to network')
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--pub_id', type=str, default='pub')
parser.add_argument('--port', type=int, default=8006)
parser.add_argument('--controller_address', type=str, default='localhost')
parser.add_argument('--controller_port', type=str, default='8004')

if __name__ == '__main__':

    pub = Device(parser.parse_args().pub_id, parser.parse_args().port)
    app = fastapi.FastAPI()
    app.include_router(pub.router)

    thread = threading.Thread(target=join, args=(pub, parser.parse_args().controller_address, parser.parse_args().controller_port, parser.parse_args().host, parser.parse_args().port,))
    thread.start()
    try:
        uvicorn.run(app, host=parser.parse_args().host,
                    port=parser.parse_args().port)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        exit(0)
