from config import load_servers
from server_checker import check_server
from utils import format_result, send_alert

from concurrent.futures import ThreadPoolExecutor
import threading

print("PROGRAM STARTED")

servers = load_servers()

failed_services = []

lock = threading.Lock()


def run_check(url):
    result = check_server(url)

    print(format_result(result))

    if result["status"] in ["DOWN", "TIMEOUT"]:
        with lock:
            failed_services.append(url)


with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(run_check, servers)

print("\nFailed services:", ", ".join(failed_services))

send_alert(failed_services)