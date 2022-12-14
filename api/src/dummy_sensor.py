import fastapi
import random
import uvicorn
import time
from pydantic import BaseModel

#### Just a Testing Module ####
app = fastapi.FastAPI()

# define a route which listens to every request on the root path "/"
# define sensor_data model


class SensorData(BaseModel):
    data: int
    timestamp: str


@app.get("/get_data/{device_id}/{sensor_id}")
async def get_data(device_id: str, sensor_id: str,  port: int = None, last: str = None) -> SensorData:
    # generate a random number
    data = random.randint(0, 100)
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    # build SensorData object
    sensor_data = SensorData(data=data, timestamp=timestamp)
    return sensor_data


# run the API on the local machine on port 8000

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="localhost", port=8000)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)
