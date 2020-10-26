#!/usr/bin/env python3
from shared.iam import iam

class iam_group_record:
  ##print(y['Path'],y['GroupName'],y['GroupId'],y['Arn'],y['CreateDate'],y['GroupPolicyList'],y['AttachedManagedPolicies'])
  def __init__(self, path, groupname, groupid, arn, createdate, grouppolicylist, attachedmanagedpolicies): 
    self.path                     = path 
    self.groupname                = groupname
    self.groupid                  = groupid
    self.arn                      = arn
    self.createdate               = createdate
    self.grouppolicylist          = grouppolicylist
    self.attachedmanagedpolicies  = attachedmanagedpolicies
    