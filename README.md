This is demo pypsa project which creates a env with just snakemake init
then we activate this env and excute our rule which inputs a file
writes the result to result folder
using bind mounts we can use our host filesystem to provide config and get results 
this conatiner will spin up and die only results which are bindmounted will survive 
