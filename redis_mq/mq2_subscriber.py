#coding:utf-8
"""
发布订阅模式中的订阅者
"""
import redis

class Task(object):

    def __init__(self):
        self.rcon = redis.StrictRedis(host='localhost')
        self.ps = self.rcon.pubsub()
        self.ps.subscribe('task:pubsub:channel')

    def listen_task(self):
        for i in self.ps.listen():
            if i['type'] == 'message':
                print ("Task get", i['data'])
if __name__ == '__main__':
    print ('监听任务频道')
    Task().listen_task()