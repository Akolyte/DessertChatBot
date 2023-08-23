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
            soup = cook_soup(line.strip(),0)
            if not is_recipe(soup):
                continue
            else:
                recipe_title = find_recipe_title(soup).strip()
                print(recipe_title)
                instructions_list.append(find_instructions(soup,recipe_title))
            if count == 10:
                break
            count += 1
            
    file_path = "instructions.json"

    # Open the file in write mode
    with open(file_path, "w") as json_file:
        # Write the dictionary to the file in JSON format
        json.dump(instructions_list, json_file)

    print("Dictionary written to JSON file successfully.")

def cook_soup(URL, request_limit):
    timeout = 10
    if request_limit == 10:
        print("Reached request limit")
        return None
    else:
        request_limit += 1
    try:
        response = requests.get(URL, timeout=timeout)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    except requests.exceptions.Timeout:
        print(f"Request timed out after {timeout} seconds.")  
        return cook_soup(URL, request_limit)    
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
    li_element = soup.find_all('li',class_ = li_pattern)
    recipe_dict = {}
    instructions_dict = {}
    for index,element in enumerate(li_element):
        index +=1
        instructions_dict[f'Step {index}'] = element.text.strip()
    recipe_dict[recipe_title] = instructions_dict
    return recipe_dict

if __name__ == "__main__":
    main()