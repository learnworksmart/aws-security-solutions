resource "aws_ssm_parameter" "slack" {
  name        = "slack"
  description = "Slack OAuth access token for posting alerts to our slack alert channel."
  type        = "SecureString"
  value       = var.slack_token

  tags      = { 
    Name    = "${var.project}-slack-token"
    Project = var.project
  }
}
