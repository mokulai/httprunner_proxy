import os
import redis


class RedisConnect():

    def __init__(self):
        self.path = './data/'
        self.hostname = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.r = redis.StrictRedis(host=self.hostname, port=self.port, db=0, decode_responses=True)

    def str_getall(self):
        res = self.r.keys()
        if res:
            return res

    def str_get(self, k):
        res = self.r.get(k)
        if res:
            return res.decode()

    def str_set(self, k, v, time=None):
        self.r.set(k, v, time)

    def delete(self, k):
        tag = self.r.exists(k)
        if tag:
            self.r.delete(k)
            print('删除成功')
        else:
            print('这个key不存在')

    def hash_hget(self, name, key):
        res = self.r.hget(name, key)
        if res:
            return res

    def hash_hset(self, name, k, v):
        self.r.hset(name, k, v)

    def hash_getall(self, name):
        res = self.r.hgetall()
        new_dict = {}
        if res:
            for k, v in res.items():
                k = k.decode()
                v = v.decode()
                new_dict[k] = v
        return new_dict

    def hash_del(self, name,k):
        res = self.r.hdel(name, k)
        if res:
            print('删除成功')
            return True
        else:
            print('删除失败.该key不存在')
            return False

    def z_getall(self, k):
        res = self.r.zrange(k, 1, -1)
        if res:
            return res

    def z_set(self, k, n, v):
        mapping = {v: n}
        self.r.zadd(k, mapping)

    def clean_redis(self):
        self.r.flushdb()
        print('清空redis成功.')
        return 0


