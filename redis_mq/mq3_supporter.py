# coding:utf-8
"""
提供一个页面作为生产者/消息发布者
"""
import redis
import random
import logging
from flask import Flask, redirect

app = Flask(__name__)

rcon = redis.StrictRedis(host='localhost', db=1)
prodcons_queue = 'task:prodcons:queue'  #生产者消费者队列名称
pubsub_channel = 'task:pubsub:channel' #发布订阅频道名称

@app.route('/')
def index():

    html = """
<br>
<center><h3>Redis Message Queue</h3>
<br>
<a href="/prodcons">生产消费者模式</a>
<br>
<br>
<a href="/pubsub">发布订阅者模式</a>
</center>
"""
    return html

#生产者
@app.route('/prodcons')
def prodcons():
    elem = random.randrange(10)
    rcon.lpush(prodcons_queue, elem)
    logging.info("lpush {} -- {}".format(prodcons_queue, elem))
    return redirect('/')
#消息发布者
@app.route('/pubsub')
def pubsub():
    ps = rcon.pubsub()
    ps.subscribe(pubsub_channel)
    elem = random.randrange(10)
    rcon.publish(pubsub_channel, elem)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)