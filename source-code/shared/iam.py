#!/usr/bin/env python3
import boto3

class iam: 
  client = boto3.client('iam')

  #Retrieves the password policy for the AWS account.
  def get_account_password_policy(self):
    try: 
      response = self.client.get_account_password_policy()
      return response
    except Exception as e:
      print("[-]ERROR encountered when trying to get account password policy!")
      print(e)
      return None

  #Retrieves information about all IAM users, groups, roles, and policies in your AWS account, including their relationships to one another.
  def get_account_authorization_details(self, type):
    maxitem = 100
    consolidated_response = []
    #If Marker is None, mean no more outstanding result.
    marker = "start"
    try:
      while marker != None:    
        if marker == "start": 
          response = self.client.get_account_authorization_details(
              Filter=[
                  type, #'User'|'Role'|'Group'|'LocalManagedPolicy'|'AWSManagedPolicy'
              ],
              MaxItems = maxitem
          )
          consolidated_response.append(response)
          if 'Marker' not in response.keys():
            marker = None
          else:
            marker = response['Marker']
        else:
          response = self.client.get_account_authorization_details(
              Filter=[
                  type, #'User'|'Role'|'Group'|'LocalManagedPolicy'|'AWSManagedPolicy'
              ],
              MaxItems = maxitem,
              Marker = marker
          )
          consolidated_response.append(response)
          if 'Marker' not in response.keys():
            marker = None
          else:
            marker = response['Marker']
      return consolidated_response
    except Exception as e:
      print("[-]ERROR encountered when trying to get account authorization details, with type %s" % type)
      print(e)
      return None


  # #Lists the IAM users
  # def list_users(self):
  #   #to indicate the maximum number of items you want in each response
  #   maxitem = 100
  #   consolidated_response = []
  #   #If Marker is None, mean no more outstanding result.
  #   marker = "start"
  #   try:
  #     while marker != None:    
  #       if marker == "start":
  #         response = self.client.list_users(
  #           MaxItems=maxitem
  #         )
  #         consolidated_response.append(response)
  #         if 'Marker' not in response.keys():
  #           marker = None
  #         else:
  #           marker = response['Marker']
  #       else:
  #         response = self.client.list_users(
  #           MaxItems=maxitem,
  #           Marker=marker
  #         )
  #         consolidated_response.append(response)
  #         if 'Marker' not in response.keys():
  #           marker = None
  #         else:
  #           marker = response['Marker']
  #     return consolidated_response
  #   except Exception as e:
  #     print("[-]ERROR encountered when trying to get list of user accounts!")
  #     print(e)
  #     return None

  # #Lists the names of the inline policies embedded in the specified IAM user.
  # def list_user_policies(self, user):
  #   maxitem = 100
  #   response = self.client.list_user_policies(
  #     UserName=user,
  #     MaxItems=maxitem
  #   )
  #   return response
  
  # #Lists all managed policies that are attached to the specified IAM user.
  # def list_attached_user_policies(self, user):
  #   maxitem = 100
  #   response = self.client.list_attached_user_policies(
  #     UserName=user,
  #     MaxItems=maxitem
  #   )
  #   return response

  # #Lists the IAM roles
  # def list_roles(self):
  #   #to indicate the maximum number of items you want in each response
  #   maxitem = 100
  #   consolidated_response = []
  #   #If Marker is None, mean no more outstanding result.
  #   marker = "start"
  #   try:
  #    while marker != None:    
  #       if marker == "start":
  #         response = self.client.list_roles(
  #           MaxItems=maxitem
  #         )
  #         consolidated_response.append(response)
  #         if 'Marker' not in response.keys():
  #           marker = None
  #         else:
  #           marker = response['Marker']
  #       else:
  #         response = self.client.list_roles(
  #           MaxItems=maxitem,
  #           Marker=marker
  #         )
  #         consolidated_response.append(response)
  #         if 'Marker' not in response.keys():
  #           marker = None
  #         else:
  #           marker = response['Marker']
  #       return consolidated_response
  #   except Exception as e:
  #     print("[-]ERROR encountered when trying to get list of roles!")
  #     print(e)
  #     return None

  # #Lists the names of the inline policies that are embedded in the specified IAM role.
  # def list_role_policies(self, role):
  #   maxitem = 100
  #   response = self.client.list_role_policies(
  #       RoleName=role,
  #       MaxItems=maxitem
  #   )
  #   return response

  # #Lists the names of the inline policies that are embedded in the specified IAM role.
  # def list_attached_role_policies(self, role):
  #   maxitem = 100
  #   response = self.client.list_attached_role_policies(
  #       RoleName=role,
  #       MaxItems=maxitem
  #   )
  #   return response
      
  # def list_policies(self, scope, isattached):
  #   #to indicate the maximum number of items you want in each response
  #   maxitem = 100
  #   consolidated_response = []
  #   #If Marker is None, mean no more outstanding result.
  #   marker = "start"
  #   try:
  #     while marker != None:    
  #       if marker == "start":
  #         response = self.client.list_policies(
  #           Scope=scope,
  #           OnlyAttached=isattached,
  #           MaxItems=maxitem
  #         )
  #         consolidated_response.append(response)
  #         if 'Marker' not in response.keys():
  #           marker = None
  #         else:
  #           marker = response['Marker']
  #       else:
  #         response = self.client.list_policies(
  #           Scope=scope,
  #           OnlyAttached=isattached,
  #           MaxItems=maxitem,
  #           Marker=marker
  #         )
  #         consolidated_response.append(response)
  #         if 'Marker' not in response.keys():
  #           marker = None
  #         else:
  #           marker = response['Marker']
  #     return consolidated_response
  #   except Exception as e:
  #     print("[-]ERROR encountered when trying to get list of policies!")
  #     print(e)
  #     return None
