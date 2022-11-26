from routes.contentrouter import ContentRouter
from routes.contentrouter import SensorData
import fastapi
# imort argparse
import uvicorn
import os
import argparse
import json
import random
import controller
import subscriber

# define the parser
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

if __name__ == "__main__":
    app = fastapi.FastAPI()
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
    # device.join_network("http://localhost:8000")

