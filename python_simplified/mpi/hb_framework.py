import logging
import time
import sys
from mpi4py import MPI

from mpi.controller import Controller
from mpi.message import ControllerToWorkerMessage


class HummingbirdFramework(object):
    """
    Framework that the user runs to run on Hummingbird.
    """

    """
    File to write the logs for the entire Hummingbird framework.
    """
    log_file = "hb_framework.log"
    """
    Logging level when printing messages.
    """
    log_level = logging.DEBUG

    MASTER_RANK = 0

    # noinspection PyPep8Naming
    @staticmethod
    def run(TaskClass, WorkerClass):
        """
        Run by the user.  It manages all communication operations that must be
        done.  It only leaves for the user to define what tasks must be
        performed.

        :param TaskClass: Defines the task sent to the workers.
        :type TaskClass: class

        :param WorkerClass: Class that defines how the workers execute the
                            passed task.
        :type WorkerClass: class
        """
        HummingbirdFramework._setup_logger()

        # Rank selects whether the task is a master or slave.
        rank = MPI.COMM_WORLD.Get_rank()
        comm = MPI.COMM_WORLD

        if rank == HummingbirdFramework.MASTER_RANK:
            logging.info("************* HUMMINGBIRD MPI HOST CREATED *************")
            HummingbirdFramework._run_controller(comm, TaskClass)
        else:
            worker = WorkerClass(comm, rank)
            worker.run()

    @staticmethod
    def _is_message_pending(comm):
        """
        Waits for a pending message to arrive.

        :param comm:
        :return: Message from the finished worker.
        :rtype: dict
        """
        return comm.Iprobe(source=MPI.ANY_SOURCE)

    # noinspection PyPep8Naming
    @staticmethod
    def _run_controller(comm, TaskClass):
        """
        Executes the controller and manages sending the messages to the workers.

        :param comm:
        :param TaskClass: Class that defines the tasks to be sent to the
                          workers.
        :type TaskClass: class
        """
        status = MPI.Status()
        controller = Controller(comm)

        log_txt = 'CONTROLLER: Starting %d workers' % controller.n_workers
        logging.info(log_txt)
        solver = TaskClass()

        all_messages_sent = False

        # Run the master
        while True:
            while HummingbirdFramework._is_message_pending(comm):
                worker_result = comm.recv(status=status)
                controller.add_available_worker(status.Get_source())
                solver.process_results(status.Get_source(), worker_result)

            # If all tasks are done, do not exit until
            if all_messages_sent:
                if controller.all_workers_completed():
                    logging.info("CONTROLLER: All workers done and " 
                                 "processed. Exiting...")
                    sys.exit(0)
                time.sleep(1)
                continue

            while controller.have_available_workers_p():
                try:
                    task = solver.get_next()
                except StopIteration:
                    # Generator fully consumed
                    controller.terminate_everything()
                    all_messages_sent = True
                    break
                else:
                    worker = controller.get_available_worker()
                    logging.info("CONTROLLER: Packing task \"%s\" for worker %d"
                                 % (task, worker))
                    message = ControllerToWorkerMessage.build(False, task)
                    comm.send(message, dest=worker)
                    time.sleep(1)

    @staticmethod
    def _setup_logger():
        """
        Logger Configurator

        Configures the framework's logger.
        """
        # noinspection PyProtectedMember
        logger = logging.getLogger()
        num_existing_handlers = len(logger.handlers)
        if num_existing_handlers > 0:
            logging.info("%d handlers already exist. Not adding any loggers."
                         % num_existing_handlers)
            return

        # Example Time Format - 12/12/2010 11:46:36 AM
        date_format = '%m/%d/%Y %I:%M:%S %p'

        format_str = '%(asctime)s -- %(levelname)s -- %(message)s'
        logging.basicConfig(filename=HummingbirdFramework.log_file,
                            level=HummingbirdFramework.log_level,
                            format=format_str, datefmt=date_format)

        # Also print to stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(format_str)
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
