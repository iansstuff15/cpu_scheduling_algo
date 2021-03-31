class Process:

    def __init__(self,id,arrival_time,burst_time):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = 0
        self.completion_time = 0
        self.turn_around_time = 0
        self.waiting_time = 0
        self.partial_waiting_time = 0
  

    def decrement_burst_time(self):
        self.burst_time = self.burst_time - 1
        return

    def create_start_time(self, start_time):
        self.start_time = start_time

    def create_completion_time(self, completion_time):
        self.completion_time = completion_time
    
    def compute_turnaround_time(self):
        self.turn_around_time = self.completion_time - self.arrival_time
        return self.turn_around_time

    def compute_waiting_time(self):
        self.waiting_time = self.turn_around_time - self.completion_time
        return self.waiting_time
    
    def partial_waiting_time(self):
        self.partial_waiting_time = self.start_time - self.arrival_time
        return self.partial_waiting_time

    def return_arrival_time(self):
        return self.arrival_time
    
    def return_burst_time(self):
        return self.burst_time
    
    def return_start_time(self):
        return self.start_time
    
    def return_completion_time(self):
        return self.completion_time