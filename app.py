#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_lambda_secrets.cdk_lambda_secrets_stack import CdkLambdaSecretsStack


app = cdk.App()
CdkLambdaSecretsStack(app, "CdkLambdaSecretsStack",
    )

app.synth()
