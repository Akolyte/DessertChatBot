import json
import requests
import re
from bs4 import BeautifulSoup

def main():
    recipe_list = []
    with open('recipe_links.txt', 'r', encoding = "utf-8") as file:
        lines = file.readlines()

        for line in lines:
            soup = cook_soup(line.strip())
            if not is_recipe(soup):
                continue
            else:
                #{recipe name: {ingredients: {} , directions: {}}}
                #{recipe name: {ingredients1: {} ,ingredients2: {} , directions: {}}}
                recipe_title = find_recipe_title(soup).strip()
                print(recipe_title)
                recipe_list.append(find_ingredients(soup,recipe_title))
   
           
    file_path = "ingredients.json"

    # Open the file in write mode
    with open(file_path, "w") as json_file:
        # Write the dictionary to the file in JSON format
        json.dump(recipe_dict, json_file)

    print("Dictionary written to JSON file successfully.")

def cook_soup(URL):
    timeout = 10
    try:
        response = requests.get(URL, timeout=timeout)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    except requests.exceptions.Timeout:
        print(f"Request timed out after {timeout} seconds.")      
    except requests.RequestException as e:
        print('Request failed:', str(e))
        return None
    
def is_recipe(soup):
    not_recipe_pattern = re.compile(r"mntl-attribution__item-descriptor")
    return soup.find('span',not_recipe_pattern).text.strip() == "Recipe by"
    
def find_recipe_title(soup):
    id_pattern = re.compile(r'article-heading_1-0')
    element = soup.find(id=id_pattern)
    return element.text

def find_ingredients(soup,recipe_title):
    class_pattern = re.compile(r'mntl-structured-ingredients__list-heading')
    subheadings = soup.find_all('p',class_=class_pattern)
    
    if subheadings:
        ingredients_dict = find_ingredients_with_multiple_sub_recipes(soup,subheadings)
        
    else:
        ingredients_dict = find_ingredients_with_one_recipe(soup)

    ingredients_dict['name'] = recipe_title
    return ingredients_dict

def find_ingredients_with_multiple_sub_recipes(soup,subheadings):
    ul_pattern = re.compile(r"mntl-structured-ingredients__list")
    ingredient_pattern = re.compile(r"mntl-structured-ingredients__list-item")
    sub_ingredients_dict = {}
    ul_elements = soup.find_all('ul',class_=ul_pattern)
    for index_ul, ul_element in enumerate(ul_elements):
        ingredients = ul_element.find_all('li',class_ = ingredient_pattern)
        ingredients_dict = {}
        for index, ingredient in enumerate(ingredients):
            ingredients_part_dict = {}
            ingredients_part_dict['quantity'] = get_quantity(ingredient)
            ingredients_part_dict['unit'] = get_unit(ingredient)
            ingredients_part_dict['ingredient_name'] = get_ingredient_name(ingredient)
            ingredients_dict[index] = ingredients_part_dict
        
        if index_ul == 0:
            sub_ingredients_dict['Ingredients'] = ingredients_dict
        else:
            sub_ingredients_dict[subheadings[index_ul-1].text] = ingredients_dict

    return sub_ingredients_dict

def find_ingredients_with_one_recipe(soup):
    ul_pattern = re.compile(r"mntl-structured-ingredients__list")
    ingredient_pattern = re.compile(r"mntl-structured-ingredients__list-item")
    ingredients_dict = {}
    ul_element = soup.find(class_=ul_pattern)
    ingredients = ul_element.find_all(class_ = ingredient_pattern)

    for index, ingredient in enumerate(ingredients):
        ingredients_part_dict = {}
        ingredients_part_dict['quantity'] = get_quantity(ingredient)
        ingredients_part_dict['unit'] = get_unit(ingredient)
        ingredients_part_dict['ingredient_name'] = get_ingredient_name(ingredient)
        ingredients_dict[index] = ingredients_part_dict

    return ingredients_dict

def get_quantity(ingredient):
    quantity_span = ingredient.find('span',attrs={"data-ingredient-quantity":"true"})
    if quantity_span:
        return quantity_span.text
    else:
        return None

def get_unit(ingredient):
    unit_span = ingredient.find('span',attrs={"data-ingredient-unit":"true"})
    if unit_span:
        return unit_span.text
    else:
        return None

def get_ingredient_name(ingredient):
    ingredient_name_span = ingredient.find('span',attrs={"data-ingredient-name":"true"})
    if ingredient_name_span:
        return ingredient_name_span.text
    else:
        return None

if __name__ == "__main__":
    main()
