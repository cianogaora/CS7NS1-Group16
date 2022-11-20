from fastapi import APIRouter, Depends, HTTPException, status
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

        @self.router.get("/get_data")
        async def get_data(sensor_id, device_id) -> SensorData:

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
