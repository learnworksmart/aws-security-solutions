terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }

  backend "s3" {
    bucket = "rbs-terraform-state"
    key    = "aws-config-terraform.tfstate"
    region = "ap-southeast-1"
    dynamodb_table = "rbs-terraform-locks"
    ### --- Reduce cost --- 
    encrypt = false
  }
}

# Configure the AWS Provider
provider "aws" {
  region                  = var.region
  shared_credentials_file = var.awscredfile
  profile                 = var.awsprofile
}

data "terraform_remote_state" "base" {
  backend  = "s3"
  config = {
    bucket = "rbs-terraform-state"
    key    = "base-terraform.tfstate"
    region = "ap-southeast-1"
  }
}
