resource "aws_cloudwatch_event_rule" "monitor" {
  name        = var.project
  description = "Scheduled Run to monitor security service resources."
  schedule_expression = var.cron

  tags    = { 
    Name    = "${var.project}"
    Project = var.project
  }
}

resource "aws_cloudwatch_event_target" "monitor" {
  rule      = aws_cloudwatch_event_rule.monitor.name
  arn       = aws_lambda_function.monitor.arn
}

resource "aws_cloudwatch_log_group" "monitor" {
  name = "/aws/lambda/${aws_lambda_function.monitor.function_name}"
  retention_in_days = 14

  tags      = { 
    Name    = var.project
    Project = var.project
  }
}
