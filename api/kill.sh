# written by Christopher enjoy with care this kills all python processes on your machine and everything else that is running on port 8000-8006  

lsof -i :8000 | awk 'NR!=1 {print $2}' | xargs kill -9
lsof -i :8001 | awk 'NR!=1 {print $2}' | xargs kill -9
lsof -i :8002 | awk 'NR!=1 {print $2}' | xargs kill -9
lsof -i :8004 | awk 'NR!=1 {print $2}' | xargs kill -9
lsof -i :8005 | awk 'NR!=1 {print $2}' | xargs kill -9
# kill python threads
ps -ef | grep python | awk '{print $2}' | xargs kill -9
