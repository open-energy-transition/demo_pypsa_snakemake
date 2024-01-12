input_dir = snakemake.input[0]
output_dir = snakemake.output[0]
rule=snakemake.rule

import os

import kubernetes
import yaml
from kubernetes import client, config, utils


print(input_dir)
print(output_dir)
print(kubernetes.__version__)


config.load_kube_config()

yaml_file = '/home/akshat/demo_pypsa_snakemake/kubernetes/k8-job.yaml'

k8s_client = client.ApiClient()

with open(yaml_file, 'r') as file:
    yaml_content = yaml.safe_load(file)


print(yaml_content)

# utils.create_from_yaml(k8s_client,yaml_file)
utils.create_from_dict(k8s_client,yaml_content)
# utils.create_from_yaml()