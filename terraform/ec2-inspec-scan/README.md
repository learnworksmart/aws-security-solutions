# Automated InSpec-Scan on AWS EC2
This project aims to carry our automated configuration scans on our EC2 instances, which also address our compliance and security requirements. 

We have introduce 2 Lambda functions to carry out the following tasks: 
1. The `ec2-inspec-scan` will:
	1. Extract the non-compliant configurations found from the latest scan performed by **AWS System Manager**. 
	1. Compare the latest scan result with the stored non-compliant configurations found in our database. 
	1. If there is any new non-compliant configurations found: 
		1. add them into the database
		1. output them into a CSV file. 
	1. Remove any stored non-compliant configurations, which cannot be found from the latest scan.
	1. Send a Slack alert message with a CSV attachment which consists of new non-compliant configurations found.  
1. The `monthly-alert` will:
	1. Extract all the stored non-compliant configurations found in our database. 
	1. Send a Slack alert message with a CSV attachment which consists all non-compliant configurations found. 
	1. Upload the CSV file into S3 Bucket. 

Here are the main components: 
1. **AWS System Manager**, trigger our `ec2-inspec-scan` lambda function whenever it run InSpec scan. 
1. **AWS CloudWatch**, scheduled to trigger our `monthly-alert` lambda function.
1. **Chef InSpec** is the review scripts where we will specify the desire configurations' state.
1. **AWS Lambda** hosts our python scripts which carried out the task mentioned in both `ec2-inspec-scan` and `monthly-alert`.  
1. **DynamoDB** stores non-compliant configurations found.
1. **S3** stores the `monthly-alert` CSV files. 

## High-Level Overview 

![image](https://user-images.githubusercontent.com/71627887/96331843-1b593480-1093-11eb-84e7-86805fea950e.png)

1. In the AWS System Manager (SSM), we create an association with [AWS-RunInspecChecks](https://aws.amazon.com/blogs/mt/using-aws-systems-manager-to-run-compliance-scans-using-inspec-by-chef/) Command Document which run InSpec scans on all EC2 instances that are installed with [SSM-agent](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html). 
	* The InSpec scans' result can be found on the SSM Compliance page or extract with the [AWS CLI list-compliance-items](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/list-compliance-items.html) 
	* For this project, our SSM association will be downloading the InSpec scripts stored in the GitHub repository. As such, we will need to generate a [GitHub Token](https://aws.amazon.com/blogs/mt/run-scripts-stored-in-private-or-public-github-repositories-using-amazon-ec2-systems-manager/) for SSM to authenticate with GitHub. 
1. After the association has been executed, regardless of success/failed, SSM will trigger the CloudWatch & EventBridge. 
1. The CloudWatch & EventBridge will: 
	* Trigger `ec2-inspec-scan` Lambda Function, when receieve [EC2 State Manager Association State Change](https://docs.amazonaws.cn/en_us/systems-manager/latest/userguide/reference-eventbridge-events.html) from SSM. 
	* Trigger `monthly-alert` Lambda Function, based on configured CloudWatch Rule cron job. 
1. Here are the expected end result from both Lambda Functions:
	* `ec2-inspec-scan` will send a Slack alert, with CSV attachment for any new non-compliant configurations found. 
	* `monthly-alert` send a Slack alert, with CSV attachment for all stored non-compliant configurations found. It will also upload its CSV file into S3 Bucket.
1. Based on the received Slack alert message, the team can carry out the necessary follow-up actions. 	
1. If required, the team can also retrieve CSV files from our S3 bucket.  

## Non-compliant Configuration records stored in DynamoDB
Each non-compliant configuration consists of:
* The affected `EC2 instance-id`. 
* The affected `non-compliant title`, which is determined by our InSpec Scripts' title input for each control.
* Primary key which is the MD5 sum of (`EC2 instance-id` + `non-compliant title`).

## Alert notification. 
Here are the sample alerts received in our Slack channel.
* `inspec-scan` with **new non-compliant configurations** found:
	![image](https://user-images.githubusercontent.com/71627887/96331568-df24d480-1090-11eb-95cb-5804e0342a91.png)
* `inspec-scan` without **new non-compliant configurations** found:
	![image](https://user-images.githubusercontent.com/71627887/96331602-29a65100-1091-11eb-98e7-ee052e2a35d6.png)
* `monthly-alert` with **all non-compliant configurations** found:
	![image](https://user-images.githubusercontent.com/71627887/96331636-640fee00-1091-11eb-99a6-ec0c517f72d5.png)
	
## Considerations and Possible enhancements
* Consider a possible situation where we need to snooze alert on a specific EC2 instance and/or non-compliant configurations. 
* Possible integration with our future Security Dashboard, e.g. Security Hub. 
