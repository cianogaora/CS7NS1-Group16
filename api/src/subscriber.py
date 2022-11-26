import argparse
import threading
import time

import requests
import fastapi
import uvicorn
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
            print(f"subscriber{self.id} received response: {data}")

    def join_network(self, controller_addr):
        print(f"registering subscriber {self.id} to controller on {controller_addr}")
        r = requests.get(controller_addr + '/register/subscriber')
        cr = r.content.decode().strip('\"')
        self.assigned_cr = cr
        print(f"subscriber {self.id} assigned to content router {self.assigned_cr}")

    def request_data(self, device_id, sensor_id):
        r = requests.get(f'http://{self.assigned_cr}/get_data/{device_id}/{sensor_id}?port={self.port}')
        print(f"subscriber received data {r.content}")


def join(sub1):
    time.sleep(5)
    sub1.join_network("http://localhost:8004")

    sub1.request_data('0', '0')

if __name__ == "__main__":
    # define the parser
    parser = argparse.ArgumentParser(
        description="Subscriber to network")

    # add arguments for host and port
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--sub_id", type=str, default="sub")
    parser.add_argument("--port", type=int, default=8005)

    sub = Subscriber(parser.parse_args().sub_id, parser.parse_args().port)
    app = fastapi.FastAPI()
    app.include_router(sub.router)

    print("registering subscriber")
    thread = threading.Thread(target=join, args=(sub,))
    thread.start()
    try:
        uvicorn.run(app, host=parser.parse_args().host,
                    port=parser.parse_args().port)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)
