class Process():
    """docstring for ."""

    def __init__(self, pid, arrival_time, cpu_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.cpu_time = cpu_time
        self.time_ran = 0
        self.finished = 0
        self.began = None
