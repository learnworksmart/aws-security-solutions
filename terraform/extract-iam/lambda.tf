resource "aws_lambda_function" "extract_iam" {
  depends_on        = [data.archive_file.extract_iam]
  layers            = [data.terraform_remote_state.base.outputs.aws_lambda_layer_version_base.arn]
  filename          = data.archive_file.extract_iam.output_path
  function_name     = var.project
  role              = aws_iam_role.lambda_extract_iam.arn #
  handler           = "extract-iam.main"
  source_code_hash  = data.archive_file.extract_iam.output_base64sha256
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

resource "aws_lambda_permission" "extract_iam" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extract_iam.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.extract_iam.arn
}

#Create an archive file for extract-iam
locals {
  source_files = [
    "${var.source_code_path}/extract-iam.py", 
    "${var.source_code_path}/.env"
  ]
}

data "template_file" "extract_iam" {
  count = "${length(local.source_files)}"
  template = "${file(element(local.source_files, count.index))}"
}

data "archive_file" "extract_iam" {
  type        = "zip"
  output_path = "extract-iam.zip"

  source {
    filename = "${basename(local.source_files[0])}"
    content  = "${data.template_file.extract_iam.0.rendered}"
  }

  source {
    filename = "${basename(local.source_files[1])}"
    content  = "${data.template_file.extract_iam.1.rendered}"
  }
}
