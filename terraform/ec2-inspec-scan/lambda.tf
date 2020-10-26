resource "aws_lambda_function" "ec2_inspec_scan" {
  #data.terraform_remote_state.base.outputs.aws_s3_bucket_base.bucket
  #depends_on        = [aws_lambda_layer_version.lambda_layer, data.archive_file.ec2_inspec_scan]
  depends_on        = [data.archive_file.ec2_inspec_scan]
  layers            = [data.terraform_remote_state.base.outputs.aws_lambda_layer_version_base.arn]
  filename          = data.archive_file.ec2_inspec_scan.output_path
  function_name     = var.project
  role              = aws_iam_role.ahdoc_scan.arn
  handler           = "ec2-inspec-scan.main"
  source_code_hash  = data.archive_file.ec2_inspec_scan.output_base64sha256
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

resource "aws_lambda_permission" "ec2_inspec_scan" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ec2_inspec_scan.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ec2_inspec_scan.arn
}

# resource "aws_lambda_layer_version" "lambda_layer" {
#   depends_on          = [null_resource.install_python_dependencies_locally, data.archive_file.lambda_layer]
#   filename            = data.archive_file.lambda_layer.output_path
#   layer_name          = "${var.project}-lambda-layer"
#   compatible_runtimes = ["python3.8", "python3.7", "python3.6"]
#   source_code_hash    = data.archive_file.lambda_layer.output_base64sha256
# }

# #download the python dependencies onto our local machine
# resource "null_resource" "install_python_dependencies_locally" {
#   triggers = {
#     always_run = "${timestamp()}"
#   }
  
#   provisioner "local-exec" {
#     command = "pip3 install -r ${var.source_code_path}/requirements.txt --target ${var.source_code_path}/packages"
#   }
# }

# #Create an archive file for lambda layer
# data "archive_file" "lambda_layer" {
#   depends_on  = [null_resource.install_python_dependencies_locally]
#   type        = "zip"
#   #target source-code folder
#   source_dir  = var.source_code_path
#   output_path = "lambda-layer.zip"
# }

#Create an archive file for ec2-inspec-scan
locals {
  source_files = [
    "${var.source_code_path}/ec2-inspec-scan.py", 
    "${var.source_code_path}/.env"
  ]
}

data "template_file" "ec2_inspec_scan" {
  count = "${length(local.source_files)}"
  template = "${file(element(local.source_files, count.index))}"
}

data "archive_file" "ec2_inspec_scan" {
  type        = "zip"
  output_path = "ec2-inspec-scan.zip"

  source {
    filename = "${basename(local.source_files[0])}"
    content  = "${data.template_file.ec2_inspec_scan.0.rendered}"
  }

  source {
    filename = "${basename(local.source_files[1])}"
    content  = "${data.template_file.ec2_inspec_scan.1.rendered}"
  }
}

### <--- monthly alert on non-compliant records found --->
resource "aws_lambda_function" "monthly_alert" {
  #depends_on        = [aws_lambda_layer_version.lambda_layer, data.archive_file.ec2_inspec_scan]
  #layers            = [aws_lambda_layer_version.lambda_layer.arn]
  layers            = [data.terraform_remote_state.base.outputs.aws_lambda_layer_version_base.arn]
  filename          = data.archive_file.monthly_update.output_path
  function_name     = "monthly-alert"
  role              = aws_iam_role.monthly_alert.arn
  handler           = "monthly-alert.main"
  source_code_hash  = data.archive_file.monthly_update.output_base64sha256
  runtime           = "python3.8"
  timeout           = 900

  tags      = { 
    Name    = "${var.project}-monthly-alert"
    Project = var.project
  }

  environment {
    variables = {
      LAMBDA = "True"
    }
  }
}

resource "aws_lambda_permission" "monthly_alert" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.monthly_alert.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.monthly_alert.arn
}

locals {
  source_files_monthly_alert = [
    "${var.source_code_path}/monthly-alert.py", 
    "${var.source_code_path}/.env"
  ]
}

data "template_file" "monthly_alert" {
  count = "${length(local.source_files_monthly_alert)}"
  template = "${file(element(local.source_files_monthly_alert, count.index))}"
}

data "archive_file" "monthly_update" {
  type        = "zip"
  output_path = "monthly_update.zip"

  source {
    filename = "${basename(local.source_files_monthly_alert[0])}"
    content  = "${data.template_file.monthly_alert.0.rendered}"
  }

  source {
    filename = "${basename(local.source_files_monthly_alert[1])}"
    content  = "${data.template_file.monthly_alert.1.rendered}"
  }
}
