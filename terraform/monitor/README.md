# Monitor
This project monitors our security-services with selected AWS resources. For example:
1. Search the `ec2-inspec-scan` triggers, which make up of SSM association and CloudWatch.
1. Search the `aws-config` triggers, which make up of AWS Config Rules & CloudWatch.
1. Search the `extract-iam` trigger, which is CloudWatch.

## High-Level Overview 

![image](https://user-images.githubusercontent.com/71627887/97109535-bb0b6800-170e-11eb-83c9-12372f1c9a8a.png)

1. A CloudWatch rule is scheduled to trigger our `monitor` lambda function.
1. The `monitor` lambda function will check for the selected resources' existence, via `Name`, and output to a CSV file.
1. Send a Slack alert, attached with the CSV file.  

## Alert notification. 
Here is the sample alert received in our Slack channel.
![image](https://user-images.githubusercontent.com/71627887/96721051-2e933980-13de-11eb-8526-c71e45fdb3d0.png)
