# Please note this script was written on Python 2.7
# Which will run from the AWS Python run time environment


# Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python,
# which allows Python developers to write software that makes use of
# services like Amazon S3 , Amazon EC2 , Amazon dynamodb etc
import boto3

import os

# This module provides immutable UUID objects (the UUID class) and
# the functions uuid1(), uuid3(), uuid4(), uuid5() for generating version 1, 3, 4, and 5 UUIDs
# unique identifier
import uuid

def lambda_handler(event, context):

    # uuid4() creates a random UUID.
    recordId = str(uuid.uuid4())
    voice = event["voice"]
    text = event["text"]

    print('Generating new DynamoDB record, with ID: ' + recordId)
    print('Input Text: ' + text)
    print('Selected voice: ' + voice)
    
    #Creating new record in DynamoDB table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            'id' : recordId,
            'text' : text,
            'voice' : voice,
            'status' : 'PROCESSING'
        }
    )
    
    #Sending notification about new post to SNS
    client = boto3.client('sns')
    client.publish(
        TopicArn = os.environ['SNS_TOPIC'],
        Message = recordId
    )
    
    return recordId
