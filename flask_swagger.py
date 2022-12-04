import sqlite3
import pandas as pd
from flask import Flask, request, jsonify, make_response
from flasgger import Swagger, swag_from, LazyJSONEncoder, LazyString
from data_cleanning import process_csv, process_text


#Initialize Flask API
app = Flask(__name__)
# Assign JSON Encoder
app.json_encoder = LazyJSONEncoder
#For the return of JSON on the right Asc/Dsc
app.config['JSON_SORT_KEYS'] = False  

# Database
db = sqlite3.connect('challenge.db', check_same_thread=False) 
db.row_factory = sqlite3.Row
mycursor = db.cursor()



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
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route":"/docs/"
}

#Initialize swagger tamplate  & config
swagger = Swagger(app, template=swagger_tamplate, config=swagger_config)

@swag_from('docs/home.yml', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return jsonify(
        info="Api data cleansing",
        status_code=200
    )
@swag_from('docs/clean.yml', methods=['POST'])
@app.route('/text_clean_form', methods=['POST'])   
def clean_text():
    text= request.form.get('text')
    cleaned_text= process_text(text)
    return jsonify(raw_text=text,cleaned_text=cleaned_text)

@swag_from("docs/upload.yml", methods=['POST'])
@app.route('/Text_Processing_File', methods=['POST'])

def post_file():
    file = request.files[file]
    df = pd.read_csv(file,encoding='utf-8')
    process_csv(df)
    return jsonify(json)


if __name__ == '__main__':
    app.run(debug=True)
