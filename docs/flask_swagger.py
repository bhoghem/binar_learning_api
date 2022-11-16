import sqlite3
import pandas as pd
from flask import Flask, request, jsonify, make_response
from flasgger import Swagger, swag_from, LazyJSONEncoder, LazyString

#Initialize Flask API
app = Flask(__name__)
# Assign JSON Encoder
app.json_encoder = LazyJSONEncoder

#Create Swagger config and tamplate

swagger_tamplate = dict(
    info = {
        'title': LazyString(lambda: 'API Data Cleansing'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda:'Documentation Cleansing Data Hate Speach for Gold Challenge')
    },
    host = LazyString(lambda:request.host)
)

swagger_config = {
    "headers": [],
    "specs":[
        {
            "endpoint": 'docs',
            "route": '/docs.json'            
        }
    ],
    "static_url_path":"/flashger_static",
    "swagger_ui": True,
    "specs_route":"/docs/"
}

#Initialize swagger tamplate  & config
swagger = Swagger(app, template=swagger_tamplate, config=swagger_config)

@app.route('/', methods=['GET'])
def home():
    return jsonify(
        info="Api data cleansing"
        status_code=200
    )
   
if __name__ == '__main__':
    app.run(debug=True)
