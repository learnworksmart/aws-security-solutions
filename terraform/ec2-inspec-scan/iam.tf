### This IAM role is assigned to ec2 instances for communication with ssm, cloudwatch and s3. 
resource "aws_iam_instance_profile" "ec2" {
  name = "${var.project}-4-ec2"
  role = aws_iam_role.ec2.name
}

resource "aws_iam_role_policy_attachment" "ec2" {
  role       = aws_iam_role.ec2.name
  policy_arn = aws_iam_policy.ec2.arn
}

resource "aws_iam_role" "ec2" {
  name               = "${var.project}-4-ec2"
  assume_role_policy = data.aws_iam_policy_document.ec2.json
  path               = "/"
  description        = "This role is created for ec2 instances"

  tags      = { 
    Name    = "${var.project}-4-ec2"
    Project = var.project
  }
}

resource "aws_iam_policy" "ec2" {
  name        = "${var.project}-4-ec2"
  policy      = file("ec2-ssm-iam-policy.json")
  path        = "/"
  description = "This policy is created for ec2 instances"
}

data "aws_iam_policy_document" "ec2" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

### This IAM role is for ec2-inspec-scan lambda function, to query SSM and write to S3 bucket & DynamoDB.
resource "aws_iam_role_policy_attachment" "ahdoc_scan" {
  role       = aws_iam_role.ahdoc_scan.name
  policy_arn = aws_iam_policy.ahdoc_scan.arn
}

resource "aws_iam_role" "ahdoc_scan" {
  name = "${var.project}-4-lambda-adhoc-scan"
  description = "This role is created for ${var.project} adhoc scan lambda function."
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags      = { 
    Name    = "${var.project}-4-lambda-adhoc-scan"
    Project = var.project
  }
}

resource "aws_iam_policy" "ahdoc_scan" {
  name        = "${var.project}-4-lambda-adhoc-scan"
  policy      = data.aws_iam_policy_document.ahdoc_scan_access_rights.json
  path        = "/"
  description = "This policy is created for ${var.project} adhoc scan lambda function."
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ahdoc_scan_access_rights" {
  statement {
      effect    = "Allow"
      actions   = ["ssm:GetInventory", "ssm:ListComplianceItems"]
      resources = ["*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["ssm:GetParameters"]
      #resources = [aws_ssm_parameter.slack.arn]   
      resources = [data.terraform_remote_state.base.outputs.slack.arn]  
  }
  statement {
      effect    = "Allow"
      actions   = ["logs:CreateLogStream","logs:CreateLogGroup","logs:PutLogEvents"]
      resources = ["*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["dynamodb:*"]
      resources = [aws_dynamodb_table.ec2_inspec_scan.arn]    
  }
}

### This IAM role is for monthly-alert lambda function, to query DynamoDB.
resource "aws_iam_role_policy_attachment" "monthly_alert" {
  role       = aws_iam_role.monthly_alert.name
  policy_arn = aws_iam_policy.monthly_alert.arn
}

resource "aws_iam_role" "monthly_alert" {
  name = "${var.project}-4-lambda-monthly-alert"
  description = "This role is created for ${var.project} monthly alert lambda function."
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags      = { 
    Name    = "${var.project}-4-lambda-monthly-alert"
    Project = var.project
  }
}

resource "aws_iam_policy" "monthly_alert" {
  name        = "${var.project}-4-lambda-monthly-alert"
  policy      = data.aws_iam_policy_document.monthly_alert_access_rights.json
  path        = "/"
  description = "This policy is created for ${var.project} monthly alert lambda function."
}

data "aws_iam_policy_document" "monthly_alert_access_rights" {
  statement {
      effect    = "Allow"
      actions   = ["ssm:GetParameters"]
      #resources = [aws_ssm_parameter.slack.arn]  
      resources = [data.terraform_remote_state.base.outputs.slack.arn] 
  }
  statement {
      effect    = "Allow"
      actions   = ["logs:CreateLogStream","logs:CreateLogGroup","logs:PutLogEvents"]
      resources = ["*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["s3:PutObject"]
      resources = ["${data.terraform_remote_state.base.outputs.aws_s3_bucket_base.arn}/*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["dynamodb:*"]
      resources = [aws_dynamodb_table.ec2_inspec_scan.arn]    
  }
}

### This IAM role is for cloudwatch rule to trigger ec2-inspec-scan lambda function.
resource "aws_iam_role_policy_attachment" "cloudwatch_rule" {
  role       = aws_iam_role.cloudwatch_rule.name
  policy_arn = aws_iam_policy.cloudwatch_rule.arn
}

resource "aws_iam_role" "cloudwatch_rule" {
  name = "${var.project}-4-cloudwatch-rule"
  description = "This role is created for ${var.project} cloudwatch rule."
  assume_role_policy = data.aws_iam_policy_document.cloudwatch_rule_assume_role.json

  tags      = { 
    Name    = "${var.project}-4-cloudwatch-rule"
    Project = var.project
  }
}

resource "aws_iam_policy" "cloudwatch_rule" {
  name        = "${var.project}-4-cloudwatch-rule"
  policy      = data.aws_iam_policy_document.cloudwatch_rule_access_rights.json
  path        = "/"
  description = "This policy is created for ${var.project} cloudwatch rule."
}

data "aws_iam_policy_document" "cloudwatch_rule_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "cloudwatch_rule_access_rights" {
  statement {
      effect    = "Allow"
      actions   = ["lambda:InvokeFunction"]
      resources = [aws_lambda_function.ec2_inspec_scan.arn]    
  }
}
