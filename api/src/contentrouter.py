import argparse

import fastapi
import uvicorn
from fastapi import APIRouter, Depends, HTTPException, status, Request
import requests
# import basemodel

from pydantic import BaseModel
from threading import Thread
import time
import os
from typing import List, Union


class RegisterDevice(BaseModel):
    device_id: str
    sensor_ids: List[str] = None
    sensor_address: str = None
    device_address: str


class RegisterSubscriber(BaseModel):
    type: str
    sub_id: str


class RegisterContentRouter(BaseModel):
    content_router_id: str
    address: str


class RequestData(BaseModel):
    device_id: str
    sensor_id: str


class SensorData(BaseModel):
    data: int
    timestamp: str


class UpdateData(BaseModel):
    device_id: str
    next: str

    # temp dict to get the address of the content router from the device id


class UpdateBefore(BaseModel):
    device_address: str


class ContentRouter:
    def __init__(self, device_id, address, controller_address) -> None:
        self.device_id = device_id
        self.address = address
        self.controller_address = controller_address

        self.next = []
        self.before = []
        self.router = APIRouter()
        self.pit = []
        self.fib = []
        # device_id sensor_id sensor_data timestamp
        self.cs = []
        self.load_from_file()
        self.start()

        # spawn a thread to clean the cs

        @self.router.get("/get_data/{device_id}/{sensor_id}")
        async def get_data(device_id: str, sensor_id: str, request: Request,  port: int = None, last: str = None) -> SensorData:
            last = self.device_id
            print(
                f"get_data request from device {device_id} for sensor {sensor_id}")

            for entry in self.cs:
                if all(x in entry for x in [device_id, sensor_id]):
                    data = entry[2]
                    return data

            # get the address of the next content router
            for entry in self.fib:
                if device_id == entry[0]:
                    next = entry[1]
                    # send the request to the next content router
                    print(f"Sending request to {next}")
                    # check if http in next address
                    if "http" not in next:
                        next = "http://" + next
                    r = requests.get(
                        f"{next}/get_data/{device_id}/{sensor_id}")
                    # add to cs
                    self.cs.append(
                        (device_id, sensor_id, r.json(), time.time()))
                    return r.json()

            else:
                raise HTTPException(status_code=404, detail="Device not found")
            # Check/Add to PIT
            # requester = request.client.host
            # print(f"requester: {requester} port {port}")
            # req_in_pit = False
            # for entry in self.pit:
            #     if all(x in entry for x in [requester, device_id, sensor_id]):
            #         req_in_pit = True

            # if not req_in_pit:
            #     self.pit.append(
            #         (requester, port, device_id, sensor_id, time.time()))

            # # Check PIT for unfulfilled requests
            # responses = []
            # for entry in self.pit:
            #     print(f"getting data for entry {entry}")

            #     src = entry[0]
            #     entry_port = entry[1]
            #     device = entry[2]
            #     sensor = int(entry[3])
            #     timestamp = entry[4]
            #     device_addr = ""
            #     for d in self.fib:
            #         if str(d[0]) == str(entry[2]):
            #             device_addr = d[1]
            #     if device_addr == "":
            #         print("device not in fib")
            #         return HTTPException(status_code=404, detail="device not in fib")

            #     # check if addr contains http
            #     if "http" not in device_addr:
            #         device_addr = "http://" + device_addr

            #     response = requests.get(
            #         f"{device_addr}/get_data/{device}/{sensor}?port={entry_port}&last={last}")
            #     # check if bad response
            #     if response.status_code != 200:
            #         print("bad response")
            #         return HTTPException(status_code=404, detail="bad response")
            #     print(response.json())
            #     print(f"processing entry {entry} in pit")
            #     responses.append((src, entry_port, response.json()))

            # for r in responses:
            #     addr = r[0]
            #     if r[0] == "::1":
            #         addr = "localhost"
            #     print(f"sending response {r[2]} to {addr}")
            #     data = SensorData(**r[2])

            #     print(data)
            #     requests.post(
            #         url=f'http://{addr}:{r[1]}/response', data=data.json())

            # return {"response": "request sent"}

        @self.router.post("/update/before")
        def update_before(data: UpdateBefore) -> None:
            print("update before")
            # add to before
            self.before.append(data.device_address)

            print(f"before: {self.before}")
            #
            return {"status": "success"}

        @self.router.post("/update/fib")
        def update_fib(data: UpdateData) -> None:
            # check if device is in fib
            for entry in self.fib:
                if entry[0] == data.device_id:
                    return {"status": "already in fib"}

            self.fib.append((data.device_id, data.next))

            print(f"updating fib for {data.device_id}")
            # print the fib
            for before in self.before:
                url = f"http://{before}/update/fib"

                print(url)
                r = requests.post(
                    url, json={"device_id": data.device_id, "next": self.address})
                print(r.content)
            # same for next
            for next in self.next:
                url = f"http://{next}/update/fib"

                print(url)
                r = requests.post(
                    url, json={"device_id": data.device_id, "next": self.address})
                print(r.content)
            # return success
            return {"status": "success"}

        @self.router.post("/register/content_router")
        def register_content_router(registration_dict: RegisterContentRouter) -> None:
            # proxied request forwards the request to the controller node
            print("registering content router")
            r = requests.post(f"http://{self.controller_address}/register/content_router",
                              json=registration_dict)
            return {"status": "success"}

        @self.router.post("/register/device")
        def register_device(data: RegisterDevice) -> None:
            # proxied request forwards the request to the controller node
            print("registering device")
            r = requests.post(
                f"http://{self.controller_address}/register/device", json=data.dict())
            print(r.content)
            return {"status": "success"}

    def join_network(self, controller_addr):
        r = requests.post(controller_addr, params={"type": "join"})
        print(r.json())

    def clean_cs(self):
        while True:
            for i in range(len(self.cs)):
                # check the timestamp of the entry
                try:
                    if time.time() - self.cs[i][3] > 10:
                        # remove the entry
                        print("removing entry")
                        self.cs.pop(i)
                except IndexError:
                    pass
            time.sleep(5)

    def save_to_file(self):
        while True:
            with open(f"content_store_{self.device_id}.txt", "w") as f:
                f.write(str(self.cs))

            # same for fib and pit

            with open(f"fib_{self.device_id}.txt", "w") as f:
                f.write(str(self.fib))

            with open(f"pit_{self.device_id}.txt", "w") as f:
                f.write(str(self.pit))

            with open(f"before_{self.device_id}.txt", "w") as f:
                f.write(str(self.before))

            with open(f"next_{self.device_id}.txt", "w") as f:
                f.write(str(self.next))

            time.sleep(5)

    def load_from_file(self):
        # check if file exists
        try:
            with open(f"content_store_{self.device_id}.txt", "r") as f:
                self.cs = list(eval(f.read()))

        except FileNotFoundError:
            print("No content store file found")
            print("Creating new content store")
            self.cs = []
            self.cs.append((self.device_id, "sensor_1", 10, time.time()))

        try:
            with open(f"fib_{self.device_id}.txt", "r") as f:
                self.fib = eval(f.read())
        except FileNotFoundError:
            print("No fib file found")
            print("Creating new fib")
            self.fib = []
        # try to open before file
        try:
            with open(f"before_{self.device_id}.txt", "r") as f:
                self.before = eval(f.read())
        except FileNotFoundError:
            print("No before file found")
            print("Creating new before")
            self.before = []
        # same for next
        try:
            with open(f"next_{self.device_id}.txt", "r") as f:
                self.next = eval(f.read())
        except FileNotFoundError:
            print("No next file found")
            print("Creating new next")
            self.next = []
        # try to open device dict{id}.json
        try:
            with open(f"before_{self.device_id}.txt", "r") as f:
                self.before = eval(f.read())
        except FileNotFoundError:
            print("No before file found")
            print("Creating new before")
            # register content router
            self.register_content_router()

    def start(self):
        t = Thread(target=self.clean_cs)
        t.start()

        t_2 = Thread(target=self.save_to_file)
        t_2.start()

        print("starting content router")

    def register_content_router(self):
        # register the content router with the controller
        registration = RegisterContentRouter(
            content_router_id=self.device_id, address=self.address)
        r = requests.post(f"http://{self.controller_address}/register/content_router",
                          json=registration.dict())
        # check if bad request
        if r.status_code == 400:
            # print message
            print(r.json())
        else:

            # send update to next if not []

            if r.json()["next"] == None:
                print("I am the last content router")
            else:
                self.next.append(r.json()["next"])
                print(f"next is {self.next}")
                # print own address
                print(f"address is {self.address}")

                url = f"http://{self.next[-1]}/update/before"
                try:
                    r = requests.post(
                        url, json={"device_address": self.address})

                except requests.exceptions.ConnectionError:
                    print("Next content router is not ready yet")
                    time.sleep(5)
                    r = requests.post(
                        url, json={"device_address": self.address})



if __name__ == "__main__":
    app = fastapi.FastAPI()

    parser = argparse.ArgumentParser(description='Run the API')
    parser.add_argument('--host', type=str, help='Host to run the API on')
    parser.add_argument('--port', type=int, help='Port to run the API on')
    # add argument for device_id
    parser.add_argument('--device_id', type=str, help='Device ID')
    # add argument for controller address
    parser.add_argument('--controller_address', type=str,
                        help='Controller address')

    # parse the arguments
    args = parser.parse_args()
    # get the device_dict and sensor_dict

    # random_number = random.randint(0, 100)

    # controller_node = controller.Controller()
    # app.include_router(controller_node.router)
    address = f"{args.host}:{args.port}"
    device = ContentRouter(f"device_id{args.device_id}",
                           address, controller_address=args.controller_address)
    app.include_router(device.router)

    # uvicorn.run(app, host=args.host, port=args.port)

    # handle keyboard interrupt
    try:
        uvicorn.run(app, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)