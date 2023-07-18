import json
import urllib.parse
from pymongo import MongoClient
# MongoDB connection parameters
host = 'dessert-chatbot-cluster.ulib92l.mongodb.net'
port = 27017
#database = 'Dessert-ChatBot-Cluster'
username = 'hryoo2004'
password = 'Ohironjoy@5413'

# Escape the username and password
escaped_username = urllib.parse.quote(username)
escaped_password = urllib.parse.quote(password)

# Build the connection string
connection_string = f"mongodb+srv://{escaped_username}:{escaped_password}@{host}/?connectTimeoutMS=120000"

# Establish a connection to MongoDB
client = MongoClient(connection_string)

# Access a specific database
db = client['Dessert-ChatBot-Cluster']

# Access a specific collection
collection_name = 'ingredients'
collection = db[collection_name]

# Read the JSON file
with open('ingredients.json', 'r') as file:
    json_data = json.load(file)

# Insert the JSON data into the collection
result = collection.insert_one(json_data)

# Print the inserted document IDs
print('Inserted document IDs:', result.inserted_ids)

# Close the connection to MongoDB
client.close()