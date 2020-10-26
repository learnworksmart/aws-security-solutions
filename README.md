# Deploy Security Solutions on AWS Environment
This repository consists of security-related solutions for our AWS environment, and here is our progression:
1. The `rbs` project provides [remote-backend-state](https://www.terraform.io/docs/backends/types/s3.html) setup using S3 and DynamoDB.  
1. The `base` project hosts the common resources for our security-related projects: 
  1. The `ec2-inspec-scan` project provides configurations/hardening scans on our EC2 instances. 
  1. The `aws-config` project enabled selected AWS Config Rules and extract non-compliant resources. 
  1. The `extract-iam` project extracts IAM resources, such as user accounts, roles, groups, and policies, to support assessment such as access reviews.
  1. The `monitor` project search for selected AWS resources that are responsible for triggering the above projects. Such resources include:
      * System Manager Association
      * CloudWatch Rule
      * Config Rule

## How to Deploy?

**Prerequisite**
* [Install Terraform](https://www.terraform.io/downloads.html) on your local machine.
* [Install AWSCLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) on your local machine.  
* [Configure AWSCLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) on your local machine. 
  * [Generate the AWS programmatically token](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds) which is required for configuring our AWSCLI.
  * Attach the token with `AdministratorAccess` policy, which provides us administrative permission.

**Deployment Steps**
1. Clone this repository to your local machine. 
1. Browse to the `terraform` folders, in the following order, provide the required inputs in `variables.tf`, run `terraform init` and `terraform apply` to deploy our AWS setups.
  1. `rbs` for setting up remote-backend-state. 
  1. `base` for setting up common resources for the rest of the projects.
  1. `ec2-inspec-scan`, `aws-config`, `monitor` and `extract-iam` which are our security-related solutions. 
