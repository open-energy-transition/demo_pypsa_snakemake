input_dir = snakemake.input[0]
output_dir = snakemake.output[0]
rule=snakemake.rule

import os

import kubernetes
import yaml
from kubernetes import client, config, utils
import time
from kubernetes.stream import stream
import subprocess
import os

bucket_name='aksjsj'

script_path = '/home/akshat/demo_pypsa_snakemake/kubernetes/upload.sh'

subprocess.run(['chmod', '+x', script_path])

subprocess.run(["bash",script_path,input_dir])

###################

config.load_kube_config()
yaml_file = '/home/akshat/demo_pypsa_snakemake/kubernetes/k8-job.yaml'
k8s_client = client.ApiClient()


def get_job_status(job_name, namespace='default'):
    batch_v1_api = client.BatchV1Api()
    try:
        job = batch_v1_api.read_namespaced_job(job_name, namespace)
        status = job.status
        print(f"{job_name} status")
        print(f"active: {status.active}")
        print(f"ready: {status.ready}")
        print(f"succeeded: {status.succeeded}")
        print("\n")
        return status.succeeded

    except client.exceptions.ApiException as e:
        return f"Error: {e}", None

def get_pods_for_job(job_name, namespace='default'):
    core_v1_api = client.CoreV1Api()
    label_selector = f"job-name={job_name}"
    pods = core_v1_api.list_namespaced_pod(namespace, label_selector=label_selector)
    
    return pods.items

def get_pod_status(pod):
    status = pod.status
    print(f"Pod Name: {pod.metadata.name}")
    print(f"Phase: {status.phase}")
    
    for container_status in status.container_statuses:
        print(f"Container Name: {container_status.name}")
        print(f" State: {container_status.state}")            
        
    print("\n")
    
with open(yaml_file, 'r') as file:
    yaml_content = yaml.safe_load(file)

try:
    utils.create_from_dict(k8s_client, yaml_content)
    job_name = yaml_content['metadata']['name']
    namespace = yaml_content.get('metadata', {}).get('namespace', 'default')
    print(yaml_content)

    finished=False
    while not finished:
        finished=get_job_status(job_name,namespace)
        pods=get_pods_for_job(job_name,namespace)
        if pods[0] is not None:
            container_status=get_pod_status(pods[0])
        time.sleep(3)
        
except kubernetes.client.exceptions.ApiException as e:
    print(f"An error occurred: {e}")


