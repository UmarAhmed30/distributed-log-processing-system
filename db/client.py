import os
import clickhouse_connect

from dotenv import load_dotenv

load_dotenv()

client = clickhouse_connect.get_client(
    host = os.getenv('CLICKHOUSE_HOST', 'localhost'),
    port = os.getenv('CLICKHOUSE_HTTP_PORT', 8120),
    username = os.getenv('CLICKHOUSE_USER', 'logs_user'),
    password = os.getenv('CLICKHOUSE_PASSWORD', 'logs_pass'),
    database = os.getenv('CLICKHOUSE_DB', 'logs_db')
)

def main():
    try:
        client.command('SELECT 1')
        print("Connection to ClickHouse established successfully.")
    except Exception as e:
        print(f"Failed to connect to ClickHouse: {e}")

if __name__ == "__main__":
    main()