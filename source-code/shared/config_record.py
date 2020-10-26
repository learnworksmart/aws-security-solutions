#!/usr/bin/env python3
class config_record:
  #object for aws_config non-compliant item.
  def __init__(self, rule, resourcetype, resourceid):
    self.rule         = rule 
    self.resourcetype = resourcetype
    self.resourceid   = resourceid
