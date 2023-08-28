import urllib.parse
from pymongo import MongoClient
import random

def lambda_handler(event, context):
    print('received request: ' + str(event))
    intent_name = event["sessionState"]["intent"]["name"]
    print(intent_name)
    if intent_name == "GetRecipeByName":
        recipe_name_input = event["sessionState"]["intent"]["slots"]["RecipeName"]["value"]["interpretedValue"]
        # TODO Remove special characters from recipe_name_input
        recipe = get_recipe_by_name(recipe_name_input)
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "GetRecipeByName",
                    "state": "Fulfilled"
                }
            },
            "messages": [{
                "contentType": "PlainText",
                "content": f"{recipe}"
            }]
        }
    
        return response
    elif intent_name == "Get3RandomRecipes":
        print('received request: ' + str(event))
        recipes = get_random_recipe()
        recipe_names_string = ""
        for index, recipe in enumerate(recipes):
            name = recipe["recipe_name"]
            recipe_names_string += f"{index+1}. {name}\n"
        recipe_names_string += f"\n Please type one of the desserts you would like the recipe for!"
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "Get3RandomRecipes",
                    "state": "Fulfilled"
                }
            },
            "messages": [{
                "contentType": "PlainText",
                "content": f"{recipe_names_string}"
            }]
        }
    
        return response
    
def get_recipe_by_name(recipe_name):
    dbname = get_database()
    collection = dbname['recipes']
    query = {"recipe_name_interpreted_value":recipe_name}
    result = collection.find_one(query)
    key = 'sub_recipes'
    if key in result.keys():
        ingredients_dict = result['sub_recipes']['ingredients']
    else:
        ingredients_dict = result['ingredients']
    
    instructions_dict = result['instructions']
    plain_text = "Ingredients:\n\n"

    for ingredient in ingredients_dict.values():
        quantity = ingredient['quantity']
        unit = ingredient['unit']
        name = ingredient['ingredient_name']
        if unit is None and quantity is None:
            plain_text += f"{name}\n"
        elif unit is None:
            plain_text += f"{quantity} {name}\n"
        elif quantity is None:
            plain_text += f"{unit} {name}\n"
        else:
            plain_text += f"{quantity} {unit} {name}\n"

    plain_text += "\nInstructions:\n\n"

    for index, instruction in instructions_dict.items():
        plain_text += f"{int(index) + 1}. {instruction}\n"

    return plain_text
    
def get_random_recipe():
    random_documents = []
    dbname = get_database()
    collection = dbname['recipes']

    # Generate a random filter/query
    total_documents = collection.count_documents({})
    random_index = [random.randint(0, total_documents - 1) for _ in range(3)]
    for i in random_index:
        random_documents.append(collection.find().skip(i).limit(3)[0])

    recipe_names = []
    for recipe in random_documents:
        interpreted_value = recipe["recipe_name_interpreted_value"]
        recipe_name = recipe["recipe_name"]
        recipe_names.append({"interpreted_value":interpreted_value, "recipe_name":recipe_name})

    return recipe_names
    
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
