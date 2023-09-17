from database_util import get_database

def main():
    dbname = get_database()
    collection = dbname['recipes']
    collection.create_index([("recipe_name_interpreted_value", "text")])
    print("Done!")
    
if __name__ == '__main__':
    main()
