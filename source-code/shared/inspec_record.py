#!/usr/bin/env python3
class inspec_record:
  #object for ec2-inspec-scan non-compliant item.
  def __init__(self, hash, ec2_id, title):
    self.hash   = hash 
    self.ec2_id = ec2_id
    self.title  = title
