#!/usr/bin/env python3
import os, sys, csv
#Lambda layers are extracted to the /opt directory in the function execution environment
#https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html?icmpid=docs_lambda_help 
#switch to /opt/packages for the 3rd parties dependencies.
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/packages')
import logging, pytz
from datetime import datetime
from dotenv import load_dotenv
from pytz import timezone
#switch back to /opt for the "shared" folder which consists our class files.
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/')
from dotenv import load_dotenv
from shared.inspec_record import inspec_record
from shared.dynamodb import dynamodb
from shared.alerts import alerts
from shared.ssm import ssm
from shared.s3 import s3

#load environment variables from .env. Applicable for both local and lambda runs. 
load_dotenv()

def remove_duplicate(listofitems):
  newlist = list(set(listofitems))
  return newlist

def prepare_alert_message(unique_ec2_instances, parse_all_records):
  now=datetime.now(timezone(os.getenv("TIMEZONE")))
  date_stamp=now.strftime('%d-%b-%Y')
  time_stamp=now.strftime('%H:%M:%S')
  title ="*[MONTHLY-UPDATE] :oncoming_police_car: Current EC2 Non-Compliant update.*\n"
  message = title
  message += "- Read database on (date): " + "`" +date_stamp + "`" + "\n"
  message += "- Read database on (time): " + "`" +time_stamp + "`" + "\n"
  message += "*Num of affected ec2*: " + "`" + str(len(unique_ec2_instances)) + "`" + "\n"
  if len(parse_all_records) > 0: 
    message += "*Num of non-compliant found*: " + "`" +  str(len(parse_all_records)) + "`" + " :rotating_light: \n"
  else: 
    message += "*NO non-compliant found* :tada: :thumbsup:"
  return(message)

def output2csv(inputs): 
  output_file = "/tmp/%s" % str(os.getenv("MONTHLY_ALERT_CSV"))
  export = open(output_file, mode='w')
  writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  #header row
  writer.writerow(["No.", "md5hash", "ec2 instance-id", "title"])
  count = 1
  for x in inputs:
    #print(count,x['md5hash'],x['instance'],x['title'])
    writer.writerow([count,x.hash,x.ec2_id,x.title])
    count = count + 1
  export.close()
  return output_file

def main(event, lambda_context):
  logging.info('Starting Lambda')
  error_count = 0

  print("event: ", event)
  print("lambda_context: ", lambda_context)

  call_dynamodb = dynamodb(os.getenv("EC2_INSPEC_SCAN"))
  all_records = call_dynamodb.get_all_record()
  print("num of non-compliant: ", str(len(all_records)))
  ec2_instances = []
  parse_all_records = []
  for x in all_records:
    ec2_instances.append(x['instance'])
    parse_all_records.append(inspec_record(x['md5hash'],x['instance'],x['title']))
  
  #remove duplicate ec2 instance id.
  unique_ec2_instances = remove_duplicate(ec2_instances)
  print("num of affected ec2_instances: ", str(len(unique_ec2_instances)))
  #prepare message for Slack alert
  prepared_message = prepare_alert_message(unique_ec2_instances, parse_all_records)
  call_alerts = alerts(ssm().get_parameter("slack"))
  if len(parse_all_records) > 0:
    #generate a csv file in /tmp (writeable in Lambda) which store all the non-compliant configuration found.
    output_file = output2csv(parse_all_records)
    #upload csv file to S3 & prepare the uploaded filename
    call_s3 = s3(os.getenv("BUCKET_NAME"))
    now=datetime.now(timezone(os.getenv("TIMEZONE")))
    now.strftime('%H:%M:%S')
    upload_filename = str(os.getenv("EC2_INSPEC_SCAN"))
    upload_filename += str(now.strftime('/%d%b%Y-'))
    upload_filename += str(now.strftime('%H%M%S-'))
    upload_filename += str(output_file)[5:]
    call_s3.upload_file(output_file, upload_filename)
    #sending the slack notificiation 
    call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), prepared_message, output_file)
  else: 
    #sending the slack notificiation 
    call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), prepared_message, None)

  logging.info('Total Errors: {}'.format(error_count))
  if error_count > 255:
    error_count = 255
  logging.info('Exiting lambda')
  # exit if error_count (lambda doesn't like sys.exit(0))
  if error_count > 0:
    sys.exit('Exiting lambda')

#Check whether the execution is local or lambda
if os.getenv("LAMBDA") != "True": 
  main(None,None)
