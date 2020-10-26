resource "aws_lambda_function" "aws_config" {
  #data.terraform_remote_state.base.outputs.aws_s3_bucket_base.bucket
  #depends_on        = [aws_lambda_layer_version.lambda_layer, data.archive_file.ec2_inspec_scan]
  depends_on        = [data.archive_file.aws_config]
  layers            = [data.terraform_remote_state.base.outputs.aws_lambda_layer_version_base.arn]
  filename          = data.archive_file.aws_config.output_path
  function_name     = var.project
  role              = aws_iam_role.lambda_aws_config.arn #
  handler           = "aws-config.main"
  source_code_hash  = data.archive_file.aws_config.output_base64sha256
  runtime           = "python3.8"
  timeout           = 900

  tags      = { 
    Name    = "${var.project}"
    Project = var.project
  }

  environment {
    variables = {
      LAMBDA = "True"
    }
  }
}

resource "aws_lambda_permission" "aws_config" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aws_config.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.aws_config.arn
}

#Create an archive file for aws-config
locals {
  source_files = [
    "${var.source_code_path}/aws-config.py", 
    "${var.source_code_path}/.env"
  ]
}

data "template_file" "aws_config" {
  count = "${length(local.source_files)}"
  template = "${file(element(local.source_files, count.index))}"
}

data "archive_file" "aws_config" {
  type        = "zip"
  output_path = "aws-config.zip"

  source {
    filename = "${basename(local.source_files[0])}"
    content  = "${data.template_file.aws_config.0.rendered}"
  }

  source {
    filename = "${basename(local.source_files[1])}"
    content  = "${data.template_file.aws_config.1.rendered}"
  }
}

# ### <--- CUSTOM AWS CONFIG RULE ---> 
# resource "aws_lambda_function" "custom" {
#   #data.terraform_remote_state.base.outputs.aws_s3_bucket_base.bucket
#   #depends_on        = [aws_lambda_layer_version.lambda_layer, data.archive_file.ec2_inspec_scan]
#   depends_on        = [data.archive_file.custom]
#   layers            = [data.terraform_remote_state.base.outputs.aws_lambda_layer_version_base.arn]
#   filename          = data.archive_file.custom.output_path
#   function_name     = "${var.project}-custom"
#   role              = aws_iam_role.lambda_aws_config.arn #
#   handler           = "custom-aws-config.main"
#   source_code_hash  = data.archive_file.custom.output_base64sha256
#   runtime           = "python3.8"
#   timeout           = 900

#   tags      = { 
#     Name    = "${var.project}-custom"
#     Project = var.project
#   }

#   environment {
#     variables = {
#       LAMBDA = "True"
#     }
#   }
# }

# resource "aws_lambda_permission" "custom" {
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.custom.arn
#   principal     = "config.amazonaws.com"
#   statement_id  = "AllowExecutionFromConfig"
# }

# locals {
#   custom_source_files = [
#     "${var.source_code_path}/custom-aws-config.py", 
#     "${var.source_code_path}/.env"
#   ]
# }

# data "template_file" "custom" {
#   count = "${length(local.custom_source_files)}"
#   template = "${file(element(local.custom_source_files, count.index))}"
# }

# data "archive_file" "custom" {
#   type        = "zip"
#   output_path = "custom-aws-config.zip"

#   source {
#     filename = "${basename(local.custom_source_files[0])}"
#     content  = "${data.template_file.custom.0.rendered}"
#   }

#   source {
#     filename = "${basename(local.custom_source_files[1])}"
#     content  = "${data.template_file.custom.1.rendered}"
#   }
# }
