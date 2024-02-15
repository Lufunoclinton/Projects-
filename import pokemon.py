import requests
from bs4 import BeautifulSoup
import os
import urllib.request

# Function to scrape data and download images from a website
def scrape_and_download(url, save_dir):
    # Create directory if not exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Fetch webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all elements containing data you want to scrape
    pokemon_list = soup.find_all("div", class_="infocard")

    # Iterate over each element
    for pokemon in pokemon_list:
        # Extract Pokemon name and image URL
        name = pokemon.find("span", class_="img-fixed icon-pkmn").get("data-alt").replace("♀", "-female").replace("♂", "-male")
        image_url = pokemon.find("span", class_="img-fixed icon-pkmn").find("span", class_="img-sprite").get("data-src")
        # Download the image
        image_name = f"{name}.png"
        image_path = os.path.join(save_dir, image_name)
        urllib.request.urlretrieve(image_url, image_path)
        print(f"Downloaded {image_name}")

# Example usage:
url = "https://img.pokemondb.net/artwork/large/pikachu.jpg"
save_dir = "pokemon_images"
scrape_and_download(url, save_dir)
