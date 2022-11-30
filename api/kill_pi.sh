# written by Christopher

ssh username@rasp-033.berry.scss.tcd.ie   -o "StrictHostKeyChecking=no" pkill -9 -f contentrouter.py
ssh username@rasp-032.berry.scss.tcd.ie  -o "StrictHostKeyChecking=no" pkill -9 -f contentrouter.py
ssh username@rasp-040.berry.scss.tcd.ie  -o "StrictHostKeyChecking=no" pkill -9 -f controller.py
ssh username@rasp-040.berry.scss.tcd.ie  -o "StrictHostKeyChecking=no" pkill -9 -f subscriber.py
ssh username@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" pkill -9 -f satellite.py