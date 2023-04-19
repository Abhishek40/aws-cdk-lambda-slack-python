import json
import boto3
import requests

def process_message(userFrom, msg, channel):
  
  print("Got message " + msg)
  print("From User:" + userFrom)
  
  if "run pipeline" in msg:
    print('posting event to run pipeline...')
    post_to_eventbridge()
  

def post_to_eventbridge():
  #Create EventBridge Client
  client = boto3.client('events')

  #put the event in queue
  response = client.put_events(
      Entries=[
          {
              'Source': 'slack.devops',
              'Resources': [],
              'DetailType': 'Execute our pipeline',
              'Detail': '{}',
              'EventBusName': 'default'
          },
      ]
  )


def lambda_handler(event, context):
  
  request_type = event['type']

  #params = event.get("body")
  #slack_event = json.loads(params)
  
  #print("Got request type: " + slack_event['type'])
  #print('Full request:')
  #print( event)
  
  #request_type = params['type']
  
  #if request_type == 'url_verification':
  #  return {'challenge' : params['challenge'] }
  
  #slack_body = event.get("body")
  #slack_event = json.loads(slack_body)
  #request_type = slack_event['type']
  #challenge_answer = slack_event.get("challenge")
  
  #return {
  #    'statusCode' : 200,
  #    'body' : challenge_answer
  #}
  if request_type == 'event_callback':
    print ("processing message...")
    process_message(event['event']['user'], event['event']['text'], event['event']['channel'])

