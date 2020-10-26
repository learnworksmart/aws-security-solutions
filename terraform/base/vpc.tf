# ### --- Reduce cost --- 

# resource "aws_vpc" "base" {
#   cidr_block       = var.cidr_block
#   # A tenancy option for instances launched into the VPC. 
#   # Default is default, which makes your instances shared on the host. 
#   # Using either of the other options (dedicated or host) costs at least $2/hr.
#   instance_tenancy = "default"

#   tags = {
#     Name = "${var.project}_vpc"
#     Project  = var.project
#   }
# }

# resource "aws_subnet" "base" {
#   vpc_id                  = aws_vpc.base.id
#   cidr_block              = var.subnet
#   map_public_ip_on_launch = "true"

#   tags = {
#     Name = "${var.project}_subnet"
#     Project = var.project
#   }
# }
# resource "aws_internet_gateway" "base" {
#   vpc_id = aws_vpc.base.id

#   tags = {
#     Name = "${var.project}_gw"
#     Project = var.project
#   }
# }
# resource "aws_default_route_table" "base" {
#   default_route_table_id = aws_vpc.base.default_route_table_id
#   route {
#     cidr_block = "0.0.0.0/0"
#     gateway_id = aws_internet_gateway.base.id
#   }

#   tags = {
#     Name = "${var.project}_default_route_table"
#     Project = var.project
#   }
# }

# resource "aws_vpc_endpoint" "base_ssm" {
#   vpc_id       = aws_vpc.base.id
#   service_name = "com.amazonaws.${var.region}.ssm"
#   vpc_endpoint_type = "Interface"
#   subnet_ids = [aws_subnet.base.id]
#   security_group_ids = [aws_security_group.base_allow_default.id]

#   tags = {
#     Name = "${var.project}_ssm_vpc_endpoint"
#     Project = var.project
#   }
# }
