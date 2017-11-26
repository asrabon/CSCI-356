from process import Process
import sys

# variable that will keep track of processes running
clock = 0
running_processes = []
completed_processes = []
time_quantum = 0
current_time_quantum = 0


def main():
    process_list = get_processes()
    print('Got all processes')
    scheduling_algorithm = sys.argv[1]
    if (scheduling_algorithm == 'FCFS'):
        first_come_first_serve(process_list)
    elif (scheduling_algorithm == 'RR'):
        round_robin(process_list)
    else:
        preemptive_shortest_job_first(process_list)


def get_processes():
    ls = []
    scheduler_input = input()
    while (scheduler_input != '0 0 0'):
        scheduler_input = scheduler_input.split(' ')
        ls.append(
            Process(scheduler_input[0], scheduler_input[1], scheduler_input[
                2]))
        scheduler_input = input()
    return ls


def first_come_first_serve(process_list):
    while (len(running_processes) > 0 or len(process_list) > 0):
        global clock
        check_arrived(process_list)
        try:
            process_to_run = running_processes[0]
        except:
            process_to_run = None
        if (process_to_run is not None):
            run_process(process_to_run)
        else:
            print('%s idle' % (clock))
        clock += 1
    print_report()


def round_robin(process_list):
    global time_quantum
    time_quantum = int(sys.argv[2])
    global current_time_quantum
    current_time_quantum = time_quantum - 1
    process_to_add = None
    while (len(running_processes) > 0 or len(process_list) > 0):
        global clock
        check_arrived(process_list)
        if (process_to_add is not None):
            running_processes.append(process_to_add)
            process_to_add = None
        try:
            process_to_run = running_processes[0]
        except:
            process_to_run = None
        if (process_to_run is not None):
            run_process(process_to_run)
            if (current_time_quantum == 0):
                current_time_quantum = time_quantum
                process_to_add = running_processes.pop(0)
            current_time_quantum = current_time_quantum - 1
        else:
            print('%s idle' % (clock))
        clock += 1
    print_report()


def preemptive_shortest_job_first(process_list):
    while (len(running_processes) > 0 or len(process_list) > 0):
        global clock
        check_arrived(process_list)
        process_to_run = get_quickest_process(running_processes)
        if (process_to_run is not None):
            run_process(process_to_run)
        else:
            print('%s idle' % (clock))
        clock += 1
    print_report()


def get_quickest_process(processes):
    quickest_process = None
    time = 9999999
    for process in processes:
        time_to_run = int(process.cpu_time) - int(process.time_ran)
        if (time_to_run < time):
            quickest_process = process
            time = time_to_run
    return quickest_process


def run_process(process):
    global clock
    global time_quantum
    global current_time_quantum
    process.time_ran += 1
    if (process.began is None):
        process.began = clock
    if (int(process.time_ran) == int(process.cpu_time)):
        print('%s %s finished' % (clock, process.pid))
        completed_processes.append(process)
        current_time_quantum = time_quantum
        process.finished = clock
        global running_processes
        for process in completed_processes:
            try:
                running_processes.remove(process)
            except:
                pass
    else:
        print('%s %s running' % (clock, process.pid))


def check_arrived(process_list):
    for process in process_list:
        if (int(process.arrival_time) == clock):
            running_processes.append(process)
            print('%s %s arriving' % (clock, process.pid))
    for process in running_processes:
        try:
            process_list.remove(process)
        except:
            pass


def print_report():
    global clock
    wait_time = 0
    response_time = 0
    total_cpu_time = 0
    for process in completed_processes:
        wait_time += int(process.finished) - int(process.cpu_time) - int(
            process.arrival_time)
        response_time += int(process.began) - int(process.arrival_time)
        total_cpu_time += int(process.cpu_time)
    print('Average waiting time: %s' % (wait_time / len(completed_processes)))
    print('Average response time: %s' %
          (response_time / len(completed_processes)))
    print('Average CPU Usage: %.2f%s' % (((total_cpu_time) / clock) * 100,
                                         '%'))


if __name__ == '__main__':
    main()
