# Purpose: declare classes
# Author: Nathan Burlis

import constants

# Job class
class Job:
    def __init__(self, rel, execu, abs_dead):
        self.rel = rel
        self.execu = execu
        self.abs_dead = abs_dead
        self.proc_time = 0
        self.complete = False
        self.wait_time = 0
        self.update_wait_time = False
        self.response_time = 0

    def execute(self, tick):
        if self.update_wait_time == True:
            self.update_wait_time = False
            self.wait_time = tick - self.rel
        self.proc_time += 1
        if(self.proc_time == self.execu):
            self.complete = True
            self.response_time = tick - self.rel

# Task class
class Task:
    def __init__(self, job_list):
        self.job_list = job_list
        self.jobs_ready = []
        self.jobs_complete = []
        self.task_complete = False
        self.cpu_time = 0

    def task_complete_check(self): # Checks if the task completed
        if len(self.jobs_complete) == len(self.job_list):
            self.task_complete = True

    def update_jobs_complete(self): # Adds job to a complete job list if it is done executing and removes it
        for i,job in enumerate(self.jobs_ready):
            if job.complete == True:
                self.jobs_complete.append(job)
                self.jobs_ready.pop(i)

    def update_jobs_ready(self, tick): # Adds a job to the ready list if it is ready to execute
        for job in self.job_list:
            if job.rel == tick:
                job.update_wait_time = True
                self.jobs_ready.append(job)

# Algorithm statistics class
class Alg_data:
    def __init__(self):
        self.tasks_complete = 0
        self.avg_wait_time = 0.0
        self.avg_cpu_util = 0.0
        self.avg_response_time = 0.0
        self.tot_wait_time = 0.0
        self.tot_response_time = 0.0
        self.jobs_complete = 0

    def averages(self):
        self.avg_wait_time = float(self.tot_wait_time/constants.RUNS)
        self.avg_response_time = float(self.tot_response_time/constants.RUNS)