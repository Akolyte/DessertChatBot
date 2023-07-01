import requests
import re
from bs4 import BeautifulSoup

def cook_soup(URL):
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
        
    except requests.RequestException as e:
        print('Request failed:', str(e))
        return None

def find_links(soup):
    # Find elements by class using a regular expression
    class_pattern = re.compile(r'taxonomy-nodes__link mntl-text-link type--squirrel-link')
    elements = soup.find_all(class_=class_pattern)
    links = []
    
    for element in elements:
        links.append(element.get('href'))
    return links

def find_category_name(soup):
    class_pattern = re.compile(r'comp mntl-taxonomysc-heading mntl-text-block')
    element = soup.find(class_=class_pattern)
    return element.text

def main():
    URL = "https://www.allrecipes.com/recipes/79/desserts/"
    soup = cook_soup(URL)
    top_layer_links = find_links(soup)
    category_dict = {}
    categories = set()
    
    for link in top_layer_links:
        new_soup = cook_soup(link)
        next_layer_title = find_category_name(new_soup)
        next_layer_links = find_links(new_soup)
        print(next_layer_title,next_layer_links)

        while not next_layer_links:
            for child_link in next_layer_links:
                mini_soup = cook_soup(next_layer_links)
                if mini_soup != None:
                    next_layer_title = find_category_name(mini_soup)
                    next_layer_links = find_links(mini_soup)
                    break
                else:
                    continue
            break    
    
if __name__ == "__main__":
    main()