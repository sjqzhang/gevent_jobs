# gevent_jobs
### how to install?

```angular2html
pip  install -U gevent_jobs
```

### how to use?

```python
#import Job,JobQueue (导入 Job,JobQueue)
from gevent_jobs import Job,JobQueue

# define your job , must be implements `do` func ,return bool  (定义你的任务，继承Job类，必须实现 do 方法，返回 bool 类型)
# 成功时回调 success 方法，失败时回调 error 方法
class MyJob(Job):
    def do(self):
        self.data=self.job_id
        return True
    def success(self):
        print(self.data)
    def error(self):
        print(self.data)

# load_job second/per（每秒种加载一次任务）
def load(queue):
    job=MyJob()
    queue.put(job)
    
# load_job custom interval (recommend) (自定义加载任务间隔【推荐】)
def load(queue):
    import time
    while True:
        for i in range(1,100):
            job=MyJob()
            queue.put(job)
        time.sleep(60)


## JobQueue(load_job_func=None,worker_count=10,queue_size=100000,thread_mode='gevent') 
'''
load_job_func 加载任务函数，用户自定义，在加载函数中最好用 while True阻塞
worker_count 工作的协（线）程数量
queue_size 队列大小
thread_mode 线程模型 gevent|thread
'''

jobQueue=JobQueue(load_job_func=load)
jobQueue.start()
```