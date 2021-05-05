# Purpose: main file
# Author: Nathan Burlis

# Scheduling Notes: A job can execute when it is released. Starting tick is 0, ending tick is 119. Absolute deadline
#                   is the last tick that a job can execute.

import classes
import constants
import random
import copy

def main() -> None:
    tasks_complete = 0

    for i in range(constants.RUNS):
        task_keep = classes.Task(generate_jobs())
        task_send = copy.deepcopy(task_keep)
        
        print("Jobs:")
        print(len(task_send.job_list))
        for job in task_send.job_list:
            print(job.rel, job.execu, job.abs_dead)
        
        print("Round Robin:")
        round_robin(task_send)
        analysis(task_send)

        task_send = copy.deepcopy(task_keep)
        print("EDF:")
        round_robin(task_send)
        analysis(task_send)

        if task_send.task_complete:
            tasks_complete += 1
        
        print("-------------------------")

    print("Tasks completed:", tasks_complete, "/", constants.RUNS)

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

    while tick < 120 and not(task.task_complete):
        task.update_jobs_ready(tick) # Update the jobs_ready list

        if task.jobs_ready:
            i = i % len(task.jobs_ready)
            task.jobs_ready[i].execute(tick)
            task.update_jobs_complete()
            two_tick = two_tick + 1

        task.update_jobs_complete()

        if (two_tick == 2 and task.jobs_ready):
            two_tick = 0
            i = (i+1)%len(task.jobs_ready)

        task.task_complete_check()

        tick += 1

def edf(task):
    tick = 0
    i = 0

    while tick < 120 and task.task_complete == False:
        task.update_jobs_ready(tick)

        if task.jobs_ready:
            ded = 119
            for j,job in enumerate(task.jobs_ready):
                if job.abs_dead <= ded:
                    ded = job.abs_dead
                    i = j

            task.jobs_ready[i].execute(tick)

        task.update_jobs_complete()
        task.task_complete_check()

        tick += 1

def fifo(task):
    tick = 0
    i = 0

    while tick < 120 and task.task_complete == False:
        task.update_jobs_ready(tick)

        if task.jobs_ready:
            task.jobs_ready[0].execute(tick)
        
        task.update_jobs_complete()
        task.task_complete_check()

        tick += 1



# Returns the analysis statistics
def analysis(task):
    tot_wait_time = 0
    avg_wait_time = 0
    total_complete = 0

    for job in task.job_list:
        if job.complete == True:
            total_complete += 1
        tot_wait_time += job.wait_time
    
    avg_wait_time = float(tot_wait_time/len(task.job_list))

    # Print statistics
    print("Average wait time:", avg_wait_time)
    print("Jobs complete:", total_complete)

if __name__ == "__main__":
    main()