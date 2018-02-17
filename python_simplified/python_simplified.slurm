#!/bin/bash
#SBATCH --job-name=<job_name>             # Job name
##SBATCH --partition=256x44               # 256GBs RAM & 44 cores
#SBATCH --partition=128x24                # 128GBs RAM & 24 cores
##SBATCH --partition=Instruction          # Use this partition for coursework
#SBATCH --mail-type=ALL                   # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=<your_email>@ucsc.edu # Where to send work related emails
#SBATCH -N <x>                            # Number of processing nodes
#SBATCH -n <x>                            # Total number of cores.
#SBATCH --mem=<x>G                         # Amount of RAM required per node
#SBATCH --account=<your_account>          # Your cruz-id
#SBATCH --time=1000:10:00                 # Time limit hrs:min:sec
#SBATCH --output=<job_name>_%j.out        # Standard output and error log, "%j" is the job number

## For more details, see here: https://www.hb.ucsc.edu/documentation/creating-scripts-to-run-jobs/

module load python-3.6.2
module load openmpi
module list
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib64"
mpirun python3 run_on_hummingbird.py 
