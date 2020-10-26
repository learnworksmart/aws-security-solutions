#!/usr/bin/env python3
import boto3

class events: 
  client = boto3.client('events')

  def list_rules(self):
    all_events = []
    token = "start" 
    #If NextToken is None, mean no more outstanding result.
    try: 
      while token != None:    
        if token == "start":
          response = self.client.list_rules(
            Limit=1
          )
          all_events.append(response)
          if 'NextToken' not in response.keys():
            token = None
          else:
            token = response['NextToken']
        else:
          response = self.client.list_rules(
            Limit=1,
            NextToken=token
          )
          all_events.append(response)
          if 'NextToken' not in response.keys():
            token = None
          else:
            token = response['NextToken']
    except Exception as e: 
      print("ERROR encountered from list_rules")
      print(e)   
    return all_events

