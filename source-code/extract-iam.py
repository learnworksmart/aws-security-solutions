#!/usr/bin/env python3
import boto3, os, sys, csv, re
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/packages')
import logging
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
#switch back to /opt for the "shared" folder which consists our class files.
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/')
from shared.iam import iam
from shared.iam_account_record import iam_account_record
from shared.iam_role_record import iam_role_record
from shared.iam_group_record import iam_group_record
from shared.iam_policy_record import iam_policy_record
from shared.alerts import alerts
from shared.ssm import ssm
from shared.s3 import s3

#load environment variables from .env. Applicable for both local and lambda runs. 
load_dotenv()

#gloabl variables, type of IAM
PASSWORD_POLICY="Password Policy"
LIST_USERS="User Accounts"
LIST_ROLES="Roles"
LIST_GROUPS="Groups"
LIST_LOCAL_POLICY="in-use Local Policy"
LIST_AWS_POLICY="in-use AWS Policy"

def prepare_alert_message(type, count):
  now=datetime.now(timezone(os.getenv("TIMEZONE")))
  date_stamp=now.strftime('%d-%b-%Y')
  time_stamp=now.strftime('%H:%M:%S')
  title =("*[Extract IAM for reviews] :oncoming_police_car: Extracted IAM %s.*\n" % type)
  message = title
  message += "- Ran on (date): " + "`" +date_stamp + "`" + "\n"
  message += "- Ran on (time): " + "`" +time_stamp + "`" + "\n"
  if count > 0: 
    message += ("*Num of IAM %s found*: `%i`" % (type, count))
  else:
    message += ("*NO IAM %s found.*" % type)
  return(message)

def output2csv(type, inputs): 
  output_file = None
  if type == PASSWORD_POLICY: 
    output_file = "/tmp/%s" % str(os.getenv("EXTRACT_IAM_PASSWORD_POLICY_ALERT_CSV"))
    export = open(output_file, mode='w')
    writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for x in inputs:      
      writer.writerow([x,inputs[x]])
    export.close()
    return output_file
  elif type == LIST_USERS: 
    output_file = "/tmp/%s" % str(os.getenv("EXTRACT_IAM_ACCOUNT_ALERT_CSV"))
    export = open(output_file, mode='w')
    writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["PathPrefix", "UserName", "UserId", "Arn", "CreateDate", "GroupList", "AttachedManagedPolicies", "Tags"])
    for x in inputs:    
      writer.writerow([x.path, x.username, x.userid, x.arn, x.createdate, x.grouplist, x.attachedmanagepolicies, x.tags])
    export.close()
  elif type == LIST_ROLES:
    output_file = "/tmp/%s" % str(os.getenv("EXTRACT_IAM_ROLES_ALERT_CSV"))
    export = open(output_file, mode='w')
    writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["PathPrefix", "RoleName", "RoleId", "Arn", "CreateDate","AssumeRolePolicyDocument","InstanceProfileList","RolePolicyList","AttachedManagedPolicies","Tags","RoleLastUsed"])
    for x in inputs:
      writer.writerow([x.path, x.rolename, x.roleid, x.arn, x.createdate, x.assumerolepolicydocument, x.instanceprofilelist, x.rolepolicylist,x.attachedmanagedpolicies,x.tags,x.rolelastused])
    export.close()
  elif type == LIST_GROUPS:
      output_file = "/tmp/%s" % str(os.getenv("EXTRACT_IAM_GROUPS_ALERT_CSV"))
      export = open(output_file, mode='w')
      writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(["PathPrefix", "GroupName", "GroupId", "Arn", "CreateDate","GroupPolicyList","AttachedManagedPolicies"])
      for x in inputs:
        writer.writerow([x.path, x.groupname, x.groupid, x.arn, x.createdate, x.grouppolicylist, x.attachedmanagedpolicies])
      export.close()
  elif type == LIST_LOCAL_POLICY:
      output_file = "/tmp/%s" % str(os.getenv("EXTRACT_IAM_LOCAL_POLICY_ALERT_CSV"))
      export = open(output_file, mode='w')
      writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(["PolicyName", "PolicyId", "Arn", "Path","DefaultVersionId","AttachmentCount", "PermissionsBoundaryUsageCount", "IsAttachable", "CreateDate", "UpdateDate", "PolicyVersionList"])
      for x in inputs:
        writer.writerow([x.policyname, x.policyid, x.arn, x.path, x.defaultversionid, x.attachmentcount, x.permissionsboundaryusagecount, x.isattachable, x.createdate,x.updatedate,x.policyversionlist])
      export.close()
  elif type == LIST_AWS_POLICY:
      output_file = "/tmp/%s" % str(os.getenv("EXTRACT_IAM_AWS_POLICY_ALERT_CSV"))
      export = open(output_file, mode='w')
      writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      writer.writerow(["PolicyName", "PolicyId", "Arn", "Path","DefaultVersionId","AttachmentCount", "PermissionsBoundaryUsageCount", "IsAttachable", "CreateDate", "UpdateDate", "PolicyVersionList"])
      for x in inputs:
        writer.writerow([x.policyname, x.policyid, x.arn, x.path, x.defaultversionid, x.attachmentcount, x.permissionsboundaryusagecount, x.isattachable, x.createdate,x.updatedate,x.policyversionlist])
      export.close()
  return output_file
 
def main(event, lambda_context):
  logging.info('Starting Lambda')
  error_count = 0
  print("event: ", event)
  print("lambda_context: ", lambda_context)

  call_iam = iam()
  call_alerts = alerts(ssm().get_parameter("slack"))
  call_s3 = s3(os.getenv("BUCKET_NAME"))
  
  #(1)extract password policy
  password_policy_response = call_iam.get_account_password_policy()
  #output CSV file for storing password_policy_csv
  password_policy_csv = None
  #if password_policy_response == None, (1)Error encountered when trying to retrieve password policy, which could be due to password policy is not configured!
  if password_policy_response != None: 
    password_policy_csv = output2csv(PASSWORD_POLICY, password_policy_response['PasswordPolicy'])
    upload_filename = str(os.getenv("EXTRACT_IAM")) + "/"
    upload_filename += str(password_policy_csv)[5:]
    call_s3.upload_file(password_policy_csv, upload_filename)
    password_policy_response = 1
  else:
    password_policy_response = 0
  message = prepare_alert_message(PASSWORD_POLICY, password_policy_response)
  call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, password_policy_csv)
  
  #(2)extract list of user accounts
  account_response = call_iam.get_account_authorization_details("User")
  parse_account = []
  account_csv_file = None
  if len(account_response) > 0 and account_response != None: 
    for x in account_response:
      for y in x['UserDetailList']:
        #print(y['Path'], y['UserName'],y['UserId'],y['Arn'],y['CreateDate'],y['GroupList'],y['AttachedManagedPolicies'],y['Tags'])
        parse_account.append(iam_account_record(y['Path'], y['UserName'],y['UserId'],y['Arn'],y['CreateDate'],y['GroupList'],y['AttachedManagedPolicies'],y['Tags']))
    account_csv_file =  output2csv(LIST_USERS, parse_account)
    upload_filename = str(os.getenv("EXTRACT_IAM")) + "/"
    upload_filename += str(account_csv_file)[5:]
    call_s3.upload_file(account_csv_file, upload_filename)
  message = prepare_alert_message(LIST_USERS, len(parse_account))
  call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, account_csv_file)

  #(3)extract list of roles
  role_response = call_iam.get_account_authorization_details("Role")
  parse_role = []
  role_csv_file = None
  if len(role_response) > 0 and role_response != None :
    for x in role_response:
      for y in x['RoleDetailList']:
        #print(y['Path'], y['RoleName'],y['RoleId'],y['Arn'],y['CreateDate'],y['AssumeRolePolicyDocument'],y['InstanceProfileList'],y['RolePolicyList'],y['AttachedManagedPolicies'],y['Tags'],y['RoleLastUsed'])
        parse_role.append(iam_role_record(y['Path'], y['RoleName'],y['RoleId'],y['Arn'],y['CreateDate'],y['AssumeRolePolicyDocument'],y['InstanceProfileList'],y['RolePolicyList'],y['AttachedManagedPolicies'],y['Tags'],y['RoleLastUsed']))
    role_csv_file =  output2csv(LIST_ROLES, parse_role)
    upload_filename = str(os.getenv("EXTRACT_IAM")) + "/"
    upload_filename += str(role_csv_file)[5:]
    call_s3.upload_file(role_csv_file, upload_filename)
  message = prepare_alert_message(LIST_ROLES, len(parse_role))
  call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, role_csv_file)

  #(4)extract list of groups
  group_response = call_iam.get_account_authorization_details("Group")
  parse_group = []
  group_csv_file = None
  if len(group_response) > 0 and group_response != None:
    for x in group_response:
      for y in x['GroupDetailList']:
        #print(y['Path'],y['GroupName'],y['GroupId'],y['Arn'],y['CreateDate'],y['GroupPolicyList'],y['AttachedManagedPolicies'])
        parse_group.append(iam_group_record(y['Path'],y['GroupName'],y['GroupId'],y['Arn'],y['CreateDate'],y['GroupPolicyList'],y['AttachedManagedPolicies']))
    group_csv_file =  output2csv(LIST_GROUPS, parse_group)
    upload_filename = str(os.getenv("EXTRACT_IAM")) + "/"
    upload_filename += str(group_csv_file)[5:]
    call_s3.upload_file(group_csv_file, upload_filename)
  message = prepare_alert_message(LIST_GROUPS, len(parse_group))
  call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, group_csv_file)

  #(5)extract list of LocalManagedPolicy
  local_managed_policy_response = call_iam.get_account_authorization_details("LocalManagedPolicy")
  parse_local_managed_policy = []
  local_managed_policy_csv_file = None
  if len(local_managed_policy_response) > 0 and local_managed_policy_response != None:
    for x in local_managed_policy_response:
      for y in x ['Policies']:
        #print(y['PolicyName'],y['PolicyId'],y['Arn'],y['Path'],['DefaultVersionId'],y['AttachmentCount'],y['PermissionsBoundaryUsageCount'],y['IsAttachable'],y['CreateDate'],y['UpdateDate'],y['PolicyVersionList'])
        parse_local_managed_policy.append(iam_policy_record(y['PolicyName'],y['PolicyId'],y['Arn'],y['Path'],['DefaultVersionId'],y['AttachmentCount'],y['PermissionsBoundaryUsageCount'],y['IsAttachable'],y['CreateDate'],y['UpdateDate'],y['PolicyVersionList']))
    local_managed_policy_csv_file =  output2csv(LIST_LOCAL_POLICY, parse_local_managed_policy)
    upload_filename = str(os.getenv("EXTRACT_IAM")) + "/"
    upload_filename += str(local_managed_policy_csv_file)[5:]
    call_s3.upload_file(local_managed_policy_csv_file, upload_filename)
  message = prepare_alert_message(LIST_LOCAL_POLICY, len(parse_local_managed_policy))
  call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, local_managed_policy_csv_file)

  #(6)extract list of AWSManagedPolicy
  aws_managed_policy_response = call_iam.get_account_authorization_details("AWSManagedPolicy")
  parse_aws_managed_policy = []
  aws_managed_policy_csv_file = None
  if len(aws_managed_policy_response) > 0 and aws_managed_policy_response != None:
    for x in aws_managed_policy_response:
      for y in x ['Policies']:
        #print(y['PolicyName'],y['PolicyId'],y['Arn'],y['Path'],['DefaultVersionId'],y['AttachmentCount'],y['PermissionsBoundaryUsageCount'],y['IsAttachable'],y['CreateDate'],y['UpdateDate'],y['PolicyVersionList'])
        parse_aws_managed_policy.append(iam_policy_record(y['PolicyName'],y['PolicyId'],y['Arn'],y['Path'],['DefaultVersionId'],y['AttachmentCount'],y['PermissionsBoundaryUsageCount'],y['IsAttachable'],y['CreateDate'],y['UpdateDate'],y['PolicyVersionList']))
    aws_managed_policy_csv_file =  output2csv(LIST_AWS_POLICY, parse_aws_managed_policy)
    upload_filename = str(os.getenv("EXTRACT_IAM")) + "/"
    upload_filename += str(aws_managed_policy_csv_file)[5:]
    call_s3.upload_file(aws_managed_policy_csv_file, upload_filename)
  message = prepare_alert_message(LIST_AWS_POLICY, len(parse_aws_managed_policy))
  call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, aws_managed_policy_csv_file)

  logging.info('Total Errors: {}'.format(error_count))
  if error_count > 255:
    error_count = 255
  logging.info('Exiting lambda')
  if error_count > 0:
    # exit if error_count (lambda doesn't like sys.exit(0))
    sys.exit('Exiting lambda')

#Check whether the execution is local or lambda
if os.getenv("LAMBDA") != "True": 
  main(None,None)
