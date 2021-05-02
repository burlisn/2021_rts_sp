# Purpose: declare classes
# Author: Nathan Burlis

class Job:
    def __init__(self, rel, execu, abs_dead):
        self.rel = rel
        self.execu = execu
        self.abs_dead = abs_dead
        
    proc_time = 0
    complete = False

    