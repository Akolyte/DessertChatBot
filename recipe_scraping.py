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
    class_pattern = re.compile(r'mntl-structured-ingredients__')
    #previous class pattern mntl-structured-ingredients__list-heading
    #comp mntl-structured-ingredients__heading mntl-text-block
    elements = soup.find_all('h2',class_=class_pattern)

    ul_pattern = re.compile(r"mntl-structured-ingredients__list")
    ingredient_pattern = re.compile(r"mntl-structured-ingredients__list-item")
    #recipe_title_dict = {}
    ingredients_dict = {}

    #{recipe name: {ingredients: {} , directions: {}}}
    #{recipe name: {ingredients1: {} ,ingredients2: {} , directions: {}}}
    if elements:
        ul_elements = soup.find_all('ul',class_=ul_pattern)
        for ul_element in ul_elements:
            ingredients = ul_element.find_all('li',class_ = ingredient_pattern)
            for index, ingredient in enumerate(ingredients):
                if ingredient.find('span',attrs={"data-ingredient-quantity":"true"}):
                    quantity = ingredient.find('span',attrs={"data-ingredient-quantity":"true"}).text
                else:
                    quantity = None
                if ingredient.find('span',attrs={"data-ingredient-unit":"true"}):
                    unit = ingredient.find('span',attrs={"data-ingredient-unit":"true"}).text
                else: 
                    unit = None
                if ingredient.find('span',attrs={"data-ingredient-name":"true"}):
                    ingredient_name = ingredient.find('span',attrs={"data-ingredient-name":"true"}).text
                else:
                    ingredient_name = None

                ingredients_part_dict = {}
                ingredients_part_dict['quantity'] = quantity
                ingredients_part_dict['unit'] = unit
                ingredients_part_dict['ingredient_name'] = ingredient_name
                ingredients_dict[index] = ingredients_part_dict
    
    else:
        ul_element = soup.find(class_=ul_pattern)
        ingredients = ul_element.find_all(class_ = ingredient_pattern)

        for index, ingredient in enumerate(ingredients):
            if ingredient.find('span',attrs={"data-ingredient-quantity":"true"}):
                quantity = ingredient.find('span',attrs={"data-ingredient-quantity":"true"}).text
            else:
                quantity = None
            if ingredient.find('span',attrs={"data-ingredient-unit":"true"}):
                unit = ingredient.find('span',attrs={"data-ingredient-unit":"true"}).text
            else: 
                unit = None
            if ingredient.find('span',attrs={"data-ingredient-name":"true"}):
                ingredient_name = ingredient.find('span',attrs={"data-ingredient-name":"true"}).text
            else:
                ingredient_name = None

            ingredients_part_dict = {}
            ingredients_part_dict['quantity'] = quantity
            ingredients_part_dict['unit'] = unit
            ingredients_part_dict['ingredient_name'] = ingredient_name
            ingredients_dict[index] = ingredients_part_dict

    return ingredients_dict 

def main():
    recipe_dict = {}
    with open('recipe_links.txt', 'r', encoding = "utf-8") as file:
        lines = file.readlines()
        for line in lines:
            soup = cook_soup(line.strip())
            #<span class="mntl-attribution__item-descriptor">By</span>
            not_recipe_pattern = re.compile(r"mntl-attribution__item-descriptor")
            #article_pattern = re.compile(r"mntl-sc-block-featuredlink__link mntl-text-link button--contained-standard type--squirrel")
            #if (soup.find('a',article_pattern) != None) or ():
            if soup.find('span',not_recipe_pattern).text.strip() != "Recipe by":
                continue
            else:
                recipe_title = find_recipe_title(soup)
                print(recipe_title)
                recipe_dict[recipe_title] = find_ingredients(soup)
        
if __name__ == "__main__":
    main()

#TODO Fix multi-dictionary stucture for ingredients
#TODO Create JSON File from dictionary
