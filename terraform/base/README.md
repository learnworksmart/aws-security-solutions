# Base
`Base` is the first project to be applied after `rbs`. It aims to house the common resources used by other projects, e.g. `ec2-inspec-scan`. 

## Main Common Resources & Practice
1. [Lambda Layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html), which house the common libraries and 3rd-party dependencies used by other projects.
1. The following practices were adopted to minimize the changes required when running the python script locally or over lambda function: 
    1. Use **dotenv** to load environment variable from a common `.env` flat file, which is applicable on both local run and lambda. 
    1. Set a unique environment variable in the Lambda function, which serves as a flag for code blocks that are only applicable for either local run or lambda. 
1. Create a Slack Application to send alerts. Here are the requirements for the Slack Application: 
    * Generate its Bot User OAuth Access Token:
      * Refer [here](https://api.slack.com/legacy/oauth) for more information.
    * Assign with the following permissions: 
      * [chat:write](https://api.slack.com/scopes/chat:write) for posting message to Slack Channel. 
      * [files:write](https://api.slack.com/scopes/files:write) for uploading any attachment.
    * [Invite](https://slack.com/intl/en-sg/help/articles/202035138-Add-an-app-to-your-workspace) it to our desire Slack workspace and channel, where we will received the Slack Alert notifications. 
 