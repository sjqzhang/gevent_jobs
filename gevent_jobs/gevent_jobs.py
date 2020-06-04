#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaozhang'
try:
    from queue import Queue
except Exception as er:
    from Queue import Queue
import time
import uuid
from enum import Enum
import logging
import threading



logger = logging.getLogger('JobQueue')

class JobStatus(Enum):
    Unkown='unkown'
    Success='success'
    Fail='fail'
    Runing='running'
    Init='init'
    Finish='finish'

class Job(object):
    def __init__(self):
        self.data=None
        self.input=None
        self.output=None
        self.job_id=str(uuid.uuid4())
        self.job_status=JobStatus.Init
    def job_switch(self):
        time.sleep(0.001)
    def error(self):
        pass
    def success(self):
        pass
    def do(self):
        raise Exception('must implements do function')


class JobQueue(object):
    '''
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

    '''
    class Status(object):
        INIT=0
        RUNNING=1
        STOP=2
        PAUSE=3
    def __init__(self,load_job_func=None,worker_count=10,queue_size=100000,thread_mode='gevent'):
        self.status=self.Status.INIT
        self.job_queue=Queue(queue_size)
        self.job_queue_error=Queue(queue_size)
        self.job_queue_success=Queue(queue_size)
        self.worker_count=worker_count
        self.load_job_func=load_job_func
        self.thread_mode=thread_mode

    def _add_job(self,job):
        if not hasattr(job, 'do'):
            logger.error('job must be implements do function')
            return False
        self.job_queue.put(job)
        return True

    def put(self,job):
        return self._add_job(job)

    def _load_job(self):
        while True:
            try:
                if callable(self.load_job_func) and self.job_queue.qsize()==0 and self.status==self.Status.RUNNING:
                    jobs=self.load_job_func(self)
                    if jobs!=None and isinstance(jobs,list):
                        for job in jobs:
                            if self._add_job(jobs):
                                logger.info('add job fail')
                time.sleep(1)
            except Exception as er:
                logger.error(er)

    def do_success(self):
        while True:
            try:
                job=self.job_queue_success.get()
                if hasattr(job, 'success') and callable(job.success):
                    job.success()
                else:
                    logger.info('please implements success funcion')
                time.sleep(0.001)
            except Exception as er:
                logger.error(er)
    def do_error(self):
        while True:
            try:
                job=self.job_queue_error.get()
                if hasattr(job, 'error') and callable(job.error):
                    job.error()
                else:
                    logger.info('please implements error funcion')
                time.sleep(0.001)
            except Exception as er:
                logger.error(er)

    def do(self):
        while True:
            try:
                if self.status==self.Status.PAUSE:
                    time.sleep(0.2)
                    continue
                if self.status==self.Status.STOP:
                    break
                job=self.job_queue.get()
                if not hasattr(job,'do'):
                    logger.error('job must be implements do function')
                    continue
                try:
                    result=job.do()
                    job.job_status=JobStatus.Finish
                except Exception as er:
                    logger.error(er)
                    job.job_status = JobStatus.Fail
                    result=False
                if result==None or result:
                    self.job_queue_success.put(job)
                else:
                    self.job_queue_error.put(job)
                time.sleep(0.001)
            except Exception as er:
                logger.error(er)

    def _start_gevent(self):
        try:
            from gevent import monkey
            monkey.patch_all()
            import gevent
            def nohup():
                while True:
                    time.sleep(100)
            self.status=self.Status.RUNNING
            workers=[]
            workers.append(gevent.spawn(nohup))
            time.sleep(0.02)
            workers.append(gevent.spawn(self.do_success))
            workers.append(gevent.spawn(self._load_job))
            workers.append(gevent.spawn(self.do_error))
            for i in range(1,self.worker_count):
                workers.append(gevent.spawn(self.do))
            gevent.joinall(workers)
        except Exception as er:
            logger.info('using threading mode')
            logger.error(er)
            self._start_thread()

    def _start_thread(self):
        import threading
        def nohup():
            while True:
                time.sleep(100)
        self.status=self.Status.RUNNING
        workers=[]
        workers.append(threading.Thread(target=nohup))
        time.sleep(0.02)
        workers.append(threading.Thread(target=self.do_success))
        workers.append(threading.Thread(target=self._load_job))
        workers.append(threading.Thread(target=self.do_error))
        for i in range(1,self.worker_count):
            workers.append(threading.Thread(target=self.do))
        for i in workers:
            i.setDaemon(True)
            i.start()
        for i in workers:
            i.join()

    def start(self):
        if self.thread_mode=='thread':
            self._start_thread()
        else:
            self._start_gevent()

    def pause(self):
        self.status=self.Status.PAUSE

    def stop(self):
        self.status=self.Status.STOP
