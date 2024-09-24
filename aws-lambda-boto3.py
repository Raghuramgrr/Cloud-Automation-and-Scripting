import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')

    # Provision an EC2 instance
    instances = ec2.create_instances(
        ImageId='ami-0123456789abcdef0',  # Replace with your AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='my-key-pair',  # Replace with your key pair
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Launched EC2 instance: {instances[0].id}')
    }
