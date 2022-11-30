# written by Cian and Christopher

# star dummy sensor
#python3 src/dummy_sensor.py  &

python3 src/controller.py  --host localhost --port 8004 &
# wait a few seconds for controller to start
sleep 5
# start the first content router

python3 src/contentrouter.py --host localhost --port 8001  --device_id 1 --controller_address localhost:8004 &

# start the second content router

python3 src/contentrouter.py --host localhost --port 8002  --device_id 2 --controller_address localhost:8004 &

sleep 3
# first satellite
python3 src/satellite.py --host localhost --pub_id 0 --port 8006  --controller_address localhost --controller_port 8004 &

# second satellite
python3 src/satellite.py --host localhost --pub_id 1 --port 8007  --controller_address localhost --controller_port 8004 &
# third satellite
python3 src/satellite.py --host localhost --pub_id 2 --port 8008  --controller_address localhost --controller_port 8004 &
# fourth satellite
python3 src/satellite.py --host localhost --pub_id 3 --port 8009  --controller_address localhost --controller_port 8004 &
# fifth satellite
python3 src/satellite.py --host localhost --pub_id 4 --port 8010  --controller_address localhost --controller_port 8004 &
# start subscriber


python3 src/subscriber.py --host localhost --sub_id "cian" --port 8005


