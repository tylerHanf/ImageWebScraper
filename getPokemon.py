from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
from pathlib import Path
from dotenv import load_dotenv
import requests
import os
import time

'''
-------------------------------------------------------
Author: Tyler Hanf
A basic web scraping utility for getting images using 
Bings Image Search API and storing such images in folder

It gets images based on the individual batch size.
Because this is suited for gathering data for machine
learning, the default batch size is 50 (the max number of
images that can be pulled at a time with the API). So
when gathering a specific number of images, please request
amounts by factors of 50 or change batch size as appropriate.
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
Checks the encoding format of an image
'''
def checkEncodingFormat(encodeFormat, image):
    if image.encoding_format == 'png':
        return True
    return False

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
        print("Failed to save or open \n")

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
def getImage(img):
    try:
        print("Getting image:", img)
        img_data = requests.get(img, timeout=(5, 14)).content
        return img_data
    except:
        print("Error getting image:", img, "\n") 

'''
Calculates the total run time
'''
def calcTotalTime(startTime):
    return time.time() - startTime
'''
Prints the total runtime based
on the current time minus start time
'''
def printTotalTime(startTime):
    totalTime = calcTotalTime(startTime)
    minutes = int(totalTime/60)
    seconds = int(totalTime % 60)
    if minutes == 0:
        return str(seconds) + "s"
    return str(minutes) + "m " + str(seconds) + "s" 

KEY = getAPIKey()
ENCODE_FORMAT = "png"
BATCH_SIZE = 50

img_count = int(input("Enter how many images you need: "))
search_term = input("Enter the query: ")
path = "./" + search_term + "/"

os.makedirs(path, exist_ok=True)

client = ImageSearchAPI(CognitiveServicesCredentials(KEY))

currentImgCount = 0
offset = 0
timerStart = time.time()

'''
Gets the correct number of images with specific
file encoding 
'''
while currentImgCount < img_count:
    image_results = getAllImages(offset, search_term) 
    if image_results.value:
        for imageCount in range(len(image_results.value)):
            if checkEncodingFormat(ENCODE_FORMAT, image_results.value[imageCount]):
                url = getURL(image_results.value[imageCount])
                img_data = getImage(url)
                if img_data:
                    filename = search_term + "_" + str(currentImgCount)
                    storeImage(path, filename, img_data)
                    currentImgCount += 1
    #The offset is how many images in should the search start with
    offset += BATCH_SIZE

print("Scraped", currentImgCount, "images of", search_term)
print("Total scrape time:", printTotalTime(timerStart))
