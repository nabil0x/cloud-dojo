# Terraform Cheat Sheet (Cloud Dojo)

Declare desired state. Read the plan. Then — only then — apply.

## Daily loop
```bash
terraform init                    # providers + modules, once per clone
terraform fmt                     # canonical formatting
terraform validate                # syntax + schema check, no cloud needed
terraform plan                    # THE diff: read every line
terraform plan -out=tfplan        # save an approved plan
terraform apply "tfplan"          # execute exactly what you approved
terraform apply                   # re-plans live (fine for learning)
terraform destroy                 # tear it all down (type yes by hand)
```

## HCL essentials
```hcl
terraform {
  required_providers { aws = { source = "hashicorp/aws" } }
}
variable "bucket_name" { type = string }          # input
output "bucket_arn" { value = aws_s3_bucket.d.arn }  # output

resource "aws_s3_bucket" "d" {                   # type + local name
  bucket = var.bucket_name
}
```
Reference anything as `aws_TYPE.NAME.attr`. Count/for_each scale repetition.

## State (ownership lives here)
```bash
terraform state list
terraform state show aws_s3_bucket.d
terraform import aws_sqs_queue.q http://localhost:4566/000000000000/q
terraform state mv old new           # rename without destroy
terraform taint aws_x.y              # force recreation next apply
```
Never hand-edit state. `.tfstate` holds secrets in plaintext — backends + `sensitive = true` for teams.

## Emulator provider pattern
```hcl
provider "aws" {
  region = "us-east-1"; access_key = "test"; secret_key = "test"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
  endpoints { s3 = "http://localhost:4566"; sqs = "http://localhost:4566" }
}
```
Same config hits real AWS by deleting `endpoints` + using real creds.

## Plan reading checklist
- `+ create`, `~ update in-place`, `-/+ destroy then create` (force-new: names, AZs)
- `forces replacement` on anything with data → stop and think
- Unexpected destroys → wrong directory/backend/branch. Do not apply.

*From the [Cloud Dojo](../README.md) Phase 6 path. Full lesson in `phase-06-terraform-iac/`.*
