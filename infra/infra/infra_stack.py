from aws_cdk import Stack
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import (
    aws_codepipeline as codepipeline,
)  # Duration,; aws_sqs as sqs,
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk import aws_iam
from aws_cdk import aws_sns as sns
from constructs import Construct

from config import APP_NAME, AWS_CODESTAR_ARN, GITHUB_OWNER, GITHUB_REPO, STAGE
from infra.helpers.secret_manager import create_secrets


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        secret = create_secrets(self)

        pipleine_name = f"{APP_NAME}-codepipeline"
        pipeline = codepipeline.Pipeline(
            self, pipleine_name, pipeline_name=pipleine_name
        )

        # add a stage
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="GitHubSource",
            owner=GITHUB_OWNER,
            repo=GITHUB_REPO,
            branch=STAGE,
            output=source_output,
            connection_arn=AWS_CODESTAR_ARN,
        )

        source_stage = pipeline.add_stage(stage_name="Source")
        source_stage.add_action(source_action)

        project_name = f"{APP_NAME}-codebuild-project"
        build_project = codebuild.PipelineProject(
            self,
            project_name,
            build_spec=codebuild.BuildSpec.from_source_filename(
                f"buildspec.{STAGE}.yml"
            ),
            project_name=project_name,
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                compute_type=codebuild.ComputeType.SMALL,
                privileged=True,
            ),
            # environment_variables={
            # 	"DEPLOYMENT_BUCKET": 'tagic-serverless-deployment-bucket'
            # }
        )

        build_project.add_to_role_policy(
            statement=aws_iam.PolicyStatement(
                # resources=[f'arn:aws:s3:::}', f'arn:aws:s3:::}/*'],
                resources=[secret.secret_arn],
                actions=["secretsmanager:*"],
            )
        )

        build_project.add_to_role_policy(
            statement=aws_iam.PolicyStatement(
                resources=["*"],
                actions=["s3:*"],
            )
        )

        build_project.add_to_role_policy(
            statement=aws_iam.PolicyStatement(
                resources=["*"],
                actions=[
                    "iam:*",
                    "cloudFormation:ListStacks",
                    "cloudformation:ListStackResources",
                    "cloudformation:CreateStack",
                    "cloudformation:DeleteStack",
                    "cloudformation:DescribeStacks",
                    "cloudformation:DescribeStackEvents",
                    "cloudformation:UpdateStack",
                    "cloudformation:CreateChangeSet",
                    "cloudformation:DeleteChangeSet",
                    "cloudformation:DescribeChangeSet",
                    "cloudformation:ExecuteChangeSet",
                    "cloudformation:SetStackPolicy",
                    "cloudformation:ValidateTemplate",
                    "cloudformation:DescribeStackResources",
                    "s3:DeleteBucket",
                    "lambda:*",
                    "events:*",
                    "sqs:*",
                    "apigateway:*",
                    "dynamodb:*",
                    "cloudfront:*",
                    "SNS:*",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeVpcs",
                    "logs:*",
                ],
            )
        )

        # sns_topic_name = f"{APP_NAME}-sns-topic"
        # sns_subscription_name = f"{APP_NAME}-sns-subscription"
        # sns_topic = sns.Topic(
        #     self,
        #     sns_topic_name,
        #     topic_name=sns_topic_name,
        #     display_name=sns_topic_name,
        # )
        # sns.Subscription(
        #     self,
        #     sns_subscription_name,
        #     topic=sns_topic,
        #     protocol=sns.SubscriptionProtocol.EMAIL,
        #     endpoint=APPROVAL_EMAIL,
        # )

        # approve_stage = pipeline.add_stage(stage_name="Approve")
        # manual_approval_action = codepipeline_actions.ManualApprovalAction(
        #     action_name="Approve", notification_topic=sns_topic
        # )
        # approve_stage.add_action(manual_approval_action)

        build_action = codepipeline_actions.CodeBuildAction(
            action_name="BuildAndDeploy",
            project=build_project,
            input=source_output,
            run_order=2,
        )

        build_stage = pipeline.add_stage(stage_name="Build")
        build_stage.add_action(build_action)
