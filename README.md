# gevent_jobs


### how to use?

```python
class MyJob(Job):
    def do(self):
        self.data=self.job_id
        return True
    def success(self):
        print(self.data)

def load(queue):
    job=MyJob()
    queue.put(job)

jobQueue=JobQueue(load_job_func=load)
jobQueue.start()
```