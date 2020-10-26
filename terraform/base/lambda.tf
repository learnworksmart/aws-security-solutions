resource "aws_lambda_layer_version" "base" {
  depends_on          = [null_resource.install_python_dependencies_locally, data.archive_file.base]
  filename            = data.archive_file.base.output_path
  layer_name          = "${var.project}-lambda-layer"
  compatible_runtimes = ["python3.8", "python3.7", "python3.6"]
  source_code_hash    = data.archive_file.base.output_base64sha256
}

#download the python dependencies onto our local machine
resource "null_resource" "install_python_dependencies_locally" {
  triggers = {
    always_run = "${timestamp()}"
  }
  
  provisioner "local-exec" {
    command = "pip3 install -r ${var.source_code_path}/requirements.txt --target ${var.source_code_path}/packages"
  }
}

#Create an archive file for lambda layer
data "archive_file" "base" {
  depends_on  = [null_resource.install_python_dependencies_locally]
  type        = "zip"
  #target source-code folder
  source_dir  = var.source_code_path
  output_path = "lambda-layer.zip"
}
