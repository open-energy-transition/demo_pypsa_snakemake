# Project Usage Guide

This guide provides instructions on how to use the project locally, with Docker, on a VM, and in Kubernetes.

## Use Locally

To run the project locally:

1. Create an environment using `env.yaml`.
2. Activate the environment.
3. Execute Snakemake commands:
    - `snakemake --cores 1 calculate_sum`
    - `snakemake --cores 1 prepare_networks`
    - `snakemake --cores 1 solve_networks`
4. To remove folders and run again:
    - `sudo rm -r results/`
    - `sudo rm -r prepared_networks/`

## How To Use With Docker

If you have Docker installed:

1. Build the Docker image:
    - `docker build -t demo-pypsa .`
2. Run the Docker container:
    - `docker run --name democontainer -v "$(pwd)"/input:/input -v "$(pwd)"/results:/results --rm demo_pypsa`
    - This will create a Docker container, run `snakemake --cores 1 calculate_sum`, and remove it after writing result files using bind mounts.
3. For interactive mode:
    - `sudo docker run -it --entrypoint /bin/bash demo-pypsa`
    - It will start a container of this image with Conda activated in it.
4. For later use in Kubernetes, tag and push the image to a Docker registry. Modify the YAML file in the Kubernetes folder and `solve-tmpl` in the root folder accordingly.

## GCloud Setup

GCloud setup is required to further run this project.

## VM Usage

1. Execute the VM runner script:
    - `bash vm_stuff/runner.sh input-dir output-dir rule-name`
    - `bash vm_stuff/runner.sh network_config prepared_networks prepare_networks`
2. This command sequence will:
    - Create a VM.
    - Install Docker on it.
    - Clone our repo (any version is possible).
    - Build our Docker image from the downloaded repo.
    - Copy our `input.txt` from the local machine to the VM.
    - Run a container that uses our input, solves it, and writes results to `network.txt`.
    - Download results.
    - Delete the VM.
3. Images can be used directly, and multiple images can be tested easily using Docker, streamlining development.

## Kubernetes

1. Set up a cluster as per [Google Cloud Persistent Volumes documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/cloud-storage-fuse-csi-driver) or get access to our cluster.
2. Configure `kubectl` to use the GCP cluster.
3. Use `bash kubernetes/executer.sh input-dir output-dir rule-name bucket-name` for running jobs.
4. `executor.sh` will create a bucket and then upload the input.
5. Use `bash kubernetes/executer.sh network_config prepared_networks prepare_networks different-name-two` for different configurations.
6. `job-executer.py` reads `k8-job-template.yaml`, describing a job, overriding rules for input and output directories for bind mounts.
7. Follow the logs to monitor job execution and download results upon completion.

## Multiple Jobs

1. After running the `prepare_network` rule, you will have multiple files in the `prepared_networks` directory.
2. Execute `bash parallel-jobs.sh` to create multiple jobs in Kubernetes in parallel.
3. This script creates a folder named `pre-k8-jobs` and multiple YAML files from `k8-solve-job-tmpl`.
4. Apply these files to create jobs.
5. Monitor jobs and pods using `kubectl get jobs` and `kubectl get pods`.
