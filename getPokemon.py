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
Store an image given path, filename, and 
the downloaded image
'''
def storeImage(path, filename, imageData):
    try:
        with open(path + filename, 'wb') as handler:
            handler.write(img_data)
            print("Saved", filename, "to", path, "\n")
    except:
        print("Failed to save or open")
    
#Get API key
env_path = Path('.') / 'key.env'
load_dotenv(dotenv_path=env_path)
key = os.getenv("KEY")

search_term = input("Enter the query: ")
path = "./" + search_term + "/"
os.makedirs(path, exist_ok=True)

subscription_key = key

client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))

image_results = client.images.search(query=search_term, count=50)

print("Total number of images returned: {}".format(len(image_results.value)))
fileNum = 0
if image_results.value:
    for image in image_results.value:
        url = "{}".format(image.content_url)
        print("Getting", url)
        try:
            img_data = requests.get(url).content
            filename = search_term + "_" + str(fileNum)
            storeImage(path, filename, img_data)
            fileNum += 1
        except:
            print("Error getting url") 
else:
    print("No image results returned!")
