import logging

from mpi.message import ControllerToWorkerMessage


class Controller(object):
    def __init__(self, comm):
        self.comm = comm
        self.n_workers = comm.Get_size() - 1
        self.available_workers = set(range(1, self.n_workers + 1))

    def have_available_workers_p(self):
        """
        Checks whether any worker processes are idle.

        :return: True if at least one worker is available.
        :rtype: bool
        """
        return len(self.available_workers) > 0

    def add_available_worker(self, w):
        """
        Adds a worker to management by the master.
        """
        self.available_workers.add(w)

    def terminate_everything(self):
        """
        All tasks are completed so the master kills all workers then exits
        completely.
        """
        self.terminate_workers(list(range(1, self.n_workers + 1)))
        txt = "CONTROLLER: Finished Successfully. Waiting" + \
              " on any unfinished workers..."
        logging.info(txt)

    def terminate_workers(self, workers_l):
        """
        Sends message to terminate all workers.

        :param workers_l: Worker identification numbers from 1 to Number of
                         workers.
        :type workers_l: List[int]
        """
        message = ControllerToWorkerMessage.exit_message()
        for w in workers_l:
            self.comm.isend(message, dest=w)

    def get_available_worker(self):
        """
        Accesses an available worker.

        :return: Index of the next worker that will perform a specified task.
        """
        # available_workers MUST BE NOT EMPTY
        return self.available_workers.pop()

    def all_workers_completed(self):
        """
        :return: True if all workers are done processing (i.e., are available)
        :rtype: bool
        """
        return len(self.available_workers) == self.n_workers
