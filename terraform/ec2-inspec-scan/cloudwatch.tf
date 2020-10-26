resource "aws_cloudwatch_event_rule" "ec2_inspec_scan" {
  name        = var.project
  description = "Capture SSM Configuration Compliance State Change"

  #https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#SSM-Configuration-Compliance-event-types
  event_pattern = jsonencode(local.eventpattern)

  tags    = { 
    Name    = "${var.project}"
    Project = var.project
  }
}

resource "aws_cloudwatch_event_target" "ec2_inspec_scan" {
  rule      = aws_cloudwatch_event_rule.ec2_inspec_scan.name
  #arn       = aws_sns_topic.ec2_inspec_scan.arn
  arn       = aws_lambda_function.ec2_inspec_scan.arn
}

# Configuration Compliance State Change
# https://docs.amazonaws.cn/en_us/systems-manager/latest/userguide/reference-eventbridge-events.html
# The state of a managed instance changes, for either Association compliance or patch compliance. 
# You can add one or more of the following state changes to an event rule:
# 1. compliant & 2. non_compliant
locals {
  eventpattern  = {
    detail-type = ["EC2 State Manager Association State Change"]
    source      = ["aws.ssm"]
    detail      = {
      "status" = ["Success", "Failed"]  
    }
  }
}

resource "aws_cloudwatch_log_group" "ec2_inspec_scan" {
  name = "/aws/lambda/${aws_lambda_function.ec2_inspec_scan.function_name}"
  retention_in_days = 14

  tags      = { 
    Name    = "${var.project}"
    Project = var.project
  }
}

### <--- monthly alert on non-compliant records found --->
resource "aws_cloudwatch_event_rule" "monthly_alert" {
  name                = "monthly-alert"
  description         = "Provide Monthly Alert on the number of Non-Compliant configuration found on our EC2 instances registered with ssm-inventory."
  schedule_expression = var.cron

  tags    = { 
    Name    = "monthly-alert"
    Project = var.project
  }
}

resource "aws_cloudwatch_event_target" "monthly_alert" {
  rule      = aws_cloudwatch_event_rule.monthly_alert.name
  arn       = aws_lambda_function.monthly_alert.arn
}

resource "aws_cloudwatch_log_group" "monthly_alert" {
  name = "/aws/lambda/${aws_lambda_function.monthly_alert.function_name}"
  retention_in_days = 14

  tags      = { 
    Name    = "monthly-alert"
    Project = var.project
  }
}
