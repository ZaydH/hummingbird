#!/bin/bash
#SBATCH --job-name=job_<name>           # Job name
#SBATCH --partition=256x44              # 256GBs RAM & 44 cores
##SBATCH --partition=128x24             # 128GBs RAM & 24 cores
##SBATCH --partition=Instruction        # Use this partition for coursework
#SBATCH --mail-type=NONE                # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=<cruzid>@ucsc.edu   # Where to send work related emails
#SBATCH -N 2                            # Number of processing nodes
#SBATCH -n 4                            # Total number of cores.
#SBATCH -mem=<Amount>G                  # Amount of RAM required per node
#SBATCH --account=<account_name_in_hummingbird>
#SBATCH --time=hh:mm:ss                 # Time limit hrs:min:sec
#SBATCH --output=mpi_test_%ji_%d.out    # Standard output and error log, "%j" is the job number

## For more details, see here: https://www.hb.ucsc.edu/documentation/creating-scripts-to-run-jobs/

module load openmpi
#module load python-3.6.2
#module load python-2.7.11
module list
cd <YourFolder>                         # Go to where your code is
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib64"
mpirun python <ModuleName>              # Would be located in <YourFolder> as above.
