INPUT_FILE=$1
INPUT_DIR_NAME=$(dirname "$INPUT_FILE")
echo "input dir: $INPUT_DIR_NAME"

BUCKET_NAME=$2

gcloud storage buckets create gs://$BUCKET_NAME --uniform-bucket-level-access

echo bucket $BUCKET_NAME created

sleep 10

gcloud storage cp --recursive "$(pwd)"/$INPUT_DIR_NAME/ gs://$BUCKET_NAME/