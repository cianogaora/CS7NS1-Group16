# star dummy sensor
python3 src/dummy_sensor.py  &

python3 src/controller.py &
# wait a few seconds for controller to start
sleep 5
# start the first content router

python3 src/main.py --host localhost --port 8001 --device_dict config/device_dict_1.json --sensor_dict config/sensor_dict_1.json  --device_id 1 --controller_address localhost:8004 &

# start the second content router

python3 src/main.py --host localhost --port 8002 --device_dict config/device_dict2.json --sensor_dict config/sensor_dict_2.json  --device_id 2 --controller_address localhost:8004 &


