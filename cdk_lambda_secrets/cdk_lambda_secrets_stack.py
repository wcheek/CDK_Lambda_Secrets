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
