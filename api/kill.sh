lsof -i :8000 | awk 'NR!=1 {print $2}' | xargs kill -9
lsof -i :8001 | awk 'NR!=1 {print $2}' | xargs kill -9
lsof -i :8002 | awk 'NR!=1 {print $2}' | xargs kill -9