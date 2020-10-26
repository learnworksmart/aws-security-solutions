#!/usr/bin/env python3
import boto3

class s3: 
  client = boto3.resource('s3')

  def __init__(self, bucket):
    self.bucket = bucket

  def upload_file(self, source_filename, dest_filename):
    try:
      self.client.Bucket(self.bucket).upload_file(Filename=source_filename,Key=dest_filename)
      print("Successfully upload %s to s3://%s/%s" % (source_filename, str(self.bucket), dest_filename))
      return True
    except Exception as e:
      print("ERROR encountered when uploading %s to s3" % source_filename)
      print(e)
      return False
