import urllib.parse
from pymongo import MongoClient

def lambda_handler(event, context):
    print('received request: ' + str(event))
    recipe_name_input = event["sessionState"]["intent"]["slots"]["RecipeName"]["value"]["originalValue"]
    slots = event['sessionState']['intent']['slots']
    recipe = get_recipe_by_name(recipe_name_input)
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": "BookHotel",
                "state": "Fulfilled"
            }
        },
        "messages": [{
            "contentType": "PlainText",
            "content": f"{recipe}"
        }]
    }

    return response
    
def get_recipe_by_name(recipe_name):
    dbname = get_database()
    collection = dbname['ingredients']
    query = {"recipe_name":recipe_name}
    result = collection.find_one(query)
    print(result)
    ingredients_dict = result['ingredients']['Ingredients']
    instructions_dict = result['instructions']
    plain_text = "Ingredients:\n\n"

    for ingredient in ingredients_dict.values():
        quantity = ingredient['quantity']
        unit = ingredient['unit']
        name = ingredient['ingredient_name']
        plain_text += f"{quantity} {unit} {name}\n"

    plain_text += "\nInstructions:\n\n"

    for index, instruction in instructions_dict.items():
        plain_text += f"{int(index) + 1}. {instruction}\n"

    return plain_text
    
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
