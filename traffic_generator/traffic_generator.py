import random, time, requests, os
BASE = os.getenv("BASE_URL", "http://demo_app:8000")

while True:
    try:
        path = "/error" if random.random() < 0.2 else "/ping"
        requests.get(BASE + path, timeout=2)
    except Exception:
        pass
    time.sleep(1)          # 1 req/s