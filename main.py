# Purpose: main file
# Author: Nathan Burlis

# Scheduling Notes: A job can execute when it is released. Starting tick is 0, ending tick is 119. Absolute deadline
#                   is the last tick that a job can execute.

import classes
import constants
import random

def main() -> None:
    tasks_complete = 0

    for i in range(1000):
        task = classes.Task(generate_jobs())
        print("Jobs:")
        print(len(task.job_list))
        for job in task.job_list:
            print(job.rel, job.execu, job.abs_dead)
        print("--------------------")

    print(tasks_complete)

# Generates a list of jobs that follow the rules
def generate_jobs():
    cur_job_amount = 0
    cur_exec_sum = 0
    job_list = []
    rel = 0
    execu = 0
    abs_dead = 0

    while(cur_job_amount < constants.MAX_JOBS and cur_exec_sum < constants.MAX_TICKS):
        rel = random.randint(0, 119)
        
        execu = random.randint(1, constants.MAX_TICKS - rel)
        if (execu + cur_exec_sum > constants.MAX_TICKS):
            execu = constants.MAX_TICKS - cur_exec_sum

        abs_dead = random.randint(rel + execu - 1, constants.MAX_TICKS -1)

        job_list.append(classes.Job(rel, execu, abs_dead))

        cur_job_amount += 1
        cur_exec_sum += execu

    return job_list

# Round robin scheduling, each job gets 2 ticks before moving onto the next job
def round_robin(task):
    tick = 0
    two_tick = 0
    i = 0
    ind = []
    done = False

    while tick < 120:
        for j,job in enumerate(job_list):
            if job.rel == tick:
                ind.append(j)

        if done == True:
            ind.pop(i)
            if len(ind) != 0:
                i = i % len(ind)
            done = False

        if two_tick < 2:
            done = execute(job_list[ind[i]], tick)
            two_tick += 1
        else:
            two_tick = 0
            i += 1
            i = i % len(ind)
            done = execute(job_list[ind[i]], tick)

        tick += 1

# Execute a job for 1 time unit and update the job
def execute(job):
    if(job.complete == False): # If the job is not complete, execute for 1 tick
        job.proc_time += 1
    if(job.proc_time == job.execu): # Check if the job is complete
        job.complete = True
        print("Job is done!!!!")

    return job.complete

# Returns the analysis statistics
def analysis(job_list):
    task_complete = 1

    for jobs in job_list:
        if jobs.complete == False:
            task_complete = 0

    return task_complete


if __name__ == "__main__":
    main()