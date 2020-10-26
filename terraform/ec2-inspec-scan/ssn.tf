# resource "aws_sns_topic" "ec2_inspec_scan" {
#   name = var.project

#   tags      = { 
#     Name    = "${var.project}-sns"
#     Project = var.project
#   }
# }
# # Terraform's aws_sns_topic_subscription does not support `email` notification as 
# # the endpoint needs to be authorized and does not generate an ARN until the target email address has been validated. 
# # This breaks the Terraform model and as a result are not currently supported.
# # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_subscription

# # as such, we will manual configured the email subscription via web console.

# resource "aws_sns_topic_policy" "ec2_inspec_scan" {
#   arn    = aws_sns_topic.ec2_inspec_scan.arn
#   policy = data.aws_iam_policy_document.ec2_inspec_scan.json
# }

# data "aws_iam_policy_document" "ec2_inspec_scan" {
#   statement {
#     effect  = "Allow"
#     actions = ["SNS:Publish"]

#     principals {
#       type        = "Service"
#       identifiers = ["events.amazonaws.com"]
#     }

#     resources = [aws_sns_topic.ec2_inspec_scan.arn]
#   }
# }
