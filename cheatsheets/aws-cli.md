# AWS CLI Cheat Sheet (Cloud Dojo)

Every command needs endpoint + credentials + region. Against the emulator:
`export AWS_ENDPOINT_URL=http://localhost:4566 AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1`
then drop `--endpoint-url` everywhere below.

## Config
```bash
aws --version
aws configure list                  # which credential source is active
export AWS_ENDPOINT_URL=http://localhost:4566   # all services → emulator
export AWS_ENDPOINT_URL_S3=http://localhost:4566  # per-service override
```

## S3 (object storage)
```bash
aws --endpoint-url=$AWS_ENDPOINT_URL s3 mb s3://my-bucket
aws --endpoint-url=$AWS_ENDPOINT_URL s3 cp file.txt s3://my-bucket/
aws --endpoint-url=$AWS_ENDPOINT_URL s3 ls s3://my-bucket/
aws --endpoint-url=$AWS_ENDPOINT_URL s3 cp s3://my-bucket/file.txt .
aws --endpoint-url=$AWS_ENDPOINT_URL s3 rm s3://my-bucket/file.txt
aws --endpoint-url=$AWS_ENDPOINT_URL s3 sync ./data s3://my-bucket/data
```

## SQS (queues) + SNS (topics)
```bash
aws --endpoint-url=$EP sqs create-queue --queue-name q
aws --endpoint-url=$EP sqs send-message --queue-url URL --message-body "hi"
aws --endpoint-url=$EP sqs receive-message --queue-url URL     # note ReceiptHandle
aws --endpoint-url=$EP sqs delete-message --queue-url URL --receipt-handle H
aws --endpoint-url=$EP sns create-topic --name t
aws --endpoint-url=$EP sns subscribe --topic-arn ARN --protocol sqs --notification-endpoint QARN
aws --endpoint-url=$EP sns publish --topic-arn ARN --message "hi"
```
Delete only after successful processing (at-least-once delivery).

## DynamoDB (NoSQL)
```bash
aws --endpoint-url=$EP dynamodb create-table --table-name T \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST
aws --endpoint-url=$EP dynamodb put-item --table-name T --item '{"id":{"S":"1"}}'
aws --endpoint-url=$EP dynamodb get-item --table-name T --key '{"id":{"S":"1"}}'
aws --endpoint-url=$EP dynamodb scan --table-name T            # whole table: learning only
aws --endpoint-url=$EP dynamodb list-tables
```

## Lambda + ECR
```bash
aws --endpoint-url=$EP lambda create-function --function-name f --package-type Image \
  --code ImageUri=localhost.localstack.cloud:4510/repo:tag --role arn:aws:iam::000000000000:role/r
aws --endpoint-url=$EP lambda invoke --function-name f --payload '{"name":"ada"}' out.json && cat out.json
aws ecr create-repository --repository-name repo              # real ECR (sandbox)
```

## Output shaping
```bash
aws ... --query 'Buckets[].Name' --output table
aws ... --query 'Reservations[].Instances[].PublicIpAddress' --output text
```

## IAM (real AWS only — emulators don't enforce)
```bash
aws iam create-user --user-name alice
aws iam create-group --group-name readers
aws iam add-user-to-group --group-name readers --user-name alice
aws iam attach-group-policy --group-name readers --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

*From the [Cloud Dojo](../README.md) Phase 1–5 path. Full lessons in `phase-01/` through `phase-05/`.*
