from flask import request, session
from flask_restx import Namespace, Resource
import boto3

from boto3 import Session
from config.config import S3_EMBEDDINGS_PATH,EMBEDDINGS_ENDPOINT,S3_BUCKET_NAME,SAGEMAKER_ENDPOINT
# from utils.sagemaker_call import endpoint_call_monitoring_lambda,call_endpoint_pass_video
from services.logger import logger

from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from utils.langchain_string_loader import get_text_chunks_langchain
from utils.helper_api import api_calling_signzy,api_calling_instafinancials,api_calling_cii,insta_combo,json_data_source

from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv

load_dotenv()


ns_ask_question_api = Namespace('ask_question', description="api for asking question ")
runtime = boto3.client("sagemaker-runtime", verify=False)
# boto_sess = Session(profile_name="gen-ai-uat",region_name="ap-south-1")

# runtime = boto_sess.client("sagemaker-runtime", verify=True)

ns_parent_retriever_api = Namespace('ask_question_to_parent',description="api for asking question to parent retriever")

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY






@ns_parent_retriever_api.route('/', methods=['POST'])
class Parent_Retv(Resource):
    def post(self):
        try:
            session_id = request.form.get("session_id")
            
        except:
            session_id = session.get("session_id")
            

        question = request.form.get("question")
        cin = request.form.get("cin")
        
        llm = ChatOpenAI(temperature=0,model_name='gpt-4') 
        
       
        data_source = request.form.get("data_source")

        if data_source == "signzy":
            text = api_calling_signzy(cin)
        elif data_source == "instafinance":
            text = api_calling_instafinancials()
        elif data_source == "cii":
            text = api_calling_cii()
        elif data_source == "instaCombo":
            text = insta_combo()
        elif data_source == "jsonData":
            text = json_data_source()

        # text = "Hello"
 

        documents = get_text_chunks_langchain(str(text))

        
        # Get your splitter ready
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

        # # Split your docs into texts
        texts = text_splitter.split_documents(documents)


        print(type(texts))

        print("Sm_llm_embeddings",OpenAIEmbeddings)

        embeddings = OpenAIEmbeddings()
        

        
        docsearch = FAISS.from_documents(texts, embeddings)
        
        docs = docsearch.similarity_search(query=question, k=10)

        

        # prompt_template = """If the context is not relevant,
        # please answer the question by using your own knowledge about the topic.
        
        # {context}
        
        # Question: {question}
        # """

        prompt_template = """If the context is not relevant, Answer "don't know" don't try to make answers on your own
        
        
        {context}
        
        Question: {question}
        """
        
        

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        llm.model_kwargs = {
                "temperature": 0.00001,
        }
        chain = load_qa_chain(llm=llm, prompt=PROMPT)

        result = chain({"input_documents": docs, "question": question}, return_only_outputs=False)[
            "output_text"
        ]

        if """don't know""" in result:
            template = "you are an intelligent bot who has all the information about indian organisations, Take Question: {question} from users and answer the questions asked"

            prompt = PromptTemplate.from_template(template)

            llm_chain = prompt|llm

            result = llm_chain.invoke("List me top manufacturing companies in south india")

        return {"result":str(result)}
        