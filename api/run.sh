# star dummy sensor
python src/dummy_sensor.py  &
# start the first content router

python src/main.py --host localhost --port 8001 --device_dict config/device_dict_1.json --sensor_dict config/sensor_dict_1.json &

# start the second content router

python src/main.py --host localhost --port 8002 --device_dict config/device_dict2.json --sensor_dict config/sensor_dict_2.json &


