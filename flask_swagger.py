import sqlite3
import pandas as pd
from flask import Flask, request, jsonify, make_response
from flasgger import Swagger, swag_from, LazyJSONEncoder, LazyString
from data_cleanning import process_text,preprocess
from pathlib import Path


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


db_path = Path(__file__).parent/'dataGold.db'
conn= sqlite3.connect('db_path', check_same_thread=False)

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
    text = request.form.get('text')
    cleaned_text= preprocess(text)
    df_new= pd.DataFrame({'raw_text':[text],'cleaned_text':[cleaned_text]})
    df_new.to_sql('text_cleaning',conn,if_exists='append',index=False)
    json_response= {
        'status_code': 200,
        'description': "cleaning text from user",
        'raw_data': text,
        'clean_data': cleaned_text
    }
    response_data = jsonify(json_response)
    return response_data
    #return jsonify(raw_text=text,cleaned_text=cleaned_text)

@swag_from("docs/upload.yml", methods=['POST'])
@app.route('/Text_Processing_File', methods=['POST'])
def post_file():
    file = request.files.get('file')    
    df = pd.read_csv(file,encoding='latin-1')
    result= []
    for text in df['Tweet']:
        clean = preprocess(text)
        result.append(clean)
    raw=df['Tweet'].to_list()
    df_new1= pd.DataFrame({'raw_text':raw, 'cleaned_text':result})
    df_new1.to_sql('text_cleaning', conn, if_exists='append', index=False)
    df_new1.to_csv('preprocess_data.csv', index=False)
    response_data = jsonify(df_new1.T.to_dict())
    return response_data


if __name__ == '__main__':
    app.run(debug=True)
