#!/bin/bash
# Specify a partition
#SBATCH --partition=dg-jup
# Request nodes
#SBATCH --nodes=4
# Request some processor cores
#SBATCH --ntasks=4
# Request GPUs
#SBATCH --gres=gpu:8
# Request memory 
#SBATCH --mem=512G
# Run for five minutes
#SBATCH --time=1:00:00
# Name of this job
#SBATCH --job-name=NNPredict
# Output of this job, stderr and stdout are joined by default
# %x=job-name %j=jobid
#SBATCH --output=%x_%j.out
# 
# change to the directory where you submitted this script
cd ${SLURM_SUBMIT_DIR}
#
# your job execution follows:
echo "Starting sbatch script myscript.sh at:`date`"
# echo some slurm variables for fun
echo "  running host:    ${SLURMD_NODENAME}"
echo "  assigned nodes:  ${SLURM_JOB_NODELIST}"
echo "  jobid:           ${SLURM_JOBID}"
# show me my assigned GPU number(s):
echo "  GPU(s):          ${CUDA_VISIBLE_DEVICES}"

./Voxelyze3 -i generation01/ -o output.xml -f
