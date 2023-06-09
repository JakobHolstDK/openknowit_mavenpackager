from flask import Flask, request, jsonify
from pymongo import MongoClient
import pprint
from bson import json_util



pp = pprint.PrettyPrinter(indent=4)

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
    dict_data = json.loads(json_data)
    print(type(dict_data))



    # Insert data into MongoDB collection
    mavenpackages.insert_one(dict_data)
    return 'Data stored successfully'

@app.route('/', methods=['GET'])
def get_maven_packages():
    maven_packages = db['maven_packages']
    return json.loads(json_util.dumps(maven_packages.find()))


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5006)


