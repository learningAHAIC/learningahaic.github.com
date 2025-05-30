import requests
from bs4 import BeautifulSoup
import os

def scrape_and_save_items(url, output_file):
    
    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save the raw HTML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
        print(f"Successfully saved page content to {output_file}")
        return soup
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None
    
def load_items_from_html(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        return soup

def download_icons(soup, output_dir):
    
    if not output_dir.endswith('/'):
        output_dir += '/'
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    images_with_class = soup.find_all('img', class_=True)
    # for i in range(1, 20):
    for i in range(len(images_with_class)):
        img = images_with_class[i]
        # print(str(img)[:100])
        try:
            name = f"{output_dir}{img['data-image-name'].replace(' ', '_').replace('/', '_')}"
        except KeyError:
            name = f"{output_dir}image_{i}.png"
        # print(name)
        url = img['src']
        if not url.startswith('https://'):
            url = img['data-src']
        # print(url)
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(name, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {name}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        
        
if __name__ == "__main__":
    items_url = "https://nova-lands.fandom.com/wiki/Items"
    soup = scrape_and_save_items(items_url, "img/items.html")
    # soup = load_items_from_html("img/items.html")
    if soup is None:
        print("Failed to load items from HTML.")
    download_icons(soup, output_dir="img/items/")
    buildings_url = "https://nova-lands.fandom.com/wiki/Buildings"
    soup = scrape_and_save_items(buildings_url, "img/buildings.html")
    # soup = load_items_from_html("img/buildings.html")
    if soup is None:
        print("Failed to load items from HTML.")
    download_icons(soup, output_dir="img/buildings/")