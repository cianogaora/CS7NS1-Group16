
from routes.get_data import Device
import fastapi
# imort argparse
import uvicorn
import os
import argparse
import json


# define the parser
parser = argparse.ArgumentParser(description='Run the API')
parser.add_argument('--host', type=str, help='Host to run the API on')
parser.add_argument('--port', type=int, help='Port to run the API on')
# add argumnt for device_dict and sensor_dict
parser.add_argument('--device_dict', type=str, help='Path to device_dict')
parser.add_argument('--sensor_dict', type=str, help='Path to sensor_dict')


# parse the arguments
args = parser.parse_args()


if __name__ == "__main__":
    app = fastapi.FastAPI()
    # get the device_dict and sensor_dict
    device_dict = json.load(open(args.device_dict))
    sensor_dict = json.load(open(args.sensor_dict))
    device = Device("device_id", "address", sensor_dict, device_dict)
    app.include_router(device.router)
    uvicorn.run(app, host=args.host, port=args.port)

    # handle keyboard interrupt
    try:
        uvicorn.run(app, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)
