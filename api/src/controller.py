from fastapi import FastAPI, APIRouter, HTTPException, status, Query, Request
import requests
from pydantic import BaseModel
from typing import List, Union
import uvicorn
# import threading
from threading import Thread
import json
import time
import argparse

import logging
# set up logging to info
logging.basicConfig(level=logging.INFO)


from routes.contentrouter import RegisterSubscriber, RegisterDevice, RegisterContentRouter


class Controller:
    def __init__(self) -> None:

        self.router = APIRouter()
        # load content router dict
        self.load_content_router_dict()
        # start thread to save content router dict
        thread = Thread(target=self.save_content_router_dict)
        thread.start()

        @self.router.post("/register/device")
        async def register_device(device: RegisterDevice, request: Request) -> None:
            # check if the device is already in the content router dict
            for cs in self.content_router_dict:
                if device.device_id in self.content_router_dict[cs]["devices"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail="Device already registered")

            print(self.content_router_dict)

            # get the content router with the least devices in its device list
            content_router = min(self.content_router_dict, key=lambda x: len(
                self.content_router_dict[x]["devices"]))

            # add the device to the content router
            self.content_router_dict[content_router]["devices"].append(
                device.device_id)

            self.brodcast_register(content_router, device)

            # # return 200 OK
            return {"message": "Device registered"}

        @ self.router.post("/register/content_router")
        async def register_content_router(content_router: RegisterContentRouter, request: Request) -> None:

            # check if the content router is already in the dict
            if content_router.content_router_id in self.content_router_dict:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Content router already registered")
            # check if content_router dict is empty
            if self.content_router_dict == {}:  # empty
                print("empty")
                # add the content router to the dict
                self.content_router_dict[content_router.content_router_id] = {
                    "devices": [], "address": content_router.address}
                logging.info(
                    f"Content router {content_router.content_router_id} registered")

                # return 200 OK
                return {"message": "Content router registered", "next": None}

            # find the content router that has the highest number of devices
            next_ = max(self.content_router_dict, key=lambda x: len(
                self.content_router_dict[x]["devices"]))

            # get the address of nexxt_
            next_address = self.content_router_dict[next_]["address"]

            # print(f"next address: {next_address}")

            # add content router to content router table
            self.content_router_dict[content_router.content_router_id] = {
                "address": content_router.address, "devices": []}

            logging.info(f"content router dict: {self.content_router_dict}")
            # return 200 OK
            return {"message": "Content router registered", "next": next_address}

        @self.router.get("/register/subscriber")
        async def register_sub():
            content_router = min(self.content_router_dict, key=lambda x: len(
                self.content_router_dict[x]["devices"]))
            return self.content_router_dict[content_router]["address"]


    def brodcast_register(self, content_router, device) -> None:
        # todo send request to content router

        for cs in self.content_router_dict:
            address = self.content_router_dict[cs]["address"]
            # add http:// to address
            # change device
            # check if the content router is in the dict
            if cs == content_router:

                print("same")

                requests.post(
                    f"http://{address}/update/fib", json={"device_id": device.device_id, "next": device.device_address})

        return 0

    def load_content_router_dict(self):
        try:
            with open("content_router_dict.json", "r") as f:
                self.content_router_dict = json.load(f)
                print(self.content_router_dict)
        except FileNotFoundError:
            self.content_router_dict = {}

    def save_content_router_dict(self):
        while True:
            with open("content_router_dict.json", "w") as f:
                print(self.content_router_dict)
                print("saving")
                json.dump(self.content_router_dict, f)
            time.sleep(5)


if __name__ == "__main__":
    # define the parser
    parser = argparse.ArgumentParser(
        description="Controller for the content router")

    # add arguments for host and port
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8004)

    controller = Controller()
    app = FastAPI()
    app.include_router(controller.router)

    print("starting controller")

    try:
        uvicorn.run(app, host=parser.parse_args().host,
                    port=parser.parse_args().port)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)

# device1/get_data/temperature
# device1/get_data/humidity


# get_data/device1/temp
