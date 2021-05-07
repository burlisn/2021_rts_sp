# Purpose: main file
# Author: Nathan Burlis

# Scheduling Notes: A job can execute when it is released. Starting tick is 0, ending tick is 119. Absolute deadline
#                   is the last tick that a job can execute.

import classes
import constants
import random
import copy

def main() -> None:
    
    # Declaring stat collecting objects for each algorithm
    rr_stats = classes.Alg_data()
    edf_stats = classes.Alg_data()
    fifo_stats = classes.Alg_data()

    # Running the simulation for each randomly generated task
    for i in range(constants.RUNS):
        
        # Generate random task
        task_keep = classes.Task(generate_jobs())
        task_send = copy.deepcopy(task_keep)
        
        # print the task
        print("Jobs:", len(task_send.job_list))
        print("Format: [r, e, d]")
        for i,job in enumerate(task_send.job_list):
            print(i,":",job.rel, job.execu, job.abs_dead)
        print("")
        
        # Perform and analyze Round Robin
        print("Round Robin:")
        round_robin(task_send)
        task_analysis(task_send, rr_stats)
        print("")

        # Perform and analyze EDF
        del task_send
        task_send = copy.deepcopy(task_keep)
        print("EDF:")
        edf(task_send)
        task_analysis(task_send, edf_stats)
        print("")

        # Perform and analyze FIFO
        del task_send
        task_send = copy.deepcopy(task_keep)
        print("FIFO:")
        fifo(task_send)
        task_analysis(task_send, fifo_stats)
        print("")
        
        print("----------------------------------------------------------")

    rr_stats.averages()
    edf_stats.averages()
    fifo_stats.averages()

    # Print algorithm statistics
    print("---------------- ALGORITHM COMPARISON --------------------")
    print("Tasks complete: \nRound Robin - {}\nEDF - {}\nFIFO - {}".format(rr_stats.tasks_complete, edf_stats.tasks_complete, fifo_stats.tasks_complete))
    print("")
    print("Jobs complete: \nRound Robin - {}\nEDF - {}\nFIFO - {}".format(rr_stats.jobs_complete, edf_stats.jobs_complete, fifo_stats.jobs_complete))
    print("")
    print("Average wait time: \nRound Robin - {}\nEDF - {}\nFIFO - {}".format(rr_stats.avg_wait_time, edf_stats.avg_wait_time, fifo_stats.avg_wait_time))
    print("")
    print("Average response time: \nRound Robin - {}\nEDF - {}\nFIFO - {}".format(rr_stats.avg_response_time, edf_stats.avg_response_time, fifo_stats.avg_response_time))
    print("")

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

    while tick < 120 and task.task_complete == False:
        task.update_jobs_ready(tick) # Update the jobs_ready list

        if task.jobs_ready:
            i = i % len(task.jobs_ready)
            task.jobs_ready[i].execute(tick)
            task.update_jobs_complete()
            two_tick = two_tick + 1
            task.cpu_time += 1

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
            task.cpu_time += 1

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
            task.cpu_time += 1
        
        task.update_jobs_complete()
        task.task_complete_check()
        

        tick += 1



# Returns the analysis statistics
def task_analysis(task: classes.Task, alg_stats: classes.Alg_data):
    tot_wait_time = 0
    tot_response_time = 0
    avg_wait_time = 0
    avg_response_time = 0
    total_complete = 0
    indexes_complete = []
    cpu_util = 0.0

    for i,job in enumerate(task.job_list):
        if job.complete == True:
            total_complete += 1
            indexes_complete.append(i)

            #Response time is only taken of the jobs that completed
            tot_response_time += job.response_time
        tot_wait_time += job.wait_time
    
    cpu_util = float(task.cpu_time)/constants.MAX_TICKS

    if task.task_complete == True:
        alg_stats.tasks_complete += 1

    avg_wait_time = float(tot_wait_time/len(task.job_list))
    avg_response_time = float(tot_response_time/len(task.job_list))

    alg_stats.tot_wait_time += avg_wait_time
    alg_stats.tot_response_time += avg_response_time
    alg_stats.jobs_complete += len(task.jobs_complete)

    # Print statistics
    print("Completed jobs:", indexes_complete)
    print("Average wait time:", avg_wait_time)
    print("Average response time:", avg_response_time)
    print("CPU utilization:", cpu_util)

if __name__ == "__main__":
    main()