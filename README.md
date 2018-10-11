# redis_mq

## 通过redis实现消息队列

### 基本思路

- 通过flask 建立一个web页面
- 点击事件，存储redis
- 生产消费模式
  - 队列名称：task:prodcons:queue
  - redis的lpush添加随机数，生产者生产随机数
  - redis的blpop，消费者消除随机数
- 发布订阅模式
  - 频道名称：task:pubsub:channel
  - redis的pubsub，创建发布订阅对象
  - pubsub.subscribe，订阅频道
  - pubsub.publish，向该频道发布消息

### 1. 提供一个页面作为生产者/消息发布者

- 建立flask和redis连接

  ```python
  import redis
  import random
  import logging
  from flask import Flask, redirect
  
  app = Flask(__name__)
  
  rcon = redis.StrictRedis(host='localhost', db=1)  #连接redis
  prodcons_queue = 'task:prodcons:queue'  #生产者消费者队列名称
  pubsub_channel = 'task:pubsub:channel' #发布订阅频道名称
  
  ```

- 提供页面

  ```python
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
  if __name__ == '__main__':
      app.run(debug=True)
  ```

### 2. 生产消费模式

- 生产者 

  ```python
  #生产者
  @app.route('/prodcons')
  def prodcons():
      elem = random.randrange(10)
      rcon.lpush(prodcons_queue, elem)
      logging.info("lpush {} -- {}".format(prodcons_queue, elem))
      return redirect('/')
  ```

- 消费者

  ```python
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
  ```
### 3. 发布订阅模式
- 发布者 

  ```python
  # 消息发布者
  @app.route('/pubsub')
  def pubsub():
      ps = rcon.pubsub()
      ps.subscribe(pubsub_channel)
      elem = random.randrange(10)
      rcon.publish(pubsub_channel, elem)
      return redirect('/')
  ```
- 订阅者 

  ```python
  # 订阅者
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
  if name == 'main':
      print ('监听任务频道')
      Task().listen_task()
  ```


