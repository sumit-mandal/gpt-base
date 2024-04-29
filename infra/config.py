import os

from dotenv import load_dotenv

load_dotenv()

AWS_TAG_PROJECT_NAME = os.environ["AWS_TAG_PROJECT_NAME"]
STAGE = os.environ["STAGE"]

APP_NAME = f"sahara-nsh-AI-{STAGE}"
print(APP_NAME)

AWS_TAG_CREATED_BY = os.environ["AWS_TAG_CREATED_BY"]

DEPLOYMENT_BUCKET = os.environ["DEPLOYMENT_BUCKET"]

GITHUB_REPO=os.environ['GITHUB_REPO']
GITHUB_OWNER=os.environ['GITHUB_OWNER']
AWS_CODESTAR_ARN=os.environ['AWS_CODESTAR_ARN']


DEBUG=os.environ["DEBUG"]
STAGE=os.environ["STAGE"]
REGION=os.environ["REGION"]
S3_BUCKET_NAME=os.environ["S3_BUCKET_NAME"]
S3_SAVE_INPUT_BUCKET=os.environ["S3_SAVE_INPUT_BUCKET"]
SAGEMAKER_ENDPOINT=os.environ["SAGEMAKER_ENDPOINT"]
SERVERLESS_DEPLOYMENT_BUCKET=os.environ["SERVERLESS_DEPLOYMENT_BUCKET"]
S3_EMBEDDINGS_PATH=os.environ["S3_EMBEDDINGS_PATH"]
EMBEDDINGS_ENDPOINT=os.environ["EMBEDDINGS_ENDPOINT"]
VPC_SUBNET_ID_2=os.environ["VPC_SUBNET_ID_2"]
VPC_SUBNET_ID_1=os.environ["VPC_SUBNET_ID_1"]
VPC_SECURITY_GROUP=os.environ["VPC_SECURITY_GROUP"]
ANUBHAV_EMBEDDINGS=os.environ["ANUBHAV_EMBEDDINGS"]
