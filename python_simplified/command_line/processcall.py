import os
import shlex
import subprocess
import time
import signal
from enum import Enum


class RunStatus(Enum):
  PASSED = "passed"
  TIMEOUT = "timeout"

class CommandLine(object):

  @staticmethod
  def _wait_timeout(proc, seconds):
    """
    Process Timeout Wait Function

    Waits for a function to either complete execution.  If the program takes
    longer to complete than the timeout, it kills the process.

    :param proc: Process information

    :param seconds: Timeout time in seconds
    :type seconds: float

    :return: Test status result
    :rtype: Test.Result
    """
    """Wait for a process to finish, or raise exception after timeout"""
    start = time.time()
    end = start + seconds
    interval = 0.01

    while True:
      result = proc.poll()
      if result is not None:
        return RunStatus.PASSED
      if time.time() >= end:
        os.killpg(proc.pid, signal.SIGTERM)
        # raise RuntimeError("Process timed out")
        return RunStatus.TIMEOUT
      time.sleep(interval)

  @staticmethod
  def run(command_line_str, timeout_sec, **kwargs):
    """
    Execute the command line command.

    :param command_line_str: Instruction with command line.  The string should have all parameters
                             and be self contained.  Processing the string will be handled by the
                             function.
    :type command_line_str: str
    :param timeout_sec: Timeout for the command line instruction.
    :type timeout_sec: int
    :param kwargs:
    :return: Result from the run and the command line instruction.
    :rtype: Tuple(RunStatus, str)
    """
    if 'stdout' in kwargs:
      raise ValueError('stdout argument not allowed.')
    inputs_args = shlex.split(command_line_str)
    process = subprocess.Popen(inputs_args, stdout=subprocess.PIPE,
                               preexec_fn=os.setsid, **kwargs)
    result = CommandLine._wait_timeout(process, timeout_sec)

    if result == RunStatus.TIMEOUT:
      return result, None

    # Read the output of the process
    output, unused_err = process.communicate()
    if output is not None and type(output) != str:
      output = output.decode()  # For python3 compatibility in bash
    return result, output
