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
        
        llm = ChatOpenAI(model_name='gpt-4')
        
       
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
 

        documents = get_text_chunks_langchain(str(text))

        
        # Get your splitter ready
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

        # # Split your docs into texts
        texts = text_splitter.split_documents(documents)


        print(type(texts))

        print("Sm_llm_embeddings",OpenAIEmbeddings)

        embeddings = OpenAIEmbeddings()
        
        


        # if data_source == "cii":
        #     vector_db=FAISS.from_documents(texts, embedding=embeddings
        #                            )
        #     vector_db.save_local("faiss_index")

        #     new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
        #     # docsearch = FAISS.from_documents(texts, embeddings).save_local("gpt_store","merged_all_books_a")
            
        #     # docsearch = FAISS.load_local(folder_path = "gpt_store",embeddings = embeddings, index_name = 'merged_all_books_a',allow_dangerous_deserialization=True)
        #     # docsearch = FAISS.load_local("merged_all_books", embeddings,allow_dangerous_deserialization=True)

        #     print("**************",new_db)

        #     return new_db
        # else :
        #     docsearch = FAISS.from_documents(texts, embeddings)
            

        
        docsearch = FAISS.from_documents(texts, embeddings)
        
        docs = docsearch.similarity_search(query=question, k=10)


        prompt_template = """Based on the information given, answer the question asked from the context that a 5-year-old can understand. If the answer isn't in the context, try to use your own knowledge and give crisp answers.
                ###
                context: {context}
                ###
                Question: {question}

                Answer:""".strip()
        
        

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        llm.model_kwargs = {
                "temperature": 0.9,
        }
        chain = load_qa_chain(llm=llm, prompt=PROMPT)

        result = chain({"input_documents": docs, "question": question}, return_only_outputs=False)[
            "output_text"
        ]

        return result