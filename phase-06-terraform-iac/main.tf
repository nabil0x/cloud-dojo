# Phase 6 starter skeleton — emulator-first Terraform.
# Flow: terraform init → plan (READ IT) → apply → destroy.
# The provider below is complete. The resources are YOUR quests (Q6.1, Q6.4).

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true

  # Same config targets the emulator AND real AWS — only endpoints change.
  endpoints {
    s3       = "http://localhost:4566"
    sqs      = "http://localhost:4566"
    sns      = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
  }
}

# TODO(Q6.1): define your first bucket. Uncomment and apply:
# resource "aws_s3_bucket" "dojo" {
#   bucket = "dojo-first-bucket"
# }

# TODO(Q6.2): parameterize the bucket name with a variable + terraform.tfvars,
# and expose the bucket ARN via an output block.

# TODO(Q6.4): add aws_sqs_queue "dojo", aws_sns_topic "dojo",
# aws_sns_topic_subscription, and aws_dynamodb_table "dojo" here.
# Then break one attribute on purpose and watch `plan` catch it.
