#!/usr/bin/env python3
from shared.iam import iam

class iam_policy_record:
  def __init__(self, policyname, policyid, arn, path, defaultversionid, attachmentcount, permissionsboundaryusagecount, isattachable, createdate, updatedate, policyversionlist):
  #print(y['PolicyName'],y['PolicyId'],y['Arn'],y['Path'],['DefaultVersionId'],y['AttachmentCount'],y['PermissionsBoundaryUsageCount'],y['IsAttachable'],y['CreateDate'],y['UpdateDate'],y['PolicyVersionList'])
    self.policyname                     = policyname
    self.policyid                       = policyid
    self.arn                            = arn
    self.path                           = path
    self.defaultversionid               = defaultversionid
    self.attachmentcount                = attachmentcount
    self.permissionsboundaryusagecount  = permissionsboundaryusagecount
    self.isattachable                   = isattachable
    self.createdate                     = createdate
    self.updatedate                     = updatedate
    self.policyversionlist              = policyversionlist
    