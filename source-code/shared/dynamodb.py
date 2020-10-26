#!/usr/bin/env python3
import boto3, os

class dynamodb: 
  client = boto3.resource('dynamodb')

  def __init__(self, table):
    self.table = table

  def insert_record(self, hash, ec2_id, title):
    self.client.Table(self.table).put_item(
    Item={
          'md5hash': hash,
          'instance': ec2_id,
          'title': title
          }
    )

  def get_record_hash(self):
    primary_keys = []
    for record in (self.client.Table(self.table).scan())['Items']:
      primary_keys.append(record['md5hash'])
    return primary_keys

  def delete_record(self, outdated_hash):
    for x in outdated_hash:
      self.client.Table(self.table).delete_item(
        Key={
          'md5hash': x
        }
      )
  
  def get_all_record(self):
    response = self.client.Table(self.table).scan()['Items']
    return response
