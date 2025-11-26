import redis
import json

from dotenv import load_dotenv

load_dotenv()

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=os.getenv('REDIS_PORT', 6379),
            db=os.getenv('REDIS_DB', 0),
            decode_responses=True
        )

    def get_key(self, endpoint: str, params: dict):
        parts = [endpoint] + [f"{k}={v}" for k, v in sorted(params.items())]
        return ":".join(parts)

    def get(self, key: str):
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def set(self, key: str, value, ttl_seconds: int = 60):
        self.client.set(key, json.dumps(value), ex=ttl_seconds)
