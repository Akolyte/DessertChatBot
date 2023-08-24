import json
import urllib.parse
from pymongo import MongoClient

def main():
    dbname = get_database()
    collection_name = dbname['recipes']

    # Read the JSON file
    with open('web_scraping/ingredients.json', 'r') as file:
        json_data = json.load(file)

    # Insert the JSON data into the collection
    for json_obj in json_data:
        result = collection_name.insert_one(json_obj)

        # Print the inserted document IDs
        print('Inserted document IDs:', result.inserted_id)

def get_database():
    # MongoDB connection parameters
    host = 'dessert-chatbot-cluster.ulib92l.mongodb.net'
    username = 'hryoo2004'
    password = 'gtl4D7iR1QkVz2ZS'

    # Escape the username and password
    escaped_username = urllib.parse.quote(username)
    escaped_password = urllib.parse.quote(password)

    # Build the connection string
    connection_string = f"mongodb+srv://{escaped_username}:{escaped_password}@{host}/?retryWrites=true&w=majority" 

    # Establish a connection to MongoDB
    client = MongoClient(connection_string)
    return client['Dessert-ChatBot-Cluster']

if __name__ == '__main__':
    main()
