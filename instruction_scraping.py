import requests
import re
import json
from bs4 import BeautifulSoup

def main():
    instructions_list = []
    with open('recipe_links.txt', 'r', encoding = "utf-8") as file:
        lines = file.readlines()
        count = 0
        for line in lines:
            soup = cook_soup(line.strip())
            if not is_recipe(soup):
                continue
            else:
                recipe_title = find_recipe_title(soup).strip()
                print(recipe_title)
                instructions_list.append(find_instructions(soup,recipe_title))
            count += 1
            if count == 5:
                break
        
        print(instructions_list)

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

def find_instructions(soup,recipe_title):
    li_pattern = re.compile(r'comp mntl-sc-block-group--LI')
    text_pattern = re.compile(r'comp mntl-sc-block mntl-sc-block-html')
    li_element = soup.find_all('li',class_ = li_pattern)
    recipe_dict = {}
    for index,element in enumerate(li_element):
        instructions_dict = {}
        index +=1
        step = element.find(class_ = text_pattern)
        instructions_dict[f'Step {index}'] = step.text
    recipe_dict[recipe_title] = instructions_dict
    return recipe_dict
        

"""         steps = element.find_all(class_ = text_pattern)
            for index,step in enumerate(steps):
            instructions_dict = {}
            index +=1
            instructions_dict[f'Step {index}'] = step.text
        recipe_dict[recipe_title] = instructions_dict
    return len(li_element) """

if __name__ == "__main__":
    main()