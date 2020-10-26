#!/usr/bin/env python3
class monitor_record:
  #object for aws_config non-compliant item.
  def __init__(self, resourcename, resourcetype, status):
    self.resourcename = resourcename 
    self.resourcetype = resourcetype
    self.status       = status
