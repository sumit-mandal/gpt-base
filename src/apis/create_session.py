import uuid,json,ast
from flask_restx import Namespace ,Resource
from services.s3_helper import put_presigned_url
from config.config import S3_SAVE_INPUT_BUCKET
from flask import session


ns_session_api = Namespace('session_api',description = "api for creating session ")

@ns_session_api.route('/',methods=['POST'])
class Redirect(Resource):
    
    def post(self):

        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        file_name_presigned_url = put_presigned_url(session_id)

        session_data = {"session_id":session_id,
                        "presigned_url":file_name_presigned_url}
        
        session_data_json = json.dumps(session_data)

        response = ast.literal_eval(session_data_json)

        

        return response
    