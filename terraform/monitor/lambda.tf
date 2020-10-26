resource "aws_lambda_function" "monitor" {
  depends_on        = [data.archive_file.monitor]
  layers            = [data.terraform_remote_state.base.outputs.aws_lambda_layer_version_base.arn]
  filename          = data.archive_file.monitor.output_path
  function_name     = var.project
  role              = aws_iam_role.lambda_monitor.arn #
  handler           = "monitor.main"
  source_code_hash  = data.archive_file.monitor.output_base64sha256
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

resource "aws_lambda_permission" "monitor" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.monitor.arn
}

#Create an archive file for aws-config
locals {
  source_files = [
    "${var.source_code_path}/monitor.py", 
    "${var.source_code_path}/.env"
  ]
}

data "template_file" "monitor" {
  count = "${length(local.source_files)}"
  template = "${file(element(local.source_files, count.index))}"
}

data "archive_file" "monitor" {
  type        = "zip"
  output_path = "monitor.zip"

  source {
    filename = "${basename(local.source_files[0])}"
    content  = "${data.template_file.monitor.0.rendered}"
  }

  source {
    filename = "${basename(local.source_files[1])}"
    content  = "${data.template_file.monitor.1.rendered}"
  }
}
