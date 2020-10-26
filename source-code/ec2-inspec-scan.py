#!/usr/bin/env python3
import boto3, hashlib, os, sys, csv
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
from shared.ssm import ssm
from shared.dynamodb import dynamodb
from shared.inspec_record import inspec_record
from shared.alerts import alerts

#load environment variables from .env. Applicable for both local and lambda runs. 
load_dotenv()

def parse_scan_result(non_compliant_items):
  extracted = []
  for z in non_compliant_items:  
    for y in z:
      for x in y['ComplianceItems']:
        #extract the ec2 instance id and the InSpec title output
        hash_key = str(x['ResourceId']) + str(x['Title'])
        #print(hashlib.md5(hash_key.encode('utf-8')).hexdigest(),x['ResourceId'],x['Title'])
        extracted.append(inspec_record(hashlib.md5(hash_key.encode('utf-8')).hexdigest(),x['ResourceId'],x['Title'])) 
  return extracted

def dynamodb_insert_new_result(new_result):
  call_dynamodb = dynamodb(os.getenv("EC2_INSPEC_SCAN"))
  for x in new_result:
    #write the extracted compliance items to dynamodb
    call_dynamodb.insert_record(x.hash, x.ec2_id, x.title)

def remove_outdated_record(stored_hashes, current_hashes):
  #identfied past records which are not found in the latest scan. This mean that these past records are NA or remediated.
  outdated_hashes = [item for item in stored_hashes if item not in current_hashes]
  print("[-]num of outdated/remediated non-compliant found: ",len(set(outdated_hashes)))
  call_dynamodb = dynamodb(os.getenv("EC2_INSPEC_SCAN"))
  call_dynamodb.delete_record(outdated_hashes)
  return outdated_hashes

def prepare_alert_message(ssm_get_inventory_ec2_ids, new_hashes):
  now=datetime.now(timezone(os.getenv("TIMEZONE")))
  date_stamp=now.strftime('%d-%b-%Y')
  time_stamp=now.strftime('%H:%M:%S')
  title ="*[Schedule/Ad-Hoc] :oncoming_police_car: Triggered EC2 Compliance Scan update.*\n"
  message = title
  message += "- Scan triggered on (date): " + "`" +date_stamp + "`" + "\n"
  message += "- Scan triggered on (time): " + "`" +time_stamp + "`" + "\n" 
  message += "*Num of ec2 found in ssm-inventory*: " + "`" + str(len(ssm_get_inventory_ec2_ids)) + "`" + "\n"
  if len(new_hashes) > 0: 
    message += "*Num of new non-compliant found*: " + "`" +  str(len(set(new_hashes))) + "`" + " :rotating_light: \n"
  else: 
    message += "*NO new non-compliant found* :tada: :thumbsup:"
  return(message)

def output2csv(inputs): 
  output_file = "/tmp/%s" % str(os.getenv("SCAN_ALERT_CSV"))
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
  call_ssm = ssm()
  ssm_get_inventory_ec2_ids = call_ssm.get_inventory()
  print("num of ec2_instances found in ssm inventory: ", len(ssm_get_inventory_ec2_ids))

  #gather list of non-compliant items from each ec2 instance. 
  non_compliant_items = []
  for ec2_id in ssm_get_inventory_ec2_ids:
    #convert from dict to str, so can append a newline for each item.
    non_compliant_items.append(call_ssm.list_compliance_items(ec2_id, "NON_COMPLIANT"))
  #print("set of non_compliant_items: ", len(non_compliant_items))

  #extract the current inspec-scan result and compute the hash value for each compliant items.
  parse_result = parse_scan_result(non_compliant_items)

  call_dynamodb = dynamodb(os.getenv("EC2_INSPEC_SCAN"))
  #capture the past inspec-scan results' hash, which are stored in DynamoDB
  stored_hashes = call_dynamodb.get_record_hash()
  print("num of non-compliant stored in dynamodb: ", len(stored_hashes))

  #capture the current inspec-scan results
  current_hashes = []
  for x in parse_result:
    current_hashes.append(x.hash)
  #As there will be duplicate if a same InSpec title is used for more than 1 control.
  #Thus, we only concern on finding unique current scan result.
  print("num of non-compliant found from current scan: ", len(set(current_hashes)))

  #remove past inspec-scan results which are not found in the current inspec-scan. 
  #This mean that these past records are NA or remediated. 
  remove_outdated_record(stored_hashes, current_hashes)

  #identify new records which are only found in the current inspec-scan results
  new_hashes = [item for item in current_hashes if item not in stored_hashes]
  print("[+]num of new non-compliant found from current scan: ", len(set(new_hashes)))
  new_result = []
  for x in parse_result:
    #extract new result, where the scan result hash is not found in the current stored hashes.
    if stored_hashes.count(x.hash) < 1:
      new_result.append(x)

  #start sending Slack alert notification
  message = prepare_alert_message(ssm_get_inventory_ec2_ids, new_hashes)
  call_alerts = alerts(call_ssm.get_parameter("slack"))
  #check whether there is any new finding 
  if len(new_result) < 1:
    print("NO new non-compliant found!")
    slack_response = call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, None)
  else: 
    #generate a csv file in /tmp (writeable in Lambda) which store the new non-compliant configurations found.
    output_file = output2csv(new_result)
    slack_response = call_alerts.send_alert(os.getenv("SLACK_CHANNEL"), message, output_file)
  #check whether the alert notification has been trigger successfully, before inserting the new result.
  if slack_response == True:
    dynamodb_insert_new_result(new_result)
  
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
