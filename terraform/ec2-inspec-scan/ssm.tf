resource "aws_ssm_parameter" "github" {
  name        = "github"
  description = "Github authenticated access token for reading public repos"
  type        = "SecureString"
  value       = var.github_token

  tags      = { 
    Name    = "${var.project}-github-token"
    Project = var.project
  }
}

resource "aws_ssm_association" "ec2_inspec_scan" {
  name = "AWS-RunInspecChecks"
  association_name = var.project
  # https://docs.aws.amazon.com/systems-manager/latest/userguide/reference-cron-and-rate-expressions.html
  #every day it runs at 10am (UTC)
  schedule_expression = "cron(0 10 * * ? *)"
  # #run every 1 hours
  # schedule_expression = "cron(0 0/1 * * ? *)"

  targets {
    key    = "InstanceIds"
    # The wildcard specify all instances found in ssm inventory.
    values = ["*"]
  }

  parameters = {
    sourceType = "GitHub"
    sourceInfo = jsonencode(local.source_info)
  }

  ##The output_location code block is for ssm to output its execution logs to S3 bucket. These log is not really required at this moment.
  # output_location {
  #   s3_bucket_name = data.terraform_remote_state.base.outputs.aws_s3_bucket_base.bucket
  #   s3_key_prefix = var.project
  # }
} 

# locals {
#   source_info = {
#     owner      = "awslabs"
#     repository = "amazon-ssm"
#     path       = "Compliance/InSpec/PortCheck"
#     getOptions = "branch:master"
#     tokenInfo  = "{{ssm-secure:${aws_ssm_parameter.github.name}}}"
#   }
# }

locals {
  source_info = {
    owner      = "learnworksmart"
    repository = "private_inspec"
    path       = "inspec"
    getOptions = "branch:full"
    tokenInfo  = "{{ssm-secure:${aws_ssm_parameter.github.name}}}"
  }
}

# resource "aws_ssm_parameter" "slack" {
#   name        = "slack"
#   description = "Slack OAuth access token for posting alerts to our slack alert channel."
#   type        = "SecureString"
#   value       = var.slack_token

#   tags      = { 
#     Name    = "${var.project}-slack-token"
#     Project = var.project
#   }
# }
