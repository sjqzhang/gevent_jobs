# gevent_jobs
### how to install?

```angular2html
pip  install -U gevent_jobs
```

### how to use?

```python
# define your job , must be implements `do` func ,return bool  (定义你的任务，必须实现 do 方法，返回 bool 类型)
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

jobQueue=JobQueue(load_job_func=load)
jobQueue.start()
```