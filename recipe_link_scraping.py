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

def find_links(soup):
    # Find elements by class using a regular expression
    id_pattern = re.compile(r'mntl-card-list-items')
    elements = soup.find_all(id=id_pattern)
    links = []
    for element in elements:
        links.append(element.get('href'))
    return links

def main():
    recipe_links = []
    with open('nonnested_links.txt', 'r', encoding = "utf-8") as file:
        lines = file.readlines()
        for line in lines:
            soup = cook_soup(line.strip())
            current_recipe_links = find_links(soup)
            recipe_links += current_recipe_links
            

    with open('recipe_links.txt', 'w', encoding = "utf-8") as file:
        for link in recipe_links:
            file.write(f"{link}\n")

        print("done")

if __name__ == "__main__":
    main()