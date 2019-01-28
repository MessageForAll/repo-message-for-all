import redis
connection = redis.StrictRedis(host='pav_redis', port=6379, 
                      password='', decode_responses=True)
connection.flushall()