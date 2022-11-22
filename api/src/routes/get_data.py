from fastapi import APIRouter, Depends, HTTPException, status, Request
import requests
# import basemodel
from pydantic import BaseModel


# def a model for the data in the request


class RequestData(BaseModel):
    device_id: str
    sensor_id: str


class SensorData(BaseModel):
    data: int
    timestamp: str


# temp dict to get the address of the content router from the device id


class Device:
    def __init__(self, device_id, address, sensor_dict, device_dict):
        self.device_id = device_id
        self.address = address
        self.sensor_dict = sensor_dict
        self.device_dict = device_dict
        self.router = APIRouter()

        # device id
        ## device addr
        self.fib = []

        # requester id, device id, sensor id
        self.pit = []

        # (device id, sensor id, sensor value)
        self.cs = []

        @self.router.get("/get_data")
        async def get_data(sensor_id, device_id, request: Request) -> SensorData:
            # Check content store
            for entry in self.cs:
                if all(x in entry for x in [device_id, sensor_id]):
                    data = entry[2]
                    return SensorData(data)

            # Check/Add to PIT
            requester = request.client.host
            req_in_pit = False
            for entry in self.pit:
                if all(x in entry for x in [requester, device_id, sensor_id]):
                    req_in_pit = True

            if not req_in_pit:
                self.pit.append((requester, device_id, sensor_id))

            self.fib = ["http://localhost:8000"]
            # Check PIT for unfulfilled requests
            for entry in self.pit:
                print(f"getting data for entry {entry}")
                src = entry[0]
                device = int(entry[1])
                sensor = entry[2]
                device_addr = self.fib[device]
                response = requests.get(device_addr + '/get_data', params={"sensor_id": sensor, "device_id": device})
                print(response.content)
                print("exiting the first request in pit")
                return response.json()
'''
            if sensor_id in self.sensor_dict:
                # request from sensor
                sensor_address = self.sensor_dict[sensor_id]["address"]
                response = requests.get(sensor_address + "/get_data")
                return response.json()

            else:
                # parse the requet to the content router
                content_router_address = self.device_dict["content_router"]
                response = requests.get(
                    content_router_address + "/get_data", params={"sensor_id": sensor_id, "device_id": device_id})

            reuest_url = self.device_dict["content_router"] + "/get_data"

            response = requests.get(
                reuest_url, params={"sensor_id": sensor_id, "device_id": device_id})
            # await response.json()
            return response.json()
            
            '''
