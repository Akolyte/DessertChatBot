import urllib.parse
from pymongo import MongoClient

def main(recipe_name):
    dbname = get_database()
    collection = dbname['ingredients']
    query = {"recipe_name":recipe_name}
    result = collection.find_one(query)
    print(result)
    ingredients_dict = result['ingredients']['Ingredients']
    instructions_dict = result['instructions']
    plain_text = "Ingredients:\n"

    for ingredient in ingredients_dict.values():
        quantity = ingredient['quantity']
        unit = ingredient['unit']
        name = ingredient['ingredient_name']
        plain_text += f"{quantity} {unit} {name}\n"

    for instruction in instructions_dict.values():
        plain_text += f"{instruction}\n"

    print(plain_text)
    
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
    main("Rhubarb Cobbler")
