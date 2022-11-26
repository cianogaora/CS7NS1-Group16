import uvicorn

import subscriber
import fastapi
from routes.contentrouter import RequestData
import time
import threading

def join(sub1):
    time.sleep(5)
    sub1.join_network("http://localhost:8004")

    sub1.request_data('0', '0')


if __name__ == "__main__":
    app = fastapi.FastAPI()
    port = 8005
    sub1 = subscriber.Subscriber("Cian", port)
    app.include_router(sub1.router)
    thread = threading.Thread(target=join, args=(sub1,))
    thread.start()
    try:
        uvicorn.run(app, host="localhost",
                    port=8005)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)

