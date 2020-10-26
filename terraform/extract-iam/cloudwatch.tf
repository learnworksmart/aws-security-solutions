resource "aws_cloudwatch_event_rule" "extract_iam" {
  name        = var.project
  description = "Scheduled Run to extract_iam security service resources."
  schedule_expression = var.cron

  tags    = { 
    Name    = "${var.project}"
    Project = var.project
  }
}

resource "aws_cloudwatch_event_target" "extract_iam" {
  rule      = aws_cloudwatch_event_rule.extract_iam.name
  arn       = aws_lambda_function.extract_iam.arn
}

resource "aws_cloudwatch_log_group" "extract_iam" {
  name = "/aws/lambda/${aws_lambda_function.extract_iam.function_name}"
  retention_in_days = 14

  tags      = { 
    Name    = var.project
    Project = var.project
  }
}
