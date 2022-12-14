# Written by Christopher 

ssh username@rasp-040.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/controller.py  --host 10.35.70.40 --port 33004 &" &


# wait a few seconds for controller to start
sleep 5
# start the first content router on pi 32
ssh username@rasp-032.berry.scss.tcd.ie  -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/contentrouter.py --host 10.35.70.32 --port 33005  --device_id 1 --controller_address 10.35.70.40:33004 &" &


# start the second content router on pi 33

ssh username@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/contentrouter.py --host 10.35.70.33 --port 33006  --device_id 2 --controller_address 10.35.70.40:33004 &" &

sleep 3 

# start 5 Satellites on pi 33 
# first satellite
ssh username@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/satellite.py --host 10.35.70.33 --pub_id 0 --port 33007 --controller_address 10.35.70.40 --controller_port 33004 &" &
# second satellite
ssh username@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/satellite.py --host 10.35.70.33 --pub_id 1 --port 33008 --controller_address 10.35.70.40 --controller_port 33004 &" &
# third satellite
ssh username@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/satellite.py --host 10.35.70.33 --pub_id 2 --port 33009 --controller_address 10.35.70.40 --controller_port 33004 &" &

# fourth satellite
ssh username@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/satellite.py --host 10.35.70.33 --pub_id 3 --port 33010 --controller_address 10.35.70.40 --controller_port 33004 &" &

# fifth satellite
ssh username@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/satellite.py --host 10.35.70.33 --pub_id 4 --port 33011 --controller_address 10.35.70.40 --controller_port 33004 &" &

# start subscriber on pi 41

ssh username@rasp-040.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" "export http_proxy= && cd project3/CS7NS1-Group16-content_router/api/  && python3 src/subscriber.py --host  10.35.70.40 --sub_id 'cian' --port 33012 --controller_addr 10.35.70.40:33004 &" &
