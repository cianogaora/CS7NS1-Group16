import argparse
import threading

import requests
import uvicorn

import sensor
import time
import fastapi
from fastapi import  FastAPI,APIRouter

app = FastAPI()
class Device:

    def __init__(self,pub_id,port):
        self.content_router = ''
        self.location = sensor.Location()
        self.altitude = sensor.Altitude()
        self.angle = sensor.Angle()
        self.speed = sensor.Speed()
        self.eccentricity = sensor.Eccentricity()
        self.temperature = sensor.Temperature()
        self.router = APIRouter()
        self.id = pub_id
        self.port = port
        @self.router.get("/get_data/{device_id}/{sensor_id}")
        async def get_data(device_id:str,sensor_name:str):
            if sensor_name == 'Location':
                return self.location
            elif sensor_name == 'Altitude':
                return self.altitude
            elif sensor_name == 'Speed':
                return self.speed
            elif sensor_name == 'Eccentricity':
                return self.eccentricity
            elif sensor_name == 'Temperature':
                return self.temperature

    def join_network(self, controller_addr, device_id, sensor_name):
        r = requests.post(controller_addr+'/device/register/', json={'device_id':device_id,'sensor_name':sensor_name})
        cr = r.content.decode().strip('\"')
        self.content_router = cr



def join(pub):
    time.sleep(5)
    pub.join_network("http://127.0.0.1:8004", '0', 'Location')



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='register to network')
    parser.add_argument('--host',type=str,default='localhost')
    parser.add_argument('--pub_id',type=str,default='pub')
    parser.add_argument('--port',type=int,default=8004)

    pub = Device(parser.parse_args().pub_id, parser.parse_args().port)
    app = fastapi.FastAPI()
    app.include_router(pub.router)

    thread = threading.Thread(target=join,args=(pub,))
    thread.start()
    try:
        uvicorn.run(app,host=parser.parse_args().host,
                    port=parser.parse_args().port)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        exit(0)