import logging

# abc = Abstract Base Class
# Used by Python to indicate something is an abstract class
import abc
import sys
import socket

from mpi.message import ControllerToWorkerMessage


class AbstractWorker:
    """
    Abstract class that defines a worker.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, comm, rank):
        self.comm = comm
        self.rank = rank

    def run(self):
        """
        Runs the worker where it accepts messages from the master and then
        executes them.  This method eventually terminates based on a message
        from the master.
        """
        # Continue running tasks until all have been completed
        while True:
            msg = self.comm.recv()

            if ControllerToWorkerMessage.extract_should_exit(msg):
                txt = 'Worker Rank \#{}: Exiting by request!'.format(self.rank)
                logging.info(txt)
                sys.exit(0)

            log_txt = ('Worker Rank \#%d (%s): Executing task'
                       % (self.rank, socket.gethostname()))
            logging.info(log_txt)

            task = ControllerToWorkerMessage.extract_generated_task(msg)
            results = self.execute_task(task)
            # Requires "results" be pickable
            self.comm.send(results, dest=0)

    @abc.abstractmethod
    def execute_task(self, msg):
        """
        Executes the task passed by the master.

        :param msg: Message from the master.
        :type msg: dict

        :return: Information to be passed back to the master.
        :rtype: dict
        """
        pass


class AbstractTask:
    """
    Abstract class that defines what a task the workers will perform.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        Only defines the task generator.  The user may add any additional
        features to this class that they need when generating or processing
        task results.
        """
        self.generator = self.__class__.task_generator()

    def get_next(self):
        """
        Extracts and returns the next task a worker will perform.  Note that the
        task must be PICKABLE.

        :return: Next task to be performed by a worker.
        """
        return next(self.generator)

    @staticmethod
    @abc.abstractmethod
    def task_generator():
        """
        Define a generator that enumerates the objects to be created.
        """
        pass

    @abc.abstractmethod
    def process_results(self, results):
        """
        Process the results from a worker.

        :param results: Results from the worker
        :type results: dict
        """
        pass
