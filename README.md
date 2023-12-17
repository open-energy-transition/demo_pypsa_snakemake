
# INTRO

This is demo pypsa project which creates a env with just snakemake init
then we activate this env and excute our rule which inputs a file
writes the result to result folder
using bind mounts we can use our host filesystem to provide config and get results 
this conatiner will spin up and die only results which are bindmounted will survive 

# How To Use

if you have docker installed 

- docker build -t demo-pypsa .
- docker run --name democontainer -v "$(pwd)"/input:/input -v "$(pwd)"/results:/results --rm demo_pypsa

to remove folder and run again

- sudo rm -r results/

# CLOUD SOLVE

## gcloud setup is needed

- `bash runner.sh`

this command will 
 - create a VM
 - install docker on it
 - we git clones our repo (any version is possible)
 - build our docker image from downloaded repo
 - copy our input.txt from local machine to VM
 - runs a container uses our input then solves it and writes result/network.txt
 - we downloads results
 - delete the VM 

