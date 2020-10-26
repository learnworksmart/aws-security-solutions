resource "aws_security_group" "base_allow_default" {
  name        = "base-allow-default"
  description = "Allow ssh and http(s) inbound traffic"
  # ### --- Reduce cost --- 
  # vpc_id      = aws_vpc.base.id

  tags = {
    Name = "${var.project}-allow-default"
    Project  = var.project
  }
}

resource "aws_security_group_rule" "base_ingress_port22" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.base_allow_default.id
}

resource "aws_security_group_rule" "base_ingress_port80" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.base_allow_default.id
}

resource "aws_security_group_rule" "base_egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.base_allow_default.id
}
