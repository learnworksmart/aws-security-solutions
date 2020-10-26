resource "aws_cloudwatch_event_rule" "aws_config" {
  name        = var.project
  description = "Capture AWS Config when a compliance check fails"
  schedule_expression = var.cron

  tags    = { 
    Name    = "${var.project}"
    Project = var.project
  }
}

resource "aws_cloudwatch_event_target" "aws_config" {
  rule      = aws_cloudwatch_event_rule.aws_config.name
  arn       = aws_lambda_function.aws_config.arn
}

resource "aws_cloudwatch_log_group" "aws_config" {
  name = "/aws/lambda/${aws_lambda_function.aws_config.function_name}"
  retention_in_days = 14

  tags      = { 
    Name    = var.project
    Project = var.project
  }
}

# resource "aws_cloudwatch_log_group" "custom" {
#   name = "/aws/lambda/${aws_lambda_function.custom.function_name}"
#   retention_in_days = 14

#   tags      = { 
#     Name    = var.project
#     Project = var.project
#   }
# }
