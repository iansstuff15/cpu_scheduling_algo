class RoundRobin:
    def processData(self, no_of_processes):
        process_data = []
        for i in range(no_of_processes):
            temporary = []
            print("+------------------------------+")
            process_id = int(input(" Process ID: "))
            arrival_time = int(input(f" P{process_id} Arrival Time: "))
            burst_time = int(input(f" P{process_id} Burst Time: "))
            # [0] means not executed and [1] means execution complete: current state of the process
            temporary.extend([process_id, arrival_time, burst_time, 0, burst_time]) 
            process_data.append(temporary)
        print("+------------------------------+")
        quantum_time = int(input(" Quantum Time: "))
        print("+------------------------------+\n")
        RoundRobin.schedulingProcess(self, process_data, quantum_time)

    def schedulingProcess(self, process_data, quantum_time):
        start_time = []         # Start time of Processes.
        exit_time = []          # Exit time of Processes.
        executed_process = []   # Executed Processes, can be used for Gantt Chart.
        ready_queue = []        # processes that already arrived
        s_time = 0              # current Start time
        process_data.sort(key=lambda x: x[1]) # Sort processes according to the Arrival Time

        while 1:
            normal_queue = []   # processes that doesnt arrive yet.
            temp = []

            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    present = 0
                    # Checks if the next process is not part of the Ready Queue
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if process_data[i][0] == ready_queue[k][0]:
                                present = 1
                    #  Adds process in the Ready Queue only if it is not already present in it
                    if present == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                        ready_queue.append(temp)
                        temp = []
                    # Appends the recently executed process at the end of Ready Queue
                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                elif process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []

            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break

            if len(ready_queue) != 0:
                # If process's Remaining Burst Time is > that the Quantum Time, 
                # it executes until the end of quantum time then switch
                if ready_queue[0][2] > quantum_time:
                    start_time.append(s_time)
                    s_time = s_time + quantum_time
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - quantum_time
                    ready_queue.pop(0)
                # If process's Remaining Burst Time is <= the Quantum Time, the execution will be completed
                elif ready_queue[0][2] <= quantum_time:
                    start_time.append(s_time)
                    s_time = s_time + ready_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
                    ready_queue.pop(0)

            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                # If process's Remaining Burst Time is > that the Quantum Time, 
                # it executes until the end of quantum time then switch 
                if normal_queue[0][2] > quantum_time:
                    start_time.append(s_time)
                    s_time = s_time + quantum_time
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - quantum_time
                # If process's Remaining Burst Time is <= the Quantum Time, the execution will be completed
                elif normal_queue[0][2] <= quantum_time:
                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)

        t_time = RoundRobin.calculateTurnaroundTime(self, process_data)
        w_time = RoundRobin.calculateWaitingTime(self, process_data)
        RoundRobin.printData(self, process_data, t_time, w_time, executed_process, exit_time)

    # Calculate Turn Around Time
    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            # turnaround_time = completion_time - arrival_time
            turnaround_time = process_data[i][5] - process_data[i][1]       
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        # average_turnaround_time = total_turnaround_time / no_of_processes    
        average_turnaround_time = total_turnaround_time / len(process_data) 
        return average_turnaround_time

    # Calculate Waiting Time
    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            # waiting_time = turnaround_time - burst_time
            waiting_time = process_data[i][6] - process_data[i][4]      
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        # average_waiting_time = total_waiting_time / no_of_processes   
        average_waiting_time = total_waiting_time / len(process_data)   
        return average_waiting_time

    # Display Round Robin Proccesses Data
    def printData(self, process_data, average_turnaround_time, average_waiting_time, executed_process, exit_time):
        process_data.sort(key=lambda x: x[0]) # Process Sorted according to the ID
        print("+=======+===============+===============+=================+=================+==============+")
        print("| P.ID  |  Arrival Time |   Burst Time  | Completion Time | Turnaround Time | Waiting Time |")
        print("+=======+===============+===============+=================+=================+==============+")
        for i in range(len(process_data)):
            print("| P", process_data[i][0], "\t|",                 # P.ID
                    "    ", process_data[i][1], " \t| ",            # Arrival Time
                    "   ", process_data[i][4], " \t|",              # Burst Time
                    "     ", process_data[i][5], " \t  |",          # Completion Time
                    "      ", process_data[i][6], " \t    |",       # Turnaround Time
                    "   ", process_data[i][7], " \t   | ", end="")  # Waiting Time 
            print()
        print("+=======+===============+===============+=================+=================+==============+")
        print(f'\n Average Turnaround Time:  {average_turnaround_time}')
        print(f' Average Waiting Time:  {average_waiting_time}')
        print("\n+=====================================+ GANTT CHART +======================================+")
        # Process
        for i in range(len(executed_process)*8):
            print("-", end="")
        print("\n|"  , end="")
        for i in range(len(executed_process)):
            print("  P", executed_process[i], "\t|", end="")
        print()
        for i in range(len(executed_process)*8):
            print("-", end="")
        # Time
        print()
        print(process_data[0][1], "\t", end="")
        for i in range(len(exit_time)):
            print(exit_time[i],"\t", end="")
        print("\n+==========================================================================================+")

# Execute Program
if __name__ == "__main__": 
    print("\n+==========================+ ROUND ROBIN SCHEDULING ALGORITHM +============================+")
    no_of_processes = int(input(" Enter Number of Processes: "))
    rr = RoundRobin()
    rr.processData(no_of_processes) 
