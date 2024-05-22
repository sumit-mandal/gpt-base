from langchain.vectorstores import Chroma,FAISS


from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader

from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

from flask import request, session
from flask_restx import Namespace, Resource
import boto3,json


ns_answer_api = Namespace('answer_bot',description="api for asking question to parent retriever")

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY






@ns_answer_api.route('/', methods=['POST'])
class AnswerBot(Resource):
    def post(self):
        current_directory = os.getcwd()
        print("Current Working Directory:*******************", current_directory)
        print("Sm_llm_embeddings",OpenAIEmbeddings)

        sm_llm_embeddings = OpenAIEmbeddings()
        question = request.form.get('question')
        file_name_to_load = request.form.get('file_name_to_load')



        docsearch = FAISS.load_local(folder_path = "faiss_store",embeddings = sm_llm_embeddings, index_name = file_name_to_load,allow_dangerous_deserialization=True)


        # question = "Who is the current director of zydus"

        docs = docsearch.similarity_search(query=str(question), k=10)

        print("################## question",question,docs)

        prompt_template = """Based on the information given, answer the question asked from the context. You need to answer the question properly. 
        However if context seems inappropriate you can reply don't know, only reply don't know when you don't find answer.
        
        ###
        context: {context}
        ###
        Question: {question}

        Answer:""".strip()
        
        

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        llm = ChatOpenAI(temperature=0.5,model_name='gpt-4o') 

        llm.model_kwargs = {
                "temperature": 0.5,
        }
        chain = load_qa_chain(llm=llm, prompt=PROMPT)

        result = chain({"input_documents": docs, "question": question}, return_only_outputs=False)[
            "output_text"
        ]


        
        print("ACtual result from the base model ************",result)
        
        print("tupe of result",type(result))
        if not """don't know""" in result.lower():
            result = result
            # print("Old result",result)

        else:
            llm_self = ChatOpenAI(temperature=0,model_name='gpt-4o') 
            llm_self.model_kwargs = {
                "temperature": 0.5,
            }
            template = """you are an intelligent bot who has all the information about indian organisations, 
            answer the {question} asked"""

            prompt = PromptTemplate.from_template(template)

            llm_chain = prompt|llm_self

            result = llm_chain.invoke(question)
            
            print("new result",(result))
            result = str(result)
            # Find the index of response_metadata
            index = result.find("response_metadata")

            # Extract the substring up to response_metadata
            result = result[:index]
            # result_old = result.content.split('" response_metadata=')[0].strip()
            # return result
            
        
        

        return {"result":result}
        
