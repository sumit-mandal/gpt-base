#!/usr/bin/env python3
import os

import aws_cdk as cdk

from config import APP_NAME, AWS_TAG_CREATED_BY, AWS_TAG_PROJECT_NAME, STAGE
from infra.infra_stack import InfraStack

stack_name = f"{APP_NAME}-codepipeline-stack"
print(stack_name)

app = cdk.App()
InfraStack(
    app,
    stack_name,
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */
    env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="ap-south-1"),
    stack_name=stack_name,
    tags={
        "project": AWS_TAG_PROJECT_NAME,
        "createdBy": AWS_TAG_CREATED_BY,
        "environment": STAGE,
    }
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

app.synth()
