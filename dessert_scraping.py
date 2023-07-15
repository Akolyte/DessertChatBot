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

def get_nonnested_links(current_layer, visited, nonnested):
    for link in current_layer:
        if link in visited:
            continue
        visited.add(link)
        soup = cook_soup(link)
        child_links = find_links(soup)

        if not child_links:
            nonnested.add(link)

        else:
            get_nonnested_links(child_links, visited, nonnested)

    return visited, nonnested

def main():
    URL = "https://www.allrecipes.com/recipes/79/desserts/"
    _,nonnested = get_nonnested_links([URL], set(), set())
    with open('nonnested_links.txt', 'w', encoding = "utf-8") as file:
        for link in nonnested:
            file.write(f"{link}\n")
    print("done")

if __name__ == "__main__":
    main()
