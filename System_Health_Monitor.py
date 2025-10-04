import psutil
import logging
import time

# ----------------------------
# Configuration
# ----------------------------
CPU_THRESHOLD = 80        # in percent
MEMORY_THRESHOLD = 80     # in percent
DISK_THRESHOLD = 80       # in percent
PROCESS_THRESHOLD = 300   # max number of running processes
CHECK_INTERVAL = 5        # seconds between checks
LOG_FILE = "system_health.log"

# ----------------------------
# Logging Setup
# ----------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Monitoring Functions
# ----------------------------
def check_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        logging.warning(f"⚠️ High CPU usage detected: {cpu_usage}%")
        print(f"⚠️ High CPU usage detected: {cpu_usage}%")
    else:
        logging.info(f"CPU Usage: {cpu_usage}%")
    return cpu_usage

def check_memory():
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if memory_usage > MEMORY_THRESHOLD:
        logging.warning(f"⚠️ High Memory usage detected: {memory_usage}%")
        print(f"⚠️ High Memory usage detected: {memory_usage}%")
    else:
        logging.info(f"Memory Usage: {memory_usage}%")
    return memory_usage

def check_disk():
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    if disk_usage > DISK_THRESHOLD:
        logging.warning(f"⚠️ High Disk usage detected: {disk_usage}%")
        print(f"⚠️ High Disk usage detected: {disk_usage}%")
    else:
        logging.info(f"Disk Usage: {disk_usage}%")
    return disk_usage

def check_processes():
    num_processes = len(psutil.pids())
    if num_processes > PROCESS_THRESHOLD:
        logging.warning(f"⚠️ Too many running processes: {num_processes}")
        print(f"⚠️ Too many running processes: {num_processes}")
    else:
        logging.info(f"Running Processes: {num_processes}")
    return num_processes

# ----------------------------
# Main Monitoring Loop
# ----------------------------
def monitor_system():
    print("🔍 Starting System Health Monitor...")
    logging.info("System Health Monitoring Started")

    try:
        while True:
            check_cpu()
            check_memory()
            check_disk()
            check_processes()
            print("-" * 50)
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")
        logging.info("System Health Monitoring Stopped by User")

if __name__ == "__main__":
    monitor_system()
