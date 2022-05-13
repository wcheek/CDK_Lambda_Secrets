# Securely Use Secrets In Your AWS CDK Deployed Lambda Function

Have you ever needed secure access to things like login details in your Lambda functions? You might need to connect to a database or other service, but you don’t want to need to hard-code your credentials. Well, let’s use best security practices by getting our login details using `AWS Secrets Manager`!

I will be using Python flavored `AWS CDK` to deploy a Lambda function which has permissions to access a secret stored in `Secrets Manager`. I will also show you how to retrieve this secret securely inside your lambda function.

Before getting into the CDK components, let’s create an example secret using AWS CLI:

```bash
aws secretsmanager create-secret --name secretsExample --secret-string "TestPass123"
```

