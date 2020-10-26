### This IAM role is for aws_config lambda function
resource "aws_iam_role_policy_attachment" "lambda_monitor" {
  role       = aws_iam_role.lambda_monitor.name
  policy_arn = aws_iam_policy.lambda_monitor.arn
}

resource "aws_iam_role" "lambda_monitor" {
  name = "${var.project}-4-lambda"
  description = "This role is created for ${var.project} lambda function monitor ."
  assume_role_policy = data.aws_iam_policy_document.lambda_monitor_assume_role.json

  tags      = { 
    Name    = "${var.project}-4-lambda"
    Project = var.project
  }
}

resource "aws_iam_policy" "lambda_monitor" {
  name        = "${var.project}-4-lambda"
  policy      = data.aws_iam_policy_document.lambda_monitor_access_rights.json
  path        = "/"
  description = "This policy is created for ${var.project} lambda function monitor ."
}

data "aws_iam_policy_document" "lambda_monitor_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_monitor_access_rights" {
  statement {
      effect    = "Allow"
      actions   = ["logs:CreateLogStream","logs:CreateLogGroup","logs:PutLogEvents"]
      resources = ["*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["config:Describe*", "ssm:List*"]
      resources = ["*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["ssm:GetParameters"]
      resources = [data.terraform_remote_state.base.outputs.slack.arn]  
  }
}
