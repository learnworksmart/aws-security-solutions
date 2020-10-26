# AWS Config
This project enable selected [AWS Config Rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html) and uses Slack for sending alerts on resources which found non-compliant. 

## High-Level Overview 

![image](https://user-images.githubusercontent.com/71627887/96404244-0a343300-120d-11eb-84c7-e860c98aa3db.png)

1. A CloudWatch rule is scheduled to trigger our `aws-config` lambda function.
1. The `aws-config` lambda function will:
    * retrieve non-compliant resources from the selected AWS Config Rules. 
    * output the non-compliant resources in a CSV file and upload to S3 bucket.  
    * send a Slack alert on the afftected AWS Config rule, non-compliant resource and attached with the CSV file.  
1. If required, the team can also retrieve CSV files from our S3 bucket. 

## Alert notification. 
Here is the sample alert received in our Slack channel.
* `aws-config` with **non-compliant resources** found:
  ![image](https://user-images.githubusercontent.com/71627887/96404322-36e84a80-120d-11eb-996c-7de3337507df.png)
