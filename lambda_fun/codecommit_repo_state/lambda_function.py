import json
import requests

def lambda_handler(event, context):
    
    myToken="xoxb-5079214484789-5105854779392-EMko3kofF9SCcd4rZqMLm0PM"
    url="https://slack.com/api/chat.postMessage"
    
    myMessage= {
        'channel' : 'devops',
        'text' : event['detail']['repositoryName'] + ' has been updated. Commit ID:' + event['detail']['commitId'] 
    }
    
    headers = {'Content-type': 'application/json','Authorization' : 'Bearer ' + myToken}

    rsp = requests.post(url, json=myMessage, headers=headers)
    print (rsp.text)