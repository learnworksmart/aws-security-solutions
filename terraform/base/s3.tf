resource "aws_s3_bucket" "base" {
  bucket        = "${var.project}-store-outputs"
  acl           = "private"
  #This option allow us to destroy a S3 bucket even though it is not empty.
  #Lazy option, need to quick tear down and test again.
  force_destroy = true

  lifecycle {
    prevent_destroy = false
  }

  versioning {
    enabled = false
  }

  tags    = { 
    Name  = "${var.project}-store-outputs"
    Project  = var.project
  }
}

resource "aws_s3_bucket_public_access_block" "base" {
  bucket = aws_s3_bucket.base.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
