from flask import Flask, request, jsonify
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from flask_restx import Namespace, Resource
import boto3,json

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

ns_simple_responder = Namespace('simple_responder',description="api for asking question to parent retriever")

llm = OpenAI()


base_prompt_template = """
You are an expert on Indian industries. Provide detailed information on the following query:
Query: {query}
Please give a comprehensive response related to the various sectors, trends, and data available in Indian industries.
"""

# Define the LangChain LLMChain with the base prompt template
prompt_template = PromptTemplate(input_variables=["query"], template=base_prompt_template)
chain = LLMChain(llm=llm, prompt=prompt_template)



@ns_simple_responder.route('/', methods=['POST'])
class PlainResponse(Resource):
    def post(self):
        query = request.form.get('query')
        response = chain.run(query=query)

        return response