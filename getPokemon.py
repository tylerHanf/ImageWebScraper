from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

'''
-------------------------------------------------------
Author: Tyler Hanf
A basic web scraping utility for getting images using 
Bings Image Search API and storing such images in folder
-------------------------------------------------------
'''

'''
Gets an API key from .env file
'''
def getAPIKey():
    env_path = Path('.') / 'key.env'
    load_dotenv(dotenv_path=env_path)
    return os.getenv("KEY")

'''
Get a correctly formatted url
'''
def getURL(img):
    return "{}".format(img.content_url)

'''
Store an image given path, filename, and 
the downloaded image
'''
def storeImage(path, filename, imageData):
    try:
        with open(path + filename, 'wb') as handler:
            handler.write(imageData)
            print("Saved", filename, "to", path, "\n")
    except:
        print("Failed to save or open")

'''
Takes image results and saves each image 
to a file
'''
def getAllImages(offset, search_term):
    image_results = client.images.search(query=search_term, count=50, offset=offset)
    return image_results

'''
Get an entire image batch and save
each image in the correct folder
'''
def getImage(url):
    try:
        print("Getting image:", url)
        img_data = requests.get(url, timeout=(5, 14)).content
        return img_data
    except:
        print("Error getting image:", url) 

key = getAPIKey()

BATCH_SIZE = 50
img_count = int(input("Enter how many images you need: "))
search_term = input("Enter the query: ")
path = "./" + search_term + "/"
os.makedirs(path, exist_ok=True)

client = ImageSearchAPI(CognitiveServicesCredentials(key))

for batch in range(0, img_count, BATCH_SIZE):
    image_results = getAllImages(batch, search_term) 
    if image_results.value:
        imageNum = 0
        for imageCount in range(len(image_results.value)):
            url = getURL(image_results.value[imageCount])
            img_data = getImage(url)
            if img_data:
                filename = search_term + "_" + str(imageNum + batch)
                storeImage(path, filename, img_data)
                imageNum += 1
