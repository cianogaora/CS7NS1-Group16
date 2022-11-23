from fastapi import FastAPI, APIRouter, HTTPException, status, Query, Request

import requests


# import basemodel
from pydantic import BaseModel
from typing import List, Union


class RegisterDevice(BaseModel):
    device_id: str
    sensor_ids: List[str]
    sensor_address: str
    device_address: str


class Controller:
    def __init__(self) -> None:

        self.router = APIRouter()

        self.initialise_routes()

        self.app = FastAPI()

        self.app.include_router(self.router)

        self.content_router_dict = {}

        self.device_dict = {}

        self.router.post("/register/device")

        async def register_device(device: RegisterDevice, request: Request) -> None:
            # dummy content router dict
            self.content_router_dict = {"content_router1": {
                "devices": ["device1", "device2", "device3"], "address": "localhost:8000"},
                "content_router2": {
                    "devices": ["device4", "device5", "device6"], "address": "localhost:8001"}},
            # get the requester address
            requester = request.client.host
            # get the port
            port = request.client.port
            # find the content router that has the least number of devices
            content_router = min(self.content_router_dict, key=lambda x: len(
                self.content_router_dict[x]["devices"]))
            # add the device to the content router
            self.content_router_dict[content_router]["devices"].append(
                device.device_id)

            # add device to device table
            self.device_dict[device.device_id] = {
                "address": f"{requester}:{port}", "content_router": content_router}

            await self.brodcast_register(content_router, device)

            # return 200 OK
            return {"message": "Device registered"}

    def brodcast_register(self, content_router, device) -> None:
        # todo send request to content router

        for cs in self.content_router_dict:
            # check if the content router is in the dict
            if cs == content_router:
                requests.post(
                    f"http://{content_router}/update/pit", json=self.device_dict)
            else:
                requests.post(
                    f"http://{content_router}/update/pit", json={"device_id": device.device_id, "content_router": content_router})

            return 0
