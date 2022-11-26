# star dummy sensor
python3 src/dummy_sensor.py  &

python3 src/controller.py  --host localhost --port 8004 &
# wait a few seconds for controller to start
sleep 5
# start the first content router

python3 src/main.py --host localhost --port 8001  --device_id 1 --controller_address localhost:8004 &

# start the second content router

python3 src/main.py --host localhost --port 8002  --device_id 2 --controller_address localhost:8004 &

python3 src/subscriber.py --host localhost --sub_id "cian" --port 8005


