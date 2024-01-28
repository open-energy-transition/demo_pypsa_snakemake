INPUT_DIR_NAME=$1
OUTPUT_DIR_NAME=$2
RULE_NAME=$3


echo "input dir: $INPUT_DIR_NAME"
echo "output dir: $OUTPUT_DIR_NAME"
echo "rule name: $RULE_NAME"

echo creating your VM....
gcloud compute instances create labrat \
    --project=stately-forest-407206 \
    --zone=us-west4-b \
    --machine-type=e2-standard-2 \
    --tags=http-server,https-server \
    --image-project=debian-cloud \
    --image-family=debian-10 \
    --metadata=enable-guest-attributes=TRUE \
    --metadata-from-file=startup-script=vm_stuff/boot.sh
    #  --container-image=akshatmittaloet/demo-pypsa \
    # --container-restart-policy=always \
    # https://cloud.google.com/compute/docs/containers/configuring-options-to-run-containers

until gcloud compute instances get-guest-attributes labrat \
    --zone=us-west4-b \
    --query-path=vm/ready > /dev/null 2>&1
do
    sleep 5 && echo waiting for VM to boot...
done


gcloud compute ssh labrat \
    --command='sudo docker run hello-world'  \
    --zone=us-west4-b 

gcloud compute ssh labrat \
    --command='sudo git clone https://github.com/drifter089/demo_pypsa_snakemake.git'  \
    --zone=us-west4-b 

gcloud compute ssh labrat \
    --command='sudo docker build -t demo-pypsa ./demo_pypsa_snakemake/'  \
    --zone=us-west4-b 

gcloud compute ssh labrat \
    --command='sudo docker images'  \
    --zone=us-west4-b 


# ~/ls = demo_pypsa_snakemake  input  results prepared_networks

gcloud compute scp --recurse "$(pwd)"/$INPUT_DIR_NAME/ labrat:~/$INPUT_DIR_NAME/ --zone=us-west4-b

SNAKEMAKE_COMMAND="snakemake --cores 1 $RULE_NAME"
DOCKER_COMMAND="sudo docker run -v ~/$INPUT_DIR_NAME/:/$INPUT_DIR_NAME/ -v ~/$OUTPUT_DIR_NAME:/$OUTPUT_DIR_NAME --entrypoint /bin/bash demo-pypsa -c '$SNAKEMAKE_COMMAND'"

gcloud compute ssh labrat \
    --command="$DOCKER_COMMAND"  \
    --zone=us-west4-b 

gcloud compute scp --recurse labrat:~/$OUTPUT_DIR_NAME/ \
    "$(pwd)"/ \
    --zone=us-west4-b


echo deleting VM this will take a while.....
gcloud compute instances delete labrat --zone=us-west4-b --quiet
