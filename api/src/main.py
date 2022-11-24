
from routes.contentrouter import ContentRouter
import fastapi
# imort argparse
import uvicorn
import os
import argparse
import json
import random
import controller

# define the parser
parser = argparse.ArgumentParser(description='Run the API')
parser.add_argument('--host', type=str, help='Host to run the API on')
parser.add_argument('--port', type=int, help='Port to run the API on')
# add argumnt for device_dict and sensor_dict
parser.add_argument('--device_dict', type=str, help='Path to device_dict')
parser.add_argument('--sensor_dict', type=str, help='Path to sensor_dict')
# add argument for device_id
parser.add_argument('--device_id', type=str, help='Device ID')
# add argument for controller address
parser.add_argument('--controller_address', type=str,
                    help='Controller address')


# parse the arguments
args = parser.parse_args()


if __name__ == "__main__":
    app = fastapi.FastAPI()
    # get the device_dict and sensor_dict
    device_dict = json.load(open(args.device_dict))
    sensor_dict = json.load(open(args.sensor_dict))
    # random_number = random.randint(0, 100)

    # controller_node = controller.Controller()
    # app.include_router(controller_node.router)
    address = f"{args.host}:{args.port}"
    device = ContentRouter(f"device_id{args.device_id}",
                           address, sensor_dict, device_dict, controller_address=args.controller_address)
    app.include_router(device.router)

    uvicorn.run(app, host=args.host, port=args.port)
    device.join_network("http://localhost:8000")
    # handle keyboard interrupt
    try:
        uvicorn.run(app, host=args.host, port=args.port, n_jobs=1)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)
