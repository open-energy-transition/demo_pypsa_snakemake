
gcloud compute instances create labrat \
    --project=stately-forest-407206 \
    --zone=us-west4-b \
    --machine-type=e2-standard-2 \
    --tags=http-server,https-server \
    --image-project=debian-cloud \
    --image-family=debian-10 \
    --metadata=enable-guest-attributes=TRUE \
    --metadata-from-file=startup-script=vm_config.sh


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

# we are copying aour config and getting results by binding directories for ~/ip/ in vm rather then ~/demo_pypsa_snakemake/ip/ because gcp dosent allow us to overwrite files and docker is also getting executed at ~/ rather then ~/demo_p_s as we do locally
# ~/ls = demo_pypsa_snakemake  input  results


gcloud compute scp --recurse "$(pwd)"/input/ labrat:~/input/ --zone=us-west4-b

gcloud compute ssh labrat \
    --command='sudo docker run -v ~/input/option.txt:/input/option.txt -v ~/results:/results demo-pypsa'  \
    --zone=us-west4-b 

gcloud compute scp --recurse labrat:~/results/ \
    "$(pwd)"/results/ \
    --zone=us-west4-b

gcloud compute instances delete labrat --zone=us-west4-b --quiet
