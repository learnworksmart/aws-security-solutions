#!/usr/bin/env python3
import boto3, os, sys, csv, re
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/packages')
import logging
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
#switch back to /opt for the "shared" folder which consists our class files.
if os.getenv("LAMBDA") == "True": sys.path.append('/opt/')
from shared.ssm import ssm
from shared.config import config
from shared.events import events
from shared.monitor_record import monitor_record
from shared.alerts import alerts

#load environment variables from .env. Applicable for both local and lambda runs. 
load_dotenv()

#global variables
EVENT_TYPE="AWS::Events::Rule"
SSM_TYPE="AWS::SSM::Association"
CONFIG_TYPE="AWS::Config::ConfigRule"
MESSAGE_NOTFOUND="NOT_FOUND"

def prepare_alert_message(notfound, overall_result):
  now=datetime.now(timezone(os.getenv("TIMEZONE")))
  date_stamp=now.strftime('%d-%b-%Y')
  time_stamp=now.strftime('%H:%M:%S')
  title ="*[MONITOR] :oncoming_police_car: AWS Security Resources update.*\n"
  message = title
  message += "- Ran on (date): " + "`" +date_stamp + "`" + "\n"
  message += "- Ran on (time): " + "`" +time_stamp + "`" + "\n"
  if notfound > 0: 
    message += "*Num of missing security resources*: " + "`" + str(notfound) + "`" + " :rotating_light: \n"
  else: 
    message += "*NO missing security resources* :tada: :thumbsup:"
  return(message)

def output2csv(inputs): 
  output_file = "/tmp/%s" % str(os.getenv("MONITOR_ALERT_CSV"))
  export = open(output_file, mode='w')
  writer = csv.writer(export, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  #header row
  writer.writerow(["No.", "resource name", "resource type", "status"])
  count = 1
  for x in inputs:
    #print(x.resourcename, x.resourcetype, x.status)
    writer.writerow([count,x.resourcename, x.resourcetype, x.status])
    count = count + 1
  export.close()
  return output_file

def check_ssm_association(all_ssm_association, required_ssm_association, overall_result):
  #extract all identified events and their state.
  parse_all_association = {}
  for x in all_ssm_association:
    for y in x['Associations']:
      parse_all_association[y['AssociationName']] = y['Overview']['AssociationStatusAggregatedCount']
  # check whether the required ssm association exists? 
  for x in required_ssm_association:
    if x in parse_all_association: 
      overall_result.append(monitor_record(x, SSM_TYPE, parse_all_association[x]))
    else:
      overall_result.append(monitor_record(x,  SSM_TYPE, MESSAGE_NOTFOUND))
  return overall_result

def check_aws_config_rule(all_aws_config_response, required_aws_config_rules, overall_result):
  prase_all_aws_config_response = {}
  for x in all_aws_config_response:
    if x != None: #meaning the requested aws config rule exists
      for y in (x['ConfigRules']):
        prase_all_aws_config_response[y['ConfigRuleName']] = y['ConfigRuleState']
  #compare the required rule with the extracted current state
  for x in required_aws_config_rules:
    if x in prase_all_aws_config_response: #if the required rule exists
      overall_result.append(monitor_record(x, CONFIG_TYPE, prase_all_aws_config_response[x]))
    else:
      overall_result.append(monitor_record(x, CONFIG_TYPE, MESSAGE_NOTFOUND)) 
  return overall_result

def check_cloudwatch_event(all_events, required_events, overall_result):
  #extract all identified events and their state.
  parse_all_events = {}
  for x in all_events:
    for y in x['Rules']:
      parse_all_events[y['Name']] = y['State']
  #compare the required event with the extracted current state
  for x in required_events:
    if x in parse_all_events: #if the required events exists
      overall_result.append(monitor_record(x, EVENT_TYPE, parse_all_events[x]))
    else:
      overall_result.append(monitor_record(x, EVENT_TYPE, MESSAGE_NOTFOUND)) 
  return overall_result
    
def main(event, lambda_context):
  logging.info('Starting Lambda')
  error_count = 0
  print("event: ", event)
  print("lambda_context: ", lambda_context)

  overall_result = []
  # non_compliant_count = 0

  #(1) check for required SSM associations 
  #get all ssm associations from AWS
  all_ssm_association = ssm().list_associations()
  #retrieve list of required SSM association from .env
  required_ssm_association = (os.getenv("MONITOR_SSM")).split(',')
  check_ssm_association(all_ssm_association, required_ssm_association, overall_result) 

  #(2) check for required AWS Config rules 
  required_aws_config_rules = (os.getenv("MONITOR_AWS_CONFIG")).split(',')
  #retrieve each aws config rule details. 
  all_aws_config_response = []
  call_config = config()
  for x in required_aws_config_rules:
    all_aws_config_response.append(call_config.describe_config_rules(x))
  check_aws_config_rule(all_aws_config_response, required_aws_config_rules, overall_result)

  #(3) check for required cloudwatch events
  required_events = (os.getenv("MONITOR_EVENT")).split(',')
  call_events = events()
  all_events = call_events.list_rules()
  check_cloudwatch_event(all_events, required_events, overall_result)

  notfound = 0
  for x in overall_result:
    if MESSAGE_NOTFOUND in x.status:
      notfound += 1

  #sending alert alert & output result to csv.
  prepared_message = prepare_alert_message(notfound, overall_result)
  call_alerts = alerts(ssm().get_parameter("slack"))
  output_file = output2csv(overall_result)
  if notfound > 0:
    call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), prepared_message, output_file)
  else:
    call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), prepared_message, output_file)

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
