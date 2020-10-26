variable "region" {
  # provide the your targeted region
  # refer here for list of regions https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html#Concepts.RegionsAndAvailabilityZones.Availability
  default = "ap-southeast-1"
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
  default = "rbs"
}
