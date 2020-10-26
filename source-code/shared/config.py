#!/usr/bin/env python3
import boto3

class config: 
  client = boto3.client('config')

  def start_config_rules_evaluation(self, rule):
    response = self.client.start_config_rules_evaluation(
      ConfigRuleNames=rule,
    )
    return response
  
  def delete_evaluation_results(self, rule):
    response = self.client.delete_evaluation_results(
      ConfigRuleName=rule
    )
    return response

  def get_compliance_details_by_config_rule(self, rule, filter):
    non_compliant = []
    token = "start" 
    #If NextToken is None, mean no more outstanding result.
    try: 
      while token != None:    
        if token == "start":
          response = self.client.get_compliance_details_by_config_rule(
              ConfigRuleName=rule,
              ComplianceTypes=[filter],
              Limit=100
          )
          for z in response['EvaluationResults']:
            y = z['EvaluationResultIdentifier']['EvaluationResultQualifier']
            non_compliant.append(y)
            #print(y['ConfigRuleName'],y['ResourceType'],y['ResourceId'])
          if 'NextToken' not in response.keys():
            token = None
          else:
            token = response['NextToken']
        else:
          response = self.client.get_compliance_details_by_config_rule(
              ConfigRuleName=rule,
              ComplianceTypes=[filter],
              Limit=100,
              NextToken=token
          )
          for z in response['EvaluationResults']:
            y = z['EvaluationResultIdentifier']['EvaluationResultQualifier']
            non_compliant.append(y)
          if 'NextToken' not in response.keys():
            token = None
          else:
            token = response['NextToken']
    except Exception as e:
      print("ERROR when trying to get compliance detail from AWS Config rules.")
      print(e)
    return non_compliant  

  def put_evaluations(self, token, resourcetype, resourceid, compliancetype, timestamp):
    response = self.client.put_evaluations(
      Evaluations=[
          {
              'ComplianceResourceType': resourcetype,
              'ComplianceResourceId': resourceid,
              'ComplianceType': compliancetype,
              #'ComplianceType': 'COMPLIANT'|'NON_COMPLIANT'|'NOT_APPLICABLE'|'INSUFFICIENT_DATA',
              #'Annotation': 'string',
              #'OrderingTimestamp': datetime(2015, 1, 1)
              'OrderingTimestamp': timestamp
          },
      ],
      ResultToken=str(token),
      TestMode=False
    )
    return response

  def describe_config_rules(self, rule):
    try: 
      response = self.client.describe_config_rules(
        ConfigRuleNames=[
            rule,
        ]
      )
      return response
    except Exception as e:
      print("[-]ERROR when checking for aws config rule: %s" % rule)
      print(e)
      return None

  # def describe_config_rules(self, rule):
  #   all_response = []
  #   token = "start" 
  #   #If NextToken is None, mean no more outstanding result.
  #   try: 
  #     while token != None:    
  #       if token == "start":
  #         response = self.client.describe_config_rules(
  #             ConfigRuleNames=[
  #                 rule,
  #             ]
  #         )
  #         all_response.append(response)
  #         if 'NextToken' not in response.keys():
  #           token = None
  #         else:
  #           token = response['NextToken']
  #       else:
  #         response = self.client.describe_config_rules(
  #           ConfigRuleNames=[
  #               rule,
  #           ],
  #           NextToken=token
  #         )
  #         all_response.append(response)
  #         if 'NextToken' not in response.keys():
  #           token = None
  #         else:
  #           token = response['NextToken']
  #   except Exception as e:
  #     print("[-]ERROR encountered when checking for aws config rule: %s" % rule)
  #     print(e)
  #   return all_response
 
