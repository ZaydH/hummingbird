# Getting Started with Hummingbird

These are notes I found helpful for getting started with the University of California, Santa Cruz (UCSC)'s Hummingbird HPC server.  Complete information is available on the [official Hummingbird page](https://www.hb.ucsc.edu/).

## Logging In

From the terminal, enter:

    ssh <cruzid>@hb.ucsc.edu

**Note**: this is your CRUZID, not your SOE id.

### Off-Campus Access

If you are using Hummingbird away from campus, you must be logged into UCSC's VPN. For more information, see [UCSC's IT page](https://its.ucsc.edu/vpn/installation.html).

## Slurm 

This is a protocol for running batch jobs.  I have included an example in the "examples" folder. You need to modify the parameters in `<...>` brackets.  Pay special care to select the right partition.  This is done by removing one of the preceding pound signs ("#").

Harvard compiled a set of [useful sbatch commands](https://www.rc.fas.harvard.edu/resources/documentation/convenient-slurm-commands/).  Examples of commands I have used include: `squeue` to check the status of a command, `scancel` to kill a running job, and `scontrol`.

## Loading Modules

Modules are how you get access to pre-install tools (e.g., python, R, Matlab, etc.).  You load modules by entering:

    module load <name>

To get the list of available modules, enter:

    module spider

To find the list of modules YOU have currently load, enter:

    module list

## mpi4py and Anaconda

This is a Python module that allows you to communicate with MPI via OpenMPI. `mpi4py` was recently installed on the server.

If you ever need a custom (or want control of the) Python distributions, install install [Anaconda](https://www.anaconda.com/what-is-anaconda/) in your user directory.  To do this, run the command:

    ./install_anaconda

You can change the version of Anaconda through the variable `VERSION_NUM` in the file. After an install, you may need to call `source .\bashrc` for your `bash` profile to be updated.

If you are using Anaconda, make sure you slurm file references the absolute path to conda's bin file and does not call the standard `python`.  You may also want to have it activate the conda environment using the command:

    source activate <CondaEnvironmentName>

