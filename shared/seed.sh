#!/bin/bash
# Seed the emulator with demo resources. Run from HOST after emulator is up:
#   bash shared/seed.sh
# Requires: aws cli + emulator on http://localhost:4566
set -euo pipefail
EP="http://localhost:4566"
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1

aws --endpoint-url="$EP" s3 mb s3://dojo-bucket
aws --endpoint-url="$EP" sqs create-queue --queue-name dojo-queue
aws --endpoint-url="$EP" dynamodb create-table --table-name Dojo \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

echo "Seeded: s3://dojo-bucket, dojo-queue, Dojo table."
