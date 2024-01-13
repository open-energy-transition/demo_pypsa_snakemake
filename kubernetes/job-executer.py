input_dir = snakemake.input[0]
output_dir = snakemake.output[0]
rule=snakemake.rule

import os

import kubernetes
import yaml
from kubernetes import client, config, utils
import time
from kubernetes.stream import stream
import json

print(input_dir)
print(output_dir)
print(kubernetes.__version__)

nameSpace="bucket-fuse"

config.load_kube_config()
yaml_file = '/home/akshat/demo_pypsa_snakemake/kubernetes/k8-job.yaml'
k8s_client = client.ApiClient()

def get_pod_name_from_job(job_name, namespace='default'):
    core_v1 = client.CoreV1Api()
    pods = core_v1.list_namespaced_pod(namespace, label_selector=f"job-name={job_name}")
    if pods.items:
        return pods.items[0].metadata.name
    return None

def stream_pod_logs(pod_name, namespace='default'):
    core_v1 = client.CoreV1Api()
    # pod_log = core_v1.read_namespaced_pod_log(name=pod_name, namespace=namespace,container="cal-img" ,follow=True)
    pod_log = core_v1.read_namespaced_pod(name=pod_name, namespace=namespace )
    
    print(pod_log)


def is_container_running(pod_name, container_name, namespace='default'):
    core_v1 = client.CoreV1Api()
    pod = core_v1.read_namespaced_pod(pod_name, namespace)
    for container_status in pod.status.container_statuses:
        if container_status.name == container_name:
            return container_status.state.running is not None
    return False

def stream_container_logs(pod_name, container_name, namespace='default'):
    core_v1 = client.CoreV1Api()
    try:
        print(f"Attaching to container '{container_name}' in pod '{pod_name}'")
        resp = stream(core_v1.connect_get_namespaced_pod_exec, pod_name, namespace,
                      command=['/bin/sh', '-c', 'tail -f /var/log/some_log_file.log'],
                      container=container_name, stderr=True, stdin=False,
                      stdout=True, tty=False)
        for line in resp:
            print(line)
    except Exception as e:
        print(f"Error streaming logs: {e}")

def connect_to_container_when_ready(pod_name, container_name, namespace='default'):
    print(f"Waiting for container '{container_name}' in pod '{pod_name}' to start...")
    while not is_container_running(pod_name, container_name, namespace):
        time.sleep(5)
    stream_container_logs(pod_name, container_name, namespace)



with open(yaml_file, 'r') as file:
    yaml_content = yaml.safe_load(file)

try:
    utils.create_from_dict(k8s_client, yaml_content)
    job_name = yaml_content['metadata']['name']
    namespace = yaml_content.get('metadata', {}).get('namespace', 'default')

    pod_name=None
    
    while not pod_name:
        print("Waiting for pod to be created...")
        time.sleep(5)
        pod_name = get_pod_name_from_job(job_name, namespace)
    print(f"Pod {pod_name} created. Streaming logs...")
    # stream_pod_logs(pod_name, namespace)
    connect_to_container_when_ready(pod_name,'cal-img')

except kubernetes.client.exceptions.ApiException as e:
    print(f"An error occurred: {e}")


