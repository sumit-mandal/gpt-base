from flask import request, session
from flask_restx import Namespace, Resource
import boto3,re
import json
import uuid
from boto3 import Session
from config.config import S3_EMBEDDINGS_PATH,EMBEDDINGS_ENDPOINT,S3_BUCKET_NAME,ANUBHAV_EMBEDDINGS
from utils.sagemaker_call import call_endpoint_pass_video
from services.logger import logger

import json

runtime = boto3.client("sagemaker-runtime", verify=False)


ns_ask_anubhav_api = Namespace('ask_anubhav', description="api for asking anubhav")


@ns_ask_anubhav_api.route('/', methods=['POST'])
class Anubhav_load(Resource):
    def post(self):
        try:
            session_id = request.form.get("session_id")
            
            logger.info("FORM Session")
        except:
            session_id = session.get("session_id")
            logger.info("FLASK Session")

        question = request.form.get("question")

        logger.info(f"Session_ID-----> {session_id}")

        logger.info(f"ANUBHAV_EMBEDDINGS baad m {ANUBHAV_EMBEDDINGS}")

        faiss_path = ANUBHAV_EMBEDDINGS+"csv" + ".faiss"
        pkl_path = ANUBHAV_EMBEDDINGS+"csv" + ".pkl"


        
        k = 50
        child_chunk_size = 100
        child_chunk_overlap = 20
        fetch_k_parent = 10

        question_uuid = "qs_" + str(uuid.uuid4())
        


        
        payload = {"task": "anubhav_load_embeddings","session_id": session_id,"question": question,
                "faiss_path": faiss_path,"pkl_path": pkl_path,"k": k,"fetch_k": fetch_k_parent,
                "bucket_cv":S3_BUCKET_NAME,"child_chunk_size":child_chunk_size,"child_chunk_overlap":child_chunk_overlap}
        
        result = call_endpoint_pass_video(payload, EMBEDDINGS_ENDPOINT)

        converted_data = {
            "Answer": [
                {
                    "title": item["excerpt"].split("\n")[0][7:],
                    "url": item["excerpt"].split("\n")[-1][5:],   
                }
                for item in result["Answer"]
            ],
            "metadata_info":[]
        }

        converted_data['question_uuid'] = question_uuid
        
        

        return converted_data