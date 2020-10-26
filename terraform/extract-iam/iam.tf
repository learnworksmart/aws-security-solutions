### This IAM role is for extract_iam lambda function
resource "aws_iam_role_policy_attachment" "lambda_extract_iam" {
  role       = aws_iam_role.lambda_extract_iam.name
  policy_arn = aws_iam_policy.lambda_extract_iam.arn
}

resource "aws_iam_role" "lambda_extract_iam" {
  name = "${var.project}-4-lambda"
  description = "This role is created for ${var.project} lambda function extract_iam ."
  assume_role_policy = data.aws_iam_policy_document.lambda_extract_iam_assume_role.json

  tags      = { 
    Name    = "${var.project}-4-lambda"
    Project = var.project
  }
}

resource "aws_iam_policy" "lambda_extract_iam" {
  name        = "${var.project}-4-lambda"
  policy      = data.aws_iam_policy_document.lambda_extract_iam_access_rights.json
  path        = "/"
  description = "This policy is created for ${var.project} lambda function extract_iam ."
}

data "aws_iam_policy_document" "lambda_extract_iam_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_extract_iam_access_rights" {
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
  statement {
      effect    = "Allow"
      actions   = ["iam:Get*"]
      resources = ["*"]  
  }
  statement {
      effect    = "Allow"
      actions   = ["s3:PutObject"]
      resources = ["${data.terraform_remote_state.base.outputs.aws_s3_bucket_base.arn}/*"]    
  }
}
