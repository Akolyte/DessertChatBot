import random
from database_util import get_database

def main(recipe_name):
    # print(get_recipe_by_name(recipe_name))
    print(get_random_recipe(recipe_name))

def get_recipe_by_name(recipe_name):
    dbname = get_database()
    collection = dbname['recipes']
    
    query = recipe_name
    result = collection.find_one(
    {"$text": {"$search": query}},
    {"score": {"$meta": "textScore"}}).sort([("score", {"$meta": "textScore"})])
    
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

def get_random_recipe(recipe_name):
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

if __name__ == '__main__':
    main("banoffeepie")
