#!/usr/bin/env python3
import os
from slack import WebClient
from slack.errors import SlackApiError

class alerts: 

  def __init__(self, token):
    self.token = token

  def send_alert(self, slack_channel, message, attachment):
    client = WebClient(token=self.token)

    try:
      client.chat_postMessage(
        channel=slack_channel,
        text=message
      )

      if attachment != None: 
        client.files_upload(
          channels=slack_channel,
          file=attachment,
          #remove the first 5 character of the filename, `/tmp/`
          title=str(attachment)[5:], 
          filetype="csv"
        )
      print("Successfully post Slack message to %s channel!" %slack_channel)
      return True
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
      print("ERROR as we are unable to send Slack alert")
      print(e.response)
      return False
