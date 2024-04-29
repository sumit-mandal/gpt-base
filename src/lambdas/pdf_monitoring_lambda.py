import urllib.parse
import boto3
import json
from src.config.config import S3_EMBEDDINGS_PATH,EMBEDDINBGS_STAGE,EMBEDDINGS_ENDPOINT,S3_BUCKET_NAME
from src.utils.sagemaker_call import endpoint_call_monitoring_lambda
from src.services.logger import logger
runtime = boto3.Session().client("sagemaker-runtime", verify=False)


def lambda_handler(event,context):
    if event:
        
        s3_records = event['Records'][0]
        file_name = urllib.parse.unquote_plus(s3_records['s3']['object']['key'])
        logger.info(f"FILENAME -----> {file_name}")
        
        chunk_size = 2000
        chunk_overlap = 20
        bm25_retriever_k = 3

        logger.info(f"S3_EMBEDDINGS_PATH {S3_EMBEDDINGS_PATH}")

        payload = {"task": "embeddings","file_path":file_name,"chunk_size":chunk_size,
                   "chunk_overlap":chunk_overlap,
                   "embeddings_bucket":S3_EMBEDDINGS_PATH,"bucket_cv":S3_BUCKET_NAME,
                   "bm25_retriever_k":bm25_retriever_k}
        
        
        
        payload_parent = {"task": "parent_embeddings","file_path":file_name,"chunk_size":chunk_size,
                   "chunk_overlap":chunk_overlap,
                   "embeddings_bucket":S3_EMBEDDINGS_PATH,"bucket_cv":S3_BUCKET_NAME}
        
        
        

        result = endpoint_call_monitoring_lambda(payload, EMBEDDINGS_ENDPOINT)

        logger.info(f"something is happening and we are moving forward to next parent embnedding----> {result}")
        result = endpoint_call_monitoring_lambda(payload_parent, EMBEDDINGS_ENDPOINT)
        
        
        
       
        logger.info(f"result, {result}")
        
        return "Monitoring Lambda Success"

