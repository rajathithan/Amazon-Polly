# Please note this script was written on Python 2.7
# Which will run from the AWS Python run time environment


# Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python,
# which allows Python developers to write software that makes use of
# services like Amazon S3 , Amazon EC2 , Amazon dynamodb
import boto3

import os

# to deal with key and attributes of item
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    postId = event["postId"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    
    if postId=="*":
        items = table.scan()
    else:
        items = table.query(
            KeyConditionExpression=Key('id').eq(postId)
        )
    
    return items["Items"]