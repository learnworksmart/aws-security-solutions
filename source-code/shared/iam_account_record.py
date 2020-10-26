#!/usr/bin/env python3
from shared.iam import iam

class iam_account_record:
  #object for aws_config non-compliant item.
  def __init__(self, path, username, userid, arn, createdate, grouplist, attachedmanagepolicies, tags):
    self.path                   = path 
    self.username               = username 
    self.userid                 = userid
    self.arn                    = arn
    self.createdate             = createdate
    self.grouplist              = grouplist
    self.attachedmanagepolicies = attachedmanagepolicies
    self.tags                    = tags
    
    # call_iam = iam()
    # #Lists the names of the inline policies embedded in the specified IAM user. 
    # response = call_iam.list_user_policies(username)
    # self.inline_policy  = response['PolicyNames']
    # #Lists all managed policies that are attached to the specified IAM user.
    # response = call_iam.list_attached_user_policies(username)
    # self.managed_policy = response['AttachedPolicies']
    