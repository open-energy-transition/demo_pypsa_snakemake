

INPUT_FILE=$1
INPUT_DIR_NAME=$(dirname "$INPUT_FILE")
echo "input dir: $INPUT_DIR_NAME"

gcloud storage buckets create gs://bucket-python-volume --uniform-bucket-level-access
echo bucket created
gcloud storage cp --recursive "$(pwd)"/input gs://bucket-python-volume/input 