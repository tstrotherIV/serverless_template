import boto3
import json
from botocore.exceptions import ClientError


class Secrets:
    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(service_name='secretsmanager')

    def get(self, secret_name):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        return json.loads(get_secret_value_response['SecretString'])
