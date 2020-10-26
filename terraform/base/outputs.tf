output "aws_key_pair_base" {
  value       = aws_key_pair.base
  description = "The uploaded public key pair for setting up SSH key authentication"
}

# ### --- Reduce cost --- 
# output "aws_subnet_base" {
#   value       = aws_subnet.base
#   description = "Our base VPC subnet"
# }

output "aws_security_group_base_allow_default" {
  value       = aws_security_group.base_allow_default
  description = "Our base default security group"
}

output "aws_s3_bucket_base" {
  value       = aws_s3_bucket.base
  description = "Our base S3 bucket"
}

output "aws_lambda_layer_version_base" {
  value       = aws_lambda_layer_version.base
  description = "Lambda layer for other Lambda Functions"
}

output "slack" {
  value       = aws_ssm_parameter.slack
  description = "Slack OAuth access token for posting alerts to our slack alert channel."
}
