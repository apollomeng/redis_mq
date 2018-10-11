#coding:utf-8
# 要使用了redis提供的blpop获取队列数据，如果队列没有数据则阻塞等待，也就是监听。
"""
生产者-消费者模式中的消费者
"""
import redis

class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(host='localhost', db=1)
        self.queue = 'task:prodcons:queue'

    def listen_task(self):
        while True:
            task = self.rcon.blpop(self.queue, 0)[1]
            print ("Task get", task)

if __name__ == '__main__':
    print ('监听任务队列')
    Task().listen_task()