import json
from database_util import get_database

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
    print("Done!")

if __name__ == '__main__':
    main()
