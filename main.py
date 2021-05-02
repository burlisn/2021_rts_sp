# Purpose: main file
# Author: Nathan Burlis

import classes
import constants
import random

def main() -> None:
    job_list = generate_jobs()
    for job in job_list:
        print(job.rel, job.execu, job.abs_dead)

def generate_jobs():
    cur_job_amount = 0
    cur_exec_sum = 0
    job_list = []
    rel = 0
    execu = 0
    abs_dead = 0

    while(cur_job_amount < constants.MAX_JOBS and cur_exec_sum < constants.MAX_TICKS):
        rel = random.randint(0, 119)
        execu = random.randint(0, constants.MAX_TICKS - cur_exec_sum)
        abs_dead = random.randint(rel+execu, 120)
        
        job_list.append(classes.Job(rel, execu, abs_dead))

        cur_job_amount += 1
        cur_exec_sum += execu

    return job_list

# Round robin scheduling, each job gets 2 ticks before moving onto the next job
def round_robin(job_list):
    tick = 0
    two_tick = 0
    i = 0

    while tick < 120:
        if two_tick < 2:
            tick = execute(job_list[i], tick)
            two_tick += 1
        else:
            two_tick = 0
            i += 1
            i = i % job_list.size()
            tick = execute(job_list[i], tick)


# Execute a job for 1 time unit and update the job
def execute(job, tick):
    if(job.complete == False): # If the job is not complete, execute for 1 tick
        job.proc_time += 1
        tick += 1
    if(job.proc_time == job.execu): # Check if the job is complete
        job.complete = True
        print("Job is done!!!!")

    return tick


if __name__ == "__main__":
    main()