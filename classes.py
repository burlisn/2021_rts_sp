# Purpose: declare classes
# Author: Nathan Burlis

class Job:
    def __init__(self, rel, execu, abs_dead):
        self.rel = rel
        self.execu = execu
        self.abs_dead = abs_dead
        
    proc_time = 0
    complete = False

class Task:
    def __init__(self, job_list):
        self.job_list = job_list

    task_complete = False