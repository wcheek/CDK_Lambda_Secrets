from aws_cdk import Duration, Stack
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class CdkLambdaSecretsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.build_lambda_func()

    def build_lambda_func(self):
        self.processing_lambda = _lambda.Function(
            scope=self,
            id="LambdaWithSecrets",
            runtime=_lambda.Runtime.PYTHON_3_9,
            function_name="LambdaWithSecretsExample",
            code=_lambda.Code.from_asset(path="lambda_with_secrets"),
            handler="lambda_with_secrets.handler",
        )
