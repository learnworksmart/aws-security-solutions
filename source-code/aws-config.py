#!/usr/bin/env python3
import boto3, os, sys,csv
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/packages')
import logging
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
#switch back to /opt for the "shared" folder which consists our class files.
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/')
from shared.config import config
from shared.config_record import config_record
from shared.ssm import ssm
from shared.alerts import alerts
from shared.s3 import s3

#load environment variables from .env. Applicable for both local and lambda runs. 
load_dotenv()

def parse_scan_result(non_compliant_items):
  parse_non_compliant = []
  for x in non_compliant_items:
    #print(x['ConfigRuleName'], x['ResourceType'], x['ResourceId'])
    parse_non_compliant.append(config_record(x['ConfigRuleName'], x['ResourceType'], x['ResourceId']))
  return parse_non_compliant

def output2csv(inputs): 
  output_file = "/tmp/%s" % str(os.getenv("AWS_CONFIG_ALERT_CSV"))
  export = open(output_file, mode='w')
  writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  #header row
  writer.writerow(["No.", "ConfigRuleName", "ResourceType", "ResourceId"])
  count = 1
  for x in inputs:
    #print(x.rule, x.resourcetype, x.resourceid)
    writer.writerow([count,x.rule,x.resourcetype,x.resourceid])
    count = count + 1
  export.close()
  return output_file

def prepare_alert_message(non_compliant_items):
  now=datetime.now(timezone(os.getenv("TIMEZONE")))
  date_stamp=now.strftime('%d-%b-%Y')
  time_stamp=now.strftime('%H:%M:%S')
  title ="*[AWS Config] :oncoming_police_car: AWS Config update.*\n"
  message = title
  message += "- Scan triggered on (date): " + "`" +date_stamp + "`" + "\n"
  message += "- Scan triggered on (time): " + "`" +time_stamp + "`" + "\n" 
  if len(non_compliant_items) > 0: 
    message += "*Num of non-compliant found*: " + "`" +  str(len(non_compliant_items)) + "`" + " :rotating_light: \n"
  else: 
    message += "*NO new non-compliant found* :tada: :thumbsup:"
  return(message)

def main(event, lambda_context):
  logging.info('Starting Lambda')
  error_count = 0
  print("event: ", event)
  print("lambda_context: ", lambda_context)

  #capture the list of targeted AWS Config rules
  aws_config_rules = (os.getenv("AWS_CONFIG_RULES")).split(',')
  call_config = config()
  # #start evalutation on the selected aws config rules
  # #useful for on-demand request, mainly for testing purpose.
  # call_config.start_config_rules_evaluation(aws_config_rules)

  #Get the non-compliant resources found in AWS Config
  non_compliant = []
  for x in aws_config_rules:
    result = call_config.get_compliance_details_by_config_rule(x, 'NON_COMPLIANT') #NON_COMPLIANT
    for y in result:
      non_compliant.append(y)
  #parse the non-compliant resources found   
  parse_non_compliant = parse_scan_result(non_compliant)

  #prepare the slack alert message  
  message = prepare_alert_message(parse_non_compliant)
  call_alerts = alerts(ssm().get_parameter("slack"))
  if len(parse_non_compliant) < 1:
    print("NO new non-compliant found!")
    call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, None)
  else: 
    #generate a csv file in /tmp (writeable in Lambda) which store the new non-compliant configurations found.
    output_file = output2csv(parse_non_compliant)
    call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, output_file)
    call_s3 = s3(os.getenv("BUCKET_NAME"))
    now=datetime.now(timezone(os.getenv("TIMEZONE")))
    now.strftime('%H:%M:%S')
    upload_filename = str(os.getenv("AWS_CONFIG"))
    upload_filename += str(now.strftime('/%d%b%Y-'))
    upload_filename += str(now.strftime('%H%M%S-'))
    upload_filename += str(output_file)[5:]
    call_s3.upload_file(output_file, upload_filename)

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


