from mpi4py import MPI
from time import sleep
import sys
import subprocess
import random
import socket

log_priority_threshold = 0


def logprint(priority, message):
    global log_priority_threshold
    if priority >= log_priority_threshold:
        print(message)


class Controller():
    def __init__(self, comm):
        self.comm = comm
        self.n_workers = comm.Get_size()
        self.available_workers = set(range(1, self.n_workers))

    def have_available_workers_p(self):
        return len(self.available_workers) > 0

    def add_available_worker(self, w):
        self.available_workers.add(w)

    def terminate_everything(self):
        self.terminate_workers(list(range(1, self.n_workers)))
        print('Rank 0: Finished Successfully!!')
        sys.exit(0)

    def terminate_workers(self, workers_l):
        for w in workers_l:
            message = {'should_exit': True, 'problem': None}
            self.comm.isend(message, dest=w)

    def get_available_worker(self):
        # available_workers MUST BE NOT EMPTY
        return self.available_workers.pop()


class ProblemSolver():
    def __init__(self):
        self.data_aggregator = {'list': [], 'counter': 0}
        self.dir_list = []

    def initialize_task_generator(self):
        self.dir_list = ['/', '/hb/home', '/hb/home', '/hb/home', '/hb/home',
                         '/hb/home', '/hb/home', '/hb/home', '/hb/home',
                         '/hb/home', '/hb/home', '/hb/home', '/hb/home',
                         '/hb/home', '/hb/home']
        self.task_generator = self.task_generator_creator()

    def task_generator_creator(self):
        for d in self.dir_list:
            if random.randint(1, 10) > 6:
                yield 'Wait Please!'
            yield ['ls', d]
        yield 'End of Problems!'

    def process_results(self, results):
        logprint(10, 'process_results: {}, {}'.format(results['directory'],
            results['len']))
        self.data_aggregator['list'].append(
            (results['directory'], results['len']))
        self.data_aggregator['counter'] += results['len']

    def next_task(self):
        return next(self.task_generator)

    def print_final_statistics(self):
        logprint(10, '== Final Statistics by Solver ==')
        logprint(10, self.data_aggregator)


def calculate(problem):
    cmd_l = problem['cmd_l']
    input = problem['cmd_input'].encode('utf-8')
    output = subprocess.run(cmd_l, stdout=subprocess.PIPE,
        input=input).stdout.decode('utf-8')
    # parse command output
    results = {'directory': cmd_l[1], 'len': len(output)}
    sleep(random.randint(0,2))
    return results


def unpack_problem(message):
    """Extract the problem incorporated in 'message'"""
    problem = message['problem']
    return problem


def worker_should_exit(message):
    """Should the worker receiving 'message' be terminated?"""
    return message['should_exit']


def pack_problem(problem_cmd_l):
    message = dict()
    message['should_exit'] = False
    message['problem'] = {'cmd_l':problem_cmd_l, 'cmd_input':''}
    return message


def message_pending_P(comm):
    return comm.Iprobe(source=MPI.ANY_SOURCE)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        logprint(10, 'Starting with {} cores!'.format(comm.Get_size()))
        status = MPI.Status()
        controller = Controller(comm)
        solver = ProblemSolver()
        solver.initialize_task_generator()
        while True:
            while message_pending_P(comm):
                data = comm.recv(status=status)
                controller.add_available_worker(status.Get_source())
                solver.process_results(data)
            while controller.have_available_workers_p():
                problem = solver.next_task()
                if problem == 'Wait Please!':
                    logprint(10, 'Waiting for new tasks to occur...')
                    break
                elif problem == 'End of Problems!':
                    solver.print_final_statistics()
                    controller.terminate_everything()
                else:
                    worker = controller.get_available_worker()
                    logprint(10, 'Packing problem: {}'.format(problem))
                    message = pack_problem(problem)
                    comm.isend(message, dest=worker)
            sleep(0.2)
    else:
        while True:
            message = comm.recv()
            if worker_should_exit(message):
                print('Rank {}: Exiting by request!'.format(rank))
                sys.exit(0)
            logprint(10, 'Rank {}({}): Executing task'.format(rank,
                socket.gethostname()))
            problem = unpack_problem(message)
            results = calculate(problem)
            comm.send(results, dest=0)


if __name__ == '__main__':
    main()
