# Securely Use Secrets In Your AWS CDK Deployed Lambda Function

Have you ever needed secure access to things like login details in your Lambda functions? You might need to connect to a database or other service, but you don’t want to need to hard-code your credentials. Well, let’s use best security practices by getting our login details using `AWS Secrets Manager`!

I will be using Python flavored `AWS CDK` to deploy a Lambda function which has permissions to access a secret stored in `Secrets Manager`. I will also show you how to retrieve this secret securely inside your lambda function.

Before getting into the CDK components, let’s create an example secret using AWS CLI:

```bash
aws secretsmanager create-secret --name secretsExample --secret-string "TestPass123"
```

## Stack Design

>   cdk_lambda_secrets/cdk_lambda_secrets_stack.py

Here we build the CDK stack by creating a lambda function and giving it permission to read our secret. We can pass the name of the secret into the lambda function as an environment variable to save ourselves some repetition.

```python
import os

from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_secretsmanager as secrets
from constructs import Construct


class CdkLambdaSecretsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.build_lambda_func()

    def build_lambda_func(self):
        secret_name = "secretsExample"
        self.secrets_lambda = _lambda.Function(
            scope=self,
            id="LambdaWithSecrets",
            runtime=_lambda.Runtime.PYTHON_3_9,
            function_name="LambdaWithSecretsExample",
            code=_lambda.Code.from_asset(
                path="lambda_funcs/lambda_with_secrets"
            ),
            handler="lambda_with_secrets.handler",
            # We need these env vars to access the secret inside the lambda
            environment={
                "secret_name": secret_name,
                "secret_region": os.environ["CDK_DEFAULT_REGION"],
            },
        )
        # Grant permission to the Lambda func to access the secret
        example_secret = secrets.Secret.from_secret_name_v2(
            scope=self, id="secretExample", secret_name=secret_name
        )
        example_secret.grant_read(grantee=self.secrets_lambda)

```

## Lambda Function

>   lambda_funcs/lambda_with_secrets/lambda_with_secrets.py

Here we define a lambda function with a helper function `get_secrets()`. This is a very slightly modified version of the ‘Sample code’ function suggested by AWS when you look at the secret in the AWS Console. Rather than use the `ARN` to access the secret, we can simply use the name of the secret. I found that I was unable to get the `full ARN` of the secret using CDK, but luckily `get_secret_value()` accepts the secret name for its `SecretId` parameter.

```python
import base64
import json
import os

import boto3
from botocore.exceptions import ClientError


def get_secret():
    """
    Gets the secret
    """
    # Get env vars we passed in the stack.
    secret_name = os.getenv("secret_name")
    region_name = os.getenv("secret_region")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        # We need only the name of the secret
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        else:
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
            # If you have multiple secret values, you will need to json.loads(secret) here and then access the values using dict keys
            return secret
        else:
            decoded_binary_secret = base64.b64decode(
                get_secret_value_response["SecretBinary"]
            )
            return decoded_binary_secret


def handler(event, context):
    secret = get_secret()
    # Don't do this in production!!!
    return secret

```

`cdk deploy` this stack and you should have a working example.

## Test the Lambda Function

![image-20220513162919655](D:\Projects\Notes\My Articles\6_CDK_Lambda_Secrets\Assets\image-20220513162919655.png)

The Lambda function successfully retrieved the secret value from `AWS Secrets Manager`!

## Tear Down

To delete the secret we created:

```bash
aws secretsmanager delete-secret --secret-id secretsExample
```

Destroy your stack:

```bash
cdk destroy
```



