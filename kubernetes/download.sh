OUTPUT_FILE=$1
OUTPUT_DIR_NAME=$(dirname "$OUTPUT_FILE")

BUCKET_NAME=$2

echo "output dir: $OUTPUT_DIR_NAME"

echo downloading results from $BUCKET_NAME

gcloud storage cp --recursive gs://$BUCKET_NAME/$OUTPUT_DIR_NAME/ "$(pwd)"/