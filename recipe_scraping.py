import requests
import re
from bs4 import BeautifulSoup

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
    
def find_recipe_title(soup):
    id_pattern = re.compile(r'article-heading_1-0')
    element = soup.find(id=id_pattern)
    return element.text

def find_ingredients(soup):
    class_pattern = re.compile(r'mntl-structured-ingredients__list-heading')
    elements = soup.find_all(class_=class_pattern)

    ul_pattern = re.compile(r"mntl-structured-ingredients__list")
    ingredient_pattern = re.compile(r"mntl-structured-ingredients__list-item")
    
    #recipe_title_dict = {}
    ingredients_dict = {}

    #{recipe name: {ingredients: {} , directions: {}}}
    #{recipe name: {ingredients1: {} ,ingredients2: {} , directions: {}}}

    if elements:
        ul_elements = soup.find_all(class_=ul_pattern)
        ingredients = ul_elements.find_all(class_ = ingredient_pattern)
        #line 37:AttributeError: ResultSet object has no attribute 'find_all'. 
        #You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?

        for index, ingredient in enumerate(ingredients):
            quantity = ingredient.find('span',attrs={"data-ingredient-quantity":"true"}).text
            unit = ingredient.find('span',attrs={"data-ingredient-unit":"true"}).text
            ingredient_name = ingredient.find('span',attrs={"data-ingredient-name":"true"}).text

            ingredients_part_dict = {}
            ingredients_part_dict['quantity'] = quantity
            ingredients_part_dict['unit'] = unit
            ingredients_part_dict['ingredient_name'] = ingredient_name
            ingredients_dict[index] = ingredients_part_dict
    
    else:
        ul_elements = soup.find(class_=ul_pattern)
        ingredients = ul_elements.find_all(class_ = ingredient_pattern)

        for index, ingredient in enumerate(ingredients):
            quantity = ingredient.find('span',attrs={"data-ingredient-quantity":"true"}).text
            unit = ingredient.find('span',attrs={"data-ingredient-unit":"true"}).text
            ingredient_name = ingredient.find('span',attrs={"data-ingredient-name":"true"}).text

            ingredients_part_dict = {}
            ingredients_part_dict['quantity'] = quantity
            ingredients_part_dict['unit'] = unit
            ingredients_part_dict['ingredient_name'] = ingredient_name
            ingredients_dict[index] = ingredients_part_dict
       

def main():
    recipe_dic = {}
    with open('recipe_links.txt', 'r', encoding = "utf-8") as file:
        lines = file.readlines()
        for line in lines:
            soup = cook_soup(line.strip())
            recipe_title = find_recipe_title(soup)
            find_ingredients(soup)
            recipe_dic[recipe_title] = {}
       
if __name__ == "__main__":
    main()