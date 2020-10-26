### This IAM role is for aws config 
resource "aws_iam_role_policy_attachment" "aws_config" {
  role       = aws_iam_role.aws_config.name
  #https://docs.aws.amazon.com/config/latest/developerguide/iamrole-permissions.html#iam-trust-policy
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWS_ConfigRole"
}

resource "aws_iam_role_policy_attachment" "aws_config2" {
  role       = aws_iam_role.aws_config.name
  policy_arn = aws_iam_policy.aws_config.arn
}

resource "aws_iam_role" "aws_config" {
  name = "aws-config"
  description = "This role is created for ${var.project}."
  assume_role_policy = data.aws_iam_policy_document.aws_config_assume_role.json

  tags      = { 
    Name    = "aws-config"
    Project = var.project
  }
}

resource "aws_iam_policy" "aws_config" {
  name        = "aws-config"
  policy      = data.aws_iam_policy_document.aws_config_access_rights.json
  path        = "/"
  description = "This policy is created for ${var.project}."
}

data "aws_iam_policy_document" "aws_config_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["config.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "aws_config_access_rights" {
  statement {
      #wildcard is required to resolve this error: 
      #Error: Creating Delivery Channel failed: InsufficientDeliveryPolicyException: 
      #Insufficient delivery policy to s3 bucket: base-store-outputs, unable to write to bucket, provided s3 key prefix is 'null'.
      effect    = "Allow"
      actions   = ["s3:*"]
      resources = ["*"]     
  }
}

### This IAM role is for aws_config lambda function
resource "aws_iam_role_policy_attachment" "lambda_aws_config" {
  role       = aws_iam_role.lambda_aws_config.name
  policy_arn = aws_iam_policy.lambda_aws_config.arn
}

resource "aws_iam_role" "lambda_aws_config" {
  name = "${var.project}-4-lambda"
  description = "This role is created for ${var.project} aws config lambda function."
  assume_role_policy = data.aws_iam_policy_document.lambda_aws_config_assume_role.json

  tags      = { 
    Name    = "${var.project}-4-lambda"
    Project = var.project
  }
}

resource "aws_iam_policy" "lambda_aws_config" {
  name        = "${var.project}-4-lambda"
  policy      = data.aws_iam_policy_document.lambda_aws_config_access_rights.json
  path        = "/"
  description = "This policy is created for ${var.project} adhoc scan lambda function."
}

data "aws_iam_policy_document" "lambda_aws_config_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_aws_config_access_rights" {
  statement {
      effect    = "Allow"
      actions   = ["s3:PutObject"]
      resources = ["${data.terraform_remote_state.base.outputs.aws_s3_bucket_base.arn}/*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["logs:CreateLogStream","logs:CreateLogGroup","logs:PutLogEvents"]
      resources = ["*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["config:Get*"]
      resources = ["*"]    
  }
  statement {
      effect    = "Allow"
      actions   = ["ssm:GetParameters"]
      resources = [data.terraform_remote_state.base.outputs.slack.arn]  
  }
}
