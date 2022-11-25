from fastapi import APIRouter, Depends, HTTPException, status, Request
import requests
# import basemodel
import controller
from pydantic import BaseModel
from threading import Thread
import time
import os
from controller import RegisterContentRouter, RegisterDevice


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

        self.load_from_file()
        self.start()

        self.pit = []

        @self.router.get("/get_data/{device_id}/{sensor_id}")
        async def get_data(device_id: str, sensor_id: str, request: Request) -> SensorData:

            print(f"get_data request from {device_id} for {sensor_id}")

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

            # Check FIB
            for entry in self.fib:
                if entry[0] == device_id:
                    # send request to next
                    print("sending request to next")
                    r = requests.get(
                        f"{entry[1]}/get_data/{device_id}/{sensor_id}")
                    return r.json()
            # Check PIT for unfulfilled requests
            for entry in self.pit:
                print(f"getting data for entry {entry}")
                src = entry[0]
                device = int(entry[1])
                sensor = entry[2]
                device_addr = self.fib[device]
                # check if addr contains http
                if "http" not in device_addr:
                    device_addr = "http://" + device_addr
                response = requests.get(
                    f"{device_addr}/get_data/{device}/{sensor}")
                print(response.content)
                print("exiting the first request in pit")
                return response.json()

        @ self.router.post("/update/before")
        def update_before(data: UpdateBefore) -> None:
            print("update before")
            # add to before
            self.before.append(data.device_address)

            print(f"before: {self.before}")
            #
            return {"status": "success"}

        @ self.router.post("/update/fib")
        def update_fib(data: UpdateData) -> None:
            # check if if device is in fib
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
                # appen dummy data
                self.cs.append((self.device_id, "sensor_1", 10, time.time()))
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
