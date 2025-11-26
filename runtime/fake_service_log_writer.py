import json
import time
import random
from datetime import datetime

SERVICES = ["auth-service", "payment-service", "orders-service", "inventory-service", "notification-service"]
LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]
HOSTS = ["worker-node-01", "worker-node-02", "worker-node-03", "api-gateway-01"]
HOST_IPS = {
    "worker-node-01": ["192.168.1.15", "10.0.0.5"],
    "worker-node-02": ["192.168.1.16", "10.0.0.6"],
    "worker-node-03": ["192.168.1.17", "10.0.0.7"],
    "api-gateway-01": ["192.168.1.10", "10.0.0.2"]
}

MESSAGES = {
    "ERROR": [
        "Transaction failed due to timeout connecting to database.",
        "Failed to authenticate user - invalid credentials.",
        "Connection refused to external API endpoint.",
        "Memory allocation failed - insufficient resources.",
        "Database query timeout after 30 seconds."
    ],
    "WARN": [
        "Response time exceeded threshold of 2 seconds.",
        "Retry attempt 3 of 5 for external service call.",
        "Cache miss rate exceeding 80% threshold.",
        "Queue size approaching maximum capacity.",
        "Deprecated API endpoint accessed."
    ],
    "INFO": [
        "Request processed successfully.",
        "User authentication completed.",
        "Payment transaction completed successfully.",
        "New order created and queued for processing.",
        "Cache refreshed successfully."
    ],
    "DEBUG": [
        "Entering method processRequest with params.",
        "Database connection pool status: 5/10 active.",
        "Cache lookup for key user_123.",
        "Parsing request body for validation.",
        "Response serialization completed."
    ]
}

LOG_PATH = "logs/services.log"

def generate_log():
    service = random.choice(SERVICES)
    level = random.choice(LEVELS)
    host = random.choice(HOSTS)
    
    log = {
        "@timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "log": {
            "level": level,
            "file": {
                "path": f"/var/log/{service}/app.log"
            }
        },
        "service": {
            "type": "application",
            "name": service
        },
        "host": {
            "name": host,
            "ip": HOST_IPS[host]
        },
        "message": random.choice(MESSAGES[level]),
        "trace_id": ''.join(random.choices('abcdef0123456789', k=12)),
        "span_id": ''.join(random.choices('0123456789', k=10))
    }
    return log

def main():
    print(f"Writing logs to {LOG_PATH} ... (Ctrl+C to stop)")
    while True:
        log = generate_log()
        line = json.dumps(log)
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
        print(f"[{log['log']['level']}] {log['service']['name']}: {log['message']}")
        time.sleep(1)

if __name__ == "__main__":
    main()
