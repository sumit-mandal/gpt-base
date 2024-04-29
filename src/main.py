import os 
from flask import Flask 
import json 
from flask_cors import CORS
from multiprocessing import Process
from dotenv import load_dotenv, dotenv_values
# from services.sqs_service import check_received_message

load_dotenv()

def create_flask_app():
    app = Flask(__name__)
    app.secret_key = b'secret key'
    app.config['CORS_HEADERS'] = 'application/json'
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
    app.url_map.strict_slashes = False
    app.config['ERROR_404_HELP'] = False
    config = dotenv_values()
    app.config.from_mapping(config)
    for i in app.config:
        os.environ[i] = str(app.config[i])
        
    return app


def init_api(flask_app: Flask) -> Flask:
    from apis import rest_api
    rest_api.init_app(flask_app)
    
    return flask_app

app = create_flask_app()
app = init_api(app)


if __name__ == "__main__":
    
    # worker_process = Process(target=check_received_message)
    # worker_process.start()
    app.run(debug=True)