mkdir ./pre-k8-jobs
for file in "$(pwd)"/prepared_networks/*
do
    
    base_name=$(basename "$file")
    file_name="${base_name%.*}"

    echo "File Name: $file_name"

    if [ "$file_name" == "done" ]; then
        continue
    fi

    gcloud storage buckets create gs://bucket-$file_name-volume --uniform-bucket-level-access

    gcloud storage cp $file gs://bucket-$file_name-volume/prepared_networks/$base_name
    gcloud storage cp "$(pwd)"/prepared_networks/done.txt  gs://bucket-$file_name-volume/prepared_networks/done.txt

    cat k8-solve-job-tmpl.yaml | sed "s/\$ITEM/$file_name/" > ./pre-k8-jobs/job-$file_name.yaml
done
kubectl create -f ./pre-k8-jobs