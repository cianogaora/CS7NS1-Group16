import requests
import fastapi
from fastapi import APIRouter
from routes.contentrouter import RequestData, SensorData


class Subscriber:
    def __init__(self, sub_id, port):
        self.router = APIRouter()
        self.id = sub_id
        self.assigned_cr = ''
        self.port = port

        @self.router.post("/response")
        async def response(data: dict):
            print(f"subscriber received {data}")

    def join_network(self, controller_addr):
        print(f"registering subscriber {self.id} to controller on {controller_addr}")
        r = requests.get(controller_addr + '/register/subscriber')
        cr = r.content.decode().strip('\"')
        self.assigned_cr = cr
        print(f"subcriber {self.id} assigned to content router {self.assigned_cr}")

    def request_data(self, device_id, sensor_id):
        r = requests.get(f'http://{self.assigned_cr}/get_data/{device_id}/{sensor_id}?port={self.port}')
        print(f"subscriber received data {r.content}")

