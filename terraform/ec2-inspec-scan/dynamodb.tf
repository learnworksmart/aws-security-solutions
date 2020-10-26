resource "aws_dynamodb_table" "ec2_inspec_scan" {
  hash_key = "md5hash"
  name = var.project
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "md5hash"
    type = "S"
  }

  tags    = { 
    Name      = "${var.project}"
    Project   = var.project
  }
}
