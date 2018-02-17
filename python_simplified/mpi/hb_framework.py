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

  @staticmethod
  def run(TaskClass, WorkerClass):
    """
    Run by the user.  It manages all communication operations that must be done.  It only leaves
    for the user to define what tasks must be performed.

    :param TaskClass: Defines the task sent to the workers.
    :type TaskClass: class

    :param WorkerClass: Class that defines how the workers execute the passed task.
    :type WorkerClass: class
    """
    HummingbirdFramework._setup_logger()

    # Rank selects whether the task is a master or slave.
    rank = MPI.COMM_WORLD.Get_rank()
    comm = MPI.COMM_WORLD

    # noinspection PyPep8Naming
    MASTER_RANK = 0
    if rank == MASTER_RANK:
      logging.info("***************************** New Run Beginning ****************************")
      HummingbirdFramework._run_controller(comm, TaskClass)
    else:
      worker = WorkerClass(comm, rank)
      worker.run()

  @staticmethod
  def _is_message_pending(comm):
    """
    Waits for a pending message to arrive.

    :param comm:
    :return: Message from the finished worker.  It has the same messa
    :rtype: dict
    """
    return comm.Iprobe(source=MPI.ANY_SOURCE)

  @staticmethod
  def _run_controller(comm, TaskClass):
    """
    Executes the controller and manages sending the messages to the workers.

    :param comm:
    :param TaskClass: Class that defines the tasks to be sent to the workers.
    :type TaskClass: class
    """
    logging.info('CONTROLLER: Starting {} workers'.format(comm.Get_size() - 1))
    status = MPI.Status()
    controller = Controller(comm)
    solver = TaskClass()

    all_messages_sent = False

    # Run the master
    while True:
      while HummingbirdFramework._is_message_pending(comm):
        worker_result = comm.recv(status=status)
        controller.add_available_worker(status.Get_source())
        solver.process_results(worker_result)

      # If all tasks are done, do not exit until
      if all_messages_sent:
        if controller.all_workers_completed():
          logging.info("CONTROLLER: All workers done and processed. Exiting...")
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
          logging.info('CONTROLLER: Packing problem: {}'.format(task))
          message = ControllerToWorkerMessage.build(False, task)
          comm.isend(message, dest=worker)
          time.sleep(1)

  @staticmethod
  def _setup_logger():
    """
    Logger Configurator

    Configures the framework's logger.
    """
    date_format = '%m/%d/%Y %I:%M:%S %p'  # Example Time Format - 12/12/2010 11:46:36 AM

    logging.basicConfig(filename=HummingbirdFramework.log_file,
                        level=HummingbirdFramework.log_level,
                        format='%(asctime)s -- %(levelname)s -- %(message)s', datefmt=date_format)

    # Also print to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

