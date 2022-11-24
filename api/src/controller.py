from fastapi import FastAPI, APIRouter, HTTPException, status, Query, Request

import requests


# import basemodel
from pydantic import BaseModel
from typing import List, Union
import uvicorn


class RegisterDevice(BaseModel):
    device_id: str
    sensor_ids: List[str]
    sensor_address: str
    device_address: str


class Controller:
    def __init__(self) -> None:

        self.router = APIRouter()

        #self.content_router_dict = {}

        self.device_dict = {}

        self.content_router_dict = {"content_router1": {
            "devices": ["device1", "device2", "device3"], "address": "localhost:8001"},
            "content_router2": {
            "devices": ["device4", "device5", "device6"], "address": "localhost:8002"}}

        @self.router.post("/register/device")
        async def register_device(device: RegisterDevice, request: Request) -> None:
            # dummy content router dict

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

            self.brodcast_register(content_router, device)

            # return 200 OK
            return {"message": "Device registered"}

    def brodcast_register(self, content_router, device) -> None:
        # todo send request to content router

        for cs in self.content_router_dict:
            address = self.content_router_dict[cs]["address"]
            # check if the content router is in the dict
            if cs == content_router:

                requests.post(
                    f"http://{address}/update/fib", json={"device_id": device.device_id, "next": self.device_dict[device.device_id]["address"]})
            else:
                requests.post(
                    f"http://{address}/update/fib", json={"device_id": device.device_id, "next": content_router})

        return 0


if __name__ == "__main__":
    controller = Controller()
    app = FastAPI()
    app.include_router(controller.router)

    print("starting controller")

    uvicorn.run(app, host="localhost", port=8004)
