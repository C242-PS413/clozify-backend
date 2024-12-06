import redis
import json

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def get(self, key):
        data = self.redis_client.get(key)
        if data:
            return json.loads(data.decode('utf-8')) 
        return None

    def set(self, key, value, ttl=3600):
        self.redis_client.setex(key, ttl, json.dumps(value))

    def delete(self, key):
        self.redis_client.delete(key)
