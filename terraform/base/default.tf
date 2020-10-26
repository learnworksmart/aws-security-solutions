# #<-- to reduce the cost for vpc-endpoint, the base setup will be automatically assigned with public addresses.
# resource "aws_default_vpc" "default" {
#   enable_dns_support = true
# }
# #disable public ip on launch on all 3 default subnet's regions.
# resource "aws_default_subnet" "default_a" {
#   availability_zone = "${var.region}a"
#   map_public_ip_on_launch = true
# }

# resource "aws_default_subnet" "default_b" {
#   availability_zone = "${var.region}b"
#   map_public_ip_on_launch = true
# }

# resource "aws_default_subnet" "default_c" {
#   availability_zone = "${var.region}c"
#   map_public_ip_on_launch = true
# }

# #lauch ec2 instance without public IP address.
# resource "aws_instance" "test" {
#   # Amazon Linux 2 AMI (HVM), SSD Volume Type (64-bit x86)
#   #ami                    = "ami-015a6758451df3cb9"
#   # Ubuntu 18.04
#   ami                         = "ami-0c8e97a27be37adfd"
#   instance_type               = "t2.micro"
#   key_name                    = aws_key_pair.base.key_name
#   vpc_security_group_ids      = [aws_security_group.base_allow_default.id]
#   #disable public IP
#   associate_public_ip_address = false

#   tags    = { 
#     Name    = "${var.project}-webserver"
#     OS      = "Ubuntu 18.04"
#     Project = var.project
#   }
# }
