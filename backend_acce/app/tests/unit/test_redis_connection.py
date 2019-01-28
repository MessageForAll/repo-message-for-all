import unittest

from app.main.model.redis_connection import RedisConnection

class TestRedisConnection(unittest.TestCase):
    redis = RedisConnection()
    redis_conect = redis.connect()

    def tearDown(self):
        self.redis_conect.delete("unit_test")

    def test_connect(self):
        self.assertTrue(self.redis_conect.set("unit_test", "redis_connection"))
