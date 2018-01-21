# Getting Started with Hummingbird

These are notes I found helpful for getting started with the University of California, Santa Cruz (UCSC)'s Hummingbird HPC server.  Complete information is available on the [official Hummingbird page](https://www.hb.ucsc.edu/).

## Logging In

From the terminal, enter:

    ssh <cruzid>@hb.ucsc.edu

**Note**: this is your CRUZID, not your SOE id.

### Off-Campus Access

If you are using Hummingbird away from campus, you must be logged into UCSC's VPN. For more information, see [UCSC's IT page](https://its.ucsc.edu/vpn/installation.html).

## Slurm 

This is a protocol for running batch jobs.  I have included an example in the "examples" folder. You need to modify the parameters in `<...>` brackets.  Pay special care to select the right partition.  This is done by removing one of the preciding pound signs ("#").

## Loading Modules

Modules are how you get access to pre-install tools (e.g., python, R, Matlab, etc.).  You load modules by entering:

    module load <name>

To get the list of available modules, enter:

    module spider

To find the list of modules YOU have currently load, enter:

    module list

## mpi4py and Anaconda

This is a Python module that allows you to communicate with MPI via OpenMPI. At the time of writing, this module is not built into Hummingbird' Python distribution (*I know it's dumb*).  To address this, install [Anaconda](https://www.anaconda.com/what-is-anaconda/), and use your own local install.  To do this, run the command:

    .\install_anaconda

You can change the version of Anaconda through the variable `VERSION_NUM` in the file. After an install, you may need to call `source .\bashrc` for your `bash` profile to be updated.

If you are using Anaconda, make sure you slurm file references the absolute path to conda's bin file and does not call the standard `python`.  You may also want to have it activate the conda environment using the command:

    source activate <CondaEnvironmentName>

