import json
import time
import random
from datetime import datetime

SERVICES = ["auth-service", "payment-service", "orders-service"]
LEVELS = ["INFO", "WARN", "ERROR"]

LOG_PATH = "logs/services.log"

def generate_log():
    service = random.choice(SERVICES)
    level = random.choice(LEVELS)
    msg = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": service,
        "level": level,
        "message": f"Sample log from {service}",
        "metadata": {
            "request_id": f"req-{random.randint(1000, 9999)}",
            "user_id": random.randint(1, 100),
        },
    }
    return msg

def main():
    print(f"Writing logs to {LOG_PATH} ... (Ctrl+C to stop)")
    while True:
        log = generate_log()
        line = json.dumps(log)
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
        time.sleep(1)

if __name__ == "__main__":
    main()

