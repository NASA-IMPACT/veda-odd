import boto3
import numpy as np
import s3fs

def get_credentials() -> dict:
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=f'arn:aws:iam::{account_id}:role/ec2-s3-access-role',
        RoleSessionName='jhub-session'
    )
    return response['Credentials']

def create_s3filesystem(credentials: dict) -> s3fs.S3FileSystem:
    return s3fs.S3FileSystem(
        anon=False,
        key=credentials['AccessKeyId'],
        secret=credentials['SecretAccessKey'],
        token=credentials['SessionToken']
    )

def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy(i) for i in obj)
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj