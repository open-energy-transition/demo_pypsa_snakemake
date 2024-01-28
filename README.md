
# Introduction

This project is conceived as a testbed for cloud strategy, which will later be used in PyPSA models. Due to the large image size of PyPSA, along with substantial data download times, we are using this to develop a cloud solution that fits PyPSA.

# USE LOCALLY

- create env using env.yaml
- then activate it
  - `snakemake --cores 1 calculate_sum`
  - `snakemake --cores 1 prepare_networks`
  - `snakemake --cores 1 solve_networks`
- to remove folder and run again
  - `sudo rm -r results/`
  - `sudo rm -r prepared_networks/`

# How To Use With Docker

if you have docker installed

- `docker build -t demo-pypsa .`

- `docker run --name democontainer -v "$(pwd)"/input:/input -v "$(pwd)"/results:/results --rm demo_pypsa`

this will create a docker container run `snakemake --cores 1 calculate_sum`  and remove it after writing result files using bindmounts.

- `sudo docker run -it --entrypoint /bin/bash demo-pypsa`

it will start a container of this image with conda activated in it.

if you want to use you image later in kubernetes section tag and push it to docker registry and modify the yaml file in kubernetes folder and solve-tmpl in root folder.

# gcloud setup is needed to further run this project

# VM

- `bash vm_stuff/runner.sh input-dir output-dir rule-name`
- `bash vm_stuff/runner.sh network_config prepared_networks prepare_networks`

this command will

- create a VM
- install docker on it
- we git clones our repo (any version is possible)
- build our docker image from downloaded repo
- copy our input.txt from local machine to VM
- runs a container uses our input then solves it and writes result/network.txt
- we downloads results
- delete the VM

- we can also use our images directly.
- we can run or test multiple images easily using docker which will streamline development.

# Kubernetes

- to run this we have setup a cluster following these instructions[https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/cloud-storage-fuse-csi-driver]
- or get access to our cluster
- configure kubectl to use GCP cluster

- in k8 solution we will upload data directly to buckets,then use buckets as persistent volume claims.

- `bash kubernetes/executer.sh input-dir output-dir rule-name bucket-name`

- `bash kubernetes/executer.sh network_config prepared_networks prepare_networks different-name-two`

- executor.sh will create a bucket and then upload the input.
- We use the job-executer.py file to read k8-job-template.yaml, which describes a job.
- We override the rule for input and output directories, which will be bind-mounted.
- We send it to solve while we can follow the logs.
- Once solved, it will download the results.

## Multiple Jobs

- Once you have run the `prepare_network` rule, you should have a number of files in the `prepared_networks` directory.
- Execute `bash parallel-jobs.sh`.
- This script will create a folder named `pre-k8-jobs`.
- We create multiple YAML files in `pre-k8-jobs` from `k8-solve-job-tmpl` located in the root directory.
- We apply all of these files to create multiple jobs in Kubernetes in parallel.
- Use `kubectl get jobs` to view all the jobs.
- Use `kubectl get pods` to see the status of pods running.

# Kubernetes and Snakemake

## older version

- This example [Snakemake on Azure AKS](https://snakemake.readthedocs.io/en/v7.32.3/executor_tutorial/azure_aks.html) works fine on Kubernetes with an older version of Snakemake (< 8.0).
- However, I couldn't figure out how to pass environment variables to Snakemake, which in turn gets passed to the pod in the cluster.
- These environment variables allow the pod to write the results of running the rule to the bucket.
- I am manually passing the environment variable `GOOGLE_CLOUD_CREDENTIALS` in `sum_script.py` of the `calculate_sum` rule.
- You will need to make a service account with permissions specified [here](https://snakemake.readthedocs.io/en/v7.32.3/executor_tutorial/azure_aks.html).
- Once you have granted permissions, download the service account key and add it to the root folder as `key.json`.
- Create a bucket and upload the input file to it.
- Use the command `snakemake --kubernetes bucket-fuse --k8s-service-account-name bucket-account --default-remote-prefix bucket-name --default-remote-provider GS -j 1 calculate_sum`.
- This should get you the results in the bucket.

## new version

- not runing sucessfully
- latest command looks like this
- `snakemake --executor kubernetes --default-storage-provider gcs --default-storage-prefix  gcs://bucket-name -j 1 calculate_sum --storage-gcs-project stately-forest-407206 --kubernetes-namespace bucket-fuse`
- results in error Has the pod been delete manually.
  