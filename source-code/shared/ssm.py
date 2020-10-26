#!/usr/bin/env python3
import boto3

class ssm: 
  client = boto3.client('ssm')

  #aws ssm get-inventory
  def get_inventory(self):
    ec2_ids = []
    #query ssm inventory for non-terminated ec2 instances
    response = self.client.get_inventory(
      Filters=[
        {
            'Key': 'AWS:InstanceInformation.InstanceStatus',
            'Values': [ 'Terminated' ],
            'Type': 'NotEqual'
        }
      ]
    )
    # gather list of ec2 instances'id registered in ssm inventory.
    for i in range(len(response['Entities'])):
      #print(response['Entities'][i]['Id'])
      ec2_ids.append(response['Entities'][i]['Id'])
    return ec2_ids
 
  def list_compliance_items(self, ec2_id, filter):
    compliance_items = []
    token = "start" 
    #If NextToken is None, mean no more outstanding compliance result.
    while token != None:    
      if token == "start":
        response = self.client.list_compliance_items(
          Filters=[
              {
                  'Key': 'ComplianceType',
                  'Values': [ 'Custom:InSpec' ],
                  'Type': 'EQUAL'
              },
              {
                  'Key': 'Status',
                  'Values': [ filter ],
                  'Type': 'EQUAL'
              }
          ],
          ResourceTypes=[ 'ManagedInstance' ],
          ResourceIds=[ ec2_id ],
          MaxResults=50
        )
        compliance_items.append(response)
        if 'NextToken' not in response.keys():
          token = None
        else:
          token = response['NextToken']
      else:
        response = self.client.list_compliance_items(
          Filters=[
              {
                  'Key': 'ComplianceType',
                  'Values': [ 'Custom:InSpec' ],
                  'Type': 'EQUAL'
              },
              {
                  'Key': 'Status',
                  'Values': [ filter ],
                  'Type': 'EQUAL'
              }
          ],
          ResourceTypes=[ 'ManagedInstance' ],
          ResourceIds=[ ec2_id ],
          MaxResults=50,
          NextToken=token
        )
        compliance_items.append(response)
        if 'NextToken' not in response.keys():
          token = None
        else:
          token = response['NextToken']
    return compliance_items

  def get_parameter(self, param_name):
    response = self.client.get_parameters(
      Names=[
        param_name,
      ],
      WithDecryption=True
    )
    return(response['Parameters'][0]['Value'])

  # def list_associations_name(self):
  #   response = self.client.list_associations(
  #       MaxResults=50,
  #   )
  #   associations = []
  #   for x in response['Associations']:
  #     associations.append(x['Name'])
  #   return associations

  def list_associations(self):
    associations = []
    token = "start" 
    try:
      #If NextToken is None, mean no more outstanding compliance result.
      while token != None:    
        if token == "start":
          response = self.client.list_associations(
            MaxResults=50
          )
          associations.append(response)
          if 'NextToken' not in response.keys():
            token = None
          else:
            token = response['NextToken']
        else: 
          response = self.client.list_associations(
            MaxResults=50,
            NextToken=token
          )
          associations.append(response)
          if 'NextToken' not in response.keys():
            token = None
          else:
            token = response['NextToken']
    except Exception as e:
      print("[-]ERROR encountered when trying to retrieve list of active SSM-Assoication!")
      print(e)
    return associations



