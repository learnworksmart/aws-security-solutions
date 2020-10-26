variable "region" {
  # provide the your targeted region
  # refer here for list of regions https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html#Concepts.RegionsAndAvailabilityZones.Availability
  default = "ap-southeast-1"
}

variable "pubkey" {
  # provide the public key which will be used for accessing the ec2 instance
  # default = "<path to your local public key>"
  default = "$HOME/.ssh/learnworksmart.pub"
}

variable "awscredfile" {
  # provide your aws credential file, which usually found in $HOME/.aws/credentials
  #default = "<path to your local aws credential file>"
  default = "$HOME/.aws/credentials"
}

variable "awsprofile" {
  # if you have multiple aws profile configured on your local machine and the target is non-default, do provide the targeted AWS profile. 
  #default = "<targeted aws profile>"
  default = "default"
}

variable "project" {
  default = "aws-config"
}

#the local source code file which is to be deployed in lambda.
variable "source_code_path" {
  default = "../../source-code"
}

#cron schedule for cloudwatch rule to trigger the aws-config lambda function.
variable "cron" {
  # #run every 30 mins
  # default = "cron(0/15 * * * ? *)"
  #10:15 AM on the last Friday of every month
  default = "cron(15 10 ? * 6L *)"
}
