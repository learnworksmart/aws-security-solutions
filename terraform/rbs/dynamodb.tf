resource "aws_dynamodb_table" "rbs_terraform_locks" {
  hash_key = "LockID"
  name = "rbs-terraform-locks"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags    = { 
    Name      = "${var.project}-terraform-locks"
    Project   = var.project
  }
}
