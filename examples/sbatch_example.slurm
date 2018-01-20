--------------------mpiexample.slurm---
#!/bin/bash
#SBATCH --job-name=job_test         # Job name
#SBATCH --mail-type=NONE            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH -N 2
#SBATCH -n 4
#SBATCH --account=<account_name_in_hummingbird>
#SBATCH --time=00:03:50             # Time limit hrs:min:sec
#SBATCH --output=mpi_test_%j.out    # Standard output and error log
#SBATCH --partition=Instruction 
module load openmpi
module load python-3.6.2
module list
cd ~/MPIExamples
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib64"
mpirun python mpipython.py
----------------------------------------