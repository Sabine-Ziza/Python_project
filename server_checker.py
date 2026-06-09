import requests
import time

session = requests.Session()


def check_server(url):
    for attempt in range(2):  # retry twice
        try:
            start = time.time()
            response = session.get(url, timeout=5)

            end = time.time()
            response_time = int((end - start) * 1000)
            status = "OK"

            if response.status_code >= 400:
                status = "DOWN"
            elif response_time > 500:
                status = "SLOW"

            try:
                data = response.json()
                if data.get("status") == "ok":
                    status = "OK"
            except:
                pass

            return {
                "url": url,
                "status_code": response.status_code,
                "response_time": response_time,
                "status": status
            }

        except requests.exceptions.RequestException:
            if attempt == 1:
                return {
                    "url": url,
                    "status_code": None,
                    "response_time": None,
                    "status": "TIMEOUT"
                }
