--------------------mpiexample.slurm---
#!/bin/bash
#SBATCH --job-name=job_meel_unigen2 # Job name
#SBATCH --mail-type=ALL             # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH -N 2
#SBATCH -n 4
#SBATCH --account=zhammoud
#SBATCH --time=50:00:50             # Time limit hrs:min:sec
#SBATCH --output=mpi_test_%j.out    # Standard output and error log
#SBATCH --partition=Instruction 
module load openmpi
module load python-3.6.2
module list
cd ~/MPIExamples
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib64"
mpirun python unigen2_controller.py
----------------------------------------