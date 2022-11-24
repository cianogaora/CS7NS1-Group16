from fastapi import APIRouter, Depends, HTTPException, status, Request
import requests
# import basemodel
import controller
from pydantic import BaseModel
from threading import Thread
import time
# def a model for the data in the request


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


class ContentRouter:
    def __init__(self, device_id, address, sensor_dict, device_dict):
        self.device_id = device_id
        self.address = address
        self.sensor_dict = sensor_dict
        self.device_dict = device_dict
        self.router = APIRouter()

        # device id
        # device addr
        self.fib = []

        # requester id, device id, sensor id
        self.pit = []

        # (device id, sensor id, sensor value, timestamp)

        self.cs = []
        # dummy data timestamp in datetime format
        self.cs.append((self.device_id, "sensor1", 1, time.time()))
        # spawn a thread to clean the cs
        t = Thread(target=self.clean_cs)
        t.start()

        t_2 = Thread(target=self.save_to_file)
        t_2.start()

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
                response = requests.get(
                    device_addr + '/get_data', params={"sensor_id": sensor, "device_id": device})
                print(response.content)
                print("exiting the first request in pit")
                return response.json()

        @self.router.post("/update/fib")
        def update_pit(data: UpdateData) -> None:
            # add to fib
            self.fib.append((data.device_id, data.next))

            print(f"updating fib for {data.device_id}")
            # print the fib
            print(self.fib)

            # return success
            return {"status": "success"}

    def join_network(self, controller_addr):
        r = requests.post(controller_addr, params={"type": "join"})
        print(r.json())

    def clean_cs(self):
        while True:
            for i in range(len(self.cs)):
                if time.time() - self.cs[i][3] > 10:
                    print(f"deleting {self.cs[i]}")
                    self.cs.pop(i)
            # write to file
            # print(f"Writing to file")
            # with open(f"content_store_{self.device_id}.txt", "w") as f:
            #     f.write(str(self.cs))
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

            time.sleep(5)

    def load_from_file(self):
        # check if file exists
        try:
            with open(f"content_store_{self.device_id}.txt", "r") as f:
                self.cs = eval(f.read())
        except FileNotFoundError:
            print("No content store file found")
            print("Creating new content store")

        try:
            with open(f"fib_{self.device_id}.txt", "r") as f:
                self.fib = eval(f.read())
        except FileNotFoundError:
            print("No fib file found")
            print("Creating new fib")

        try:
            with open(f"pit_{self.device_id}.txt", "r") as f:
                self
        except FileNotFoundError:
            print("No pit file found")
            print("Creating new pit")


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
