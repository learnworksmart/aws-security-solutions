# Extract IAM
This project extracts IAM resources, such as user accounts, roles, groups and policies, to support assessment such as access reviews.

## High-Level Overview 

![image](https://user-images.githubusercontent.com/71627887/97108618-bd1ef800-1709-11eb-992f-03764523994a.png)

1. A CloudWatch rule is scheduled to trigger our `extract-iam` lambda function.
1. The `extract-iam` lambda function will:
    * extract the IAM resources and output to CSV files.
    * upload the CSV files to S3 bucket.  
1. Send Slack alerts, each attached with associated CSV file.

## Alert notification. 
Here is the sample alert received in our Slack channel.
![image](https://user-images.githubusercontent.com/71627887/97108897-60244180-170b-11eb-9425-fe3de8e0ddc7.png)

