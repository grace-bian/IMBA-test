import json
import boto3

def lambda_handler(event, context):
    glue=boto3.client('glue')
    response = glue.start_job_run(JobName ="imba-4-features")
    print("Lambda Invoke ")
    