from flask_restx import Api


from apis.ask_question import ns_ask_question_api,ns_parent_retriever_api
from apis.answer_embeddings import ns_answer_api
from apis.simple_responder import ns_simple_responder

rest_api = Api()


rest_api.add_namespace(ns_ask_question_api)

rest_api.add_namespace(ns_parent_retriever_api)

rest_api.add_namespace(ns_answer_api)

rest_api.add_namespace(ns_simple_responder)
