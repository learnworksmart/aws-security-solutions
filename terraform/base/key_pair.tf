resource "aws_key_pair" "base" {
  key_name   = "${var.project}_key_pair"
  public_key = file(var.pubkey)

  tags    = { 
    Name  = "${var.project}-key-pair"
    Project  = var.project
  }
}
