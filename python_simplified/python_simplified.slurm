#!/bin/bash
#SBATCH --job-name=job_uniform_sampler  # Job name
##SBATCH --partition=256x44             # 256GBs RAM & 44 cores
#SBATCH --partition=128x24              # 128GBs RAM & 24 cores
##SBATCH --partition=Instruction        # Use this partition for coursework
#SBATCH --mail-type=ALL                 # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=zhammoud@ucsc.edu   # Where to send work related emails
#SBATCH -N 2                            # Number of processing nodes
#SBATCH -n 12                            # Total number of cores.
#SBATCH --mem=50G                       # Amount of RAM required per node
#SBATCH --account=zhammoud
#SBATCH --time=1000:10:00               # Time limit hrs:min:sec
#SBATCH --output=mpi_uni_sampler_%j.out # Standard output and error log, "%j" is the job number

# PYTHON_VERSION=2.7.14

## For more details, see here: https://www.hb.ucsc.edu/documentation/creating-scripts-to-run-jobs/

module load python-3.6.2
module load openmpi
module list
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib64"
mpirun python3 run_on_hummingbird.py 

#PYTHON_VERSION=2.7.14

## For more details, see here: https://www.hb.ucsc.edu/documentation/creating-scripts-to-run-jobs/

#module load openmpi
#source activate conda-$PYTHON_VERSION
#module list
#export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib64"
#mpirun ~/anaconda/envs/conda-$PYTHON_VERSION/bin/python run_on_hummingbird.py 

 
