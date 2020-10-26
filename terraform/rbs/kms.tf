# ## --- Reduce cost --- 
# resource "aws_kms_key" "rbs_key" {
#   description             = "This key is used to encrypt bucket objects"
#   # Duration in days after which the key is deleted after destruction of the resource
#   deletion_window_in_days = 7

#   tags = {
#     Name    = "${var.project}-key"
#     Project = var.project
#   }
# }
