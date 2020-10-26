# check for EC2 Ubuntu18 ssm-agent service
# sudo systemctl status snap.amazon-ssm-agent.amazon-ssm-agent.service
resource "aws_instance" "ec2_inspec_scan_webserver" {
  # Amazon Linux 2 AMI (HVM), SSD Volume Type (64-bit x86)
  #ami                    = "ami-015a6758451df3cb9"
  # Ubuntu 18.04
  ami                    = "ami-0c8e97a27be37adfd"
  instance_type          = "t2.micro"
  iam_instance_profile   = aws_iam_instance_profile.ec2.name
  key_name               = data.terraform_remote_state.base.outputs.aws_key_pair_base.key_name
  # ### --- Reduce cost --- 
  # subnet_id              = data.terraform_remote_state.base.outputs.aws_subnet_base.id
  vpc_security_group_ids = [data.terraform_remote_state.base.outputs.aws_security_group_base_allow_default.id]

  tags    = { 
    Name    = "${var.project}-webserver"
    OS      = "Ubuntu 18.04"
    Project = var.project
  }
}

resource "aws_instance" "ec2_inspec_scan_nonwebserver" {
  # Amazon Linux 2 AMI (HVM), SSD Volume Type (64-bit x86)
  #ami                    = "ami-015a6758451df3cb9"
  # Ubuntu 18.04
  ami                    = "ami-0c8e97a27be37adfd"
  instance_type          = "t2.micro"
  iam_instance_profile   = aws_iam_instance_profile.ec2.name
  key_name               = data.terraform_remote_state.base.outputs.aws_key_pair_base.key_name
  # ### --- Reduce cost --- 
  # subnet_id              = data.terraform_remote_state.base.outputs.aws_subnet_base.id
  vpc_security_group_ids = [data.terraform_remote_state.base.outputs.aws_security_group_base_allow_default.id]

  tags    = { 
    Name    = "${var.project}-nonwebserver"
    OS      = "Ubuntu 18.04"
    Project = var.project
  }
}
