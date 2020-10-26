#!/usr/bin/env python3
from shared.iam import iam

class iam_role_record:
  def __init__(self, path, rolename, roleid, arn, createdate, assumerolepolicydocument, instanceprofilelist, rolepolicylist, attachedmanagedpolicies, tags, rolelastused):
    #y['Path'], y['RoleName'],y['RoleId'],y['Arn'],y['CreateDate'],y['AssumeRolePolicyDocument'],y['InstanceProfileList'],y['RolePolicyList'],y['AttachedManagedPolicies'],y['Tags'],y['RoleLastUsed'] 
    self.path                     = path 
    self.rolename                 = rolename 
    self.roleid                   = roleid
    self.arn                      = arn
    self.createdate               = createdate
    self.assumerolepolicydocument = assumerolepolicydocument
    self.instanceprofilelist      = instanceprofilelist
    self.rolepolicylist           = rolepolicylist
    self.attachedmanagedpolicies  = attachedmanagedpolicies
    self.tags                     = tags
    self.rolelastused             = rolelastused
    