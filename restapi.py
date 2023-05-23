from flask import Flask, request, jsonify
from pymongo import MongoClient


import xml.etree.ElementTree as ET
import os
import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    return json.dumps(_element_to_dict(root))

def _element_to_dict(element):
    result = {}
    if element.attrib:
        result["@attributes"] = element.attrib
    if element.text:
        result["text"] = element.text.strip()
    for child in element:
        child_data = _element_to_dict(child)
        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO"))
db = client['maven-packages']
mavenpackages = db['maven_packages']


# Configure MongoDB connection
@app.route('/data', methods=['POST'])
def handle_data():
    xml_data = request.data
    json_data = xml_to_json(xml_data)
    print(json_data)
    dict_data = json.loads(json_data)


    # Insert data into MongoDB collection
    mavenpackages.insert_one(dict_data)
    return 'Data stored successfully'

@app.route('/data', methods=['GET'])
def get_data():
    # Fetch all data from MongoDB collection
    stored_data = mongo.db.collection_name.find()

    # Prepare the data to be returned as JSON
    data_list = []
    for data in stored_data:
        data_list.append({
            'field1': data['field1'],
            'field2': data['field2'],
            # Add more fields as needed
        })

    return jsonify(data_list)


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5006)


