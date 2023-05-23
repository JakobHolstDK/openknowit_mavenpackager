from flask import Flask, request
from flask_pymongo import PyMongo
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)

# Define a route to handle the XML data
@app.route('/data', methods=['POST'])
def handle_data():
    xml_data = request.data

    # Parse XML
    root = ET.fromstring(xml_data)

    # Extract data from XML and store in MongoDB
    data = {
        'field1': root.find('field1').text,
        'field2': root.find('field2').text,
        # Add more fields as needed
    }

    # Insert data into MongoDB collection
    mongo.db.collection_name.insert_one(data)

    return 'Data stored successfully'

if __name__ == '__main__':
    app.run(debug=True)
