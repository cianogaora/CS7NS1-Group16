# written by Christopher

ssh lohsec@rasp-033.berry.scss.tcd.ie   -o "StrictHostKeyChecking=no" pkill -9 -f contentrouter.py
ssh lohsec@rasp-032.berry.scss.tcd.ie  -o "StrictHostKeyChecking=no" pkill -9 -f contentrouter.py
ssh lohsec@rasp-040.berry.scss.tcd.ie  -o "StrictHostKeyChecking=no" pkill -9 -f controller.py
ssh lohsec@rasp-040.berry.scss.tcd.ie  -o "StrictHostKeyChecking=no" pkill -9 -f subscriber.py
ssh lohsec@rasp-033.berry.scss.tcd.ie -o "StrictHostKeyChecking=no" pkill -9 -f satellite.py