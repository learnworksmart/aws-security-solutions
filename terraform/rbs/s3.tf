resource "aws_s3_bucket" "rbs_terraform_state" {
  bucket = "rbs-terraform-state"
  acl    = "private"

  lifecycle {
    ### --- set to true for LIVE env ---
    prevent_destroy = false
  }

  versioning {
    ### --- set to true for LIVE env ---
    enabled = false
  }

  ### --- Reduce cost ---
  # server_side_encryption_configuration {
  #   rule {
  #     apply_server_side_encryption_by_default {
  #       kms_master_key_id = aws_kms_key.rbs_key.arn
  #       sse_algorithm     = "aws:kms"
  #     }
  #   }
  # }

  tags = {
    Name    = "${var.project}-terraform-state"
    Project = var.project
  }
}

resource "aws_s3_bucket_public_access_block" "rbs_terraform_state" {
  bucket = aws_s3_bucket.rbs_terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
