# #https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html
resource "aws_config_config_rule" "S3_BUCKET_VERSIONING_ENABLED" {
  name = "S3_BUCKET_VERSIONING_ENABLED"
  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_VERSIONING_ENABLED"
  }
  depends_on = [aws_config_configuration_recorder.aws_config, aws_config_delivery_channel.aws_config]
}

resource "aws_config_config_rule" "CLOUDWATCH_LOG_GROUP_ENCRYPTED" {
  name = "CLOUDWATCH_LOG_GROUP_ENCRYPTED"
  source {
    owner             = "AWS"
    source_identifier = "CLOUDWATCH_LOG_GROUP_ENCRYPTED"
  }
  depends_on = [aws_config_configuration_recorder.aws_config, aws_config_delivery_channel.aws_config]
}

resource "aws_config_config_rule" "LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED" {
  name = "LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED"
  source {
    owner             = "AWS"
    source_identifier = "LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED"
  }
  depends_on = [aws_config_configuration_recorder.aws_config, aws_config_delivery_channel.aws_config]
}

resource "aws_config_config_rule" "EC2_INSTANCE_MANAGED_BY_SSM" {
  name = "EC2_INSTANCE_MANAGED_BY_SSM"
  source {
    owner             = "AWS"
    source_identifier = "EC2_INSTANCE_MANAGED_BY_SSM"
  }
  depends_on = [aws_config_configuration_recorder.aws_config, aws_config_delivery_channel.aws_config]
}

resource "aws_config_delivery_channel" "aws_config" {
  name           = var.project
  s3_bucket_name = data.terraform_remote_state.base.outputs.aws_s3_bucket_base.bucket
  s3_key_prefix  = var.project
  depends_on = [aws_config_configuration_recorder.aws_config]
}

resource "aws_config_configuration_recorder" "aws_config" {
  name     = var.project
  role_arn = aws_iam_role.aws_config.arn
  
}

resource "aws_config_configuration_recorder_status" "aws_config" {
  name       = aws_config_configuration_recorder.aws_config.name
  is_enabled = true
  depends_on = [aws_config_delivery_channel.aws_config]
}

## <--- CUSTOM AWS CONFIG RULE ---> 
# resource "aws_config_config_rule" "custom" {
#   name = "${var.project}-custom"
#   source {
#     owner             = "CUSTOM_LAMBDA"
#     source_identifier = aws_lambda_function.custom.arn
#     source_detail {
#       event_source                = "aws.config" 
#       maximum_execution_frequency = "TwentyFour_Hours"
#       #message_type = "ConfigurationItemChangeNotification"
#       message_type                = "ScheduledNotification"
#     }
#   }

#   scope {
#     compliance_resource_types = ["AWS::EC2::Instance"]
#   }

#   depends_on = [
#     aws_config_configuration_recorder.aws_config,
#     aws_lambda_permission.custom,
#   ]
# }
