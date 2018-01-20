# Using 

These are notes I found helpful for getting started with the University of California, Santa Cruz (UCSC)'s Hummingbird HPC server.  Complete information is available on the [official Hummingbird page](https://www.hb.ucsc.edu/).

## LOGGING INTO HUMMINGBIRD

From the terminal, enter:

    ssh <cruzid>@hb.ucsc.edu

**Note**: this is your CRUZID, not your SOE id.

### Off-Campus Access

If you are using Hummingbird away from campus, you must be logged into UCSC's VPN. For more information, see [UCSC's IT page](https://its.ucsc.edu/vpn/installation.html).

## SLURM 

This is a protocol for running batch jobs.  I have included an example in the "examples" folder. You need to modify the parameters in <> brackets.  Pay special care to select the right partition.  This is done by removing one of the preciding pound signs ("#").

## Loading Modules

Modules are how you get access to pre-install tools (e.g., python, R, Matlab, etc.).  You load modules by entering:

    module load <name>

To get the list of available modules, enter:

    module spider

To find the list of modules YOU have currently load, enter:

    module list

## MPI4PY 

This is a Python module that allows you to communicate with MPI via OpenMPI. At the time of writing, this module is not built into the Python distribution (*I know it's dumb*).  You instead can clone the source via the command:

    git clone [https://bitbucket.org/mpi4py/mpi4py]()

You then copy the directory `mpi4py/src/mpi4py` into your project directory.
