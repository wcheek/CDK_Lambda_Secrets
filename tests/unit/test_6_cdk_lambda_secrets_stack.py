import aws_cdk as core
import aws_cdk.assertions as assertions

from 6_cdk_lambda_secrets.6_cdk_lambda_secrets_stack import 6CdkLambdaSecretsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in 6_cdk_lambda_secrets/6_cdk_lambda_secrets_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = 6CdkLambdaSecretsStack(app, "6-cdk-lambda-secrets")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
