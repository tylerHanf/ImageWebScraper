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
images that can be pulled at a time with the API) and the
default number of images to scrape is 1000. 
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
def checkEncoding(encodeFormat, image):
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
def getAllImages(offset, searchTerm, client):
    global BATCH_SIZE
    imageResults = client.images.search(query=searchTerm, count=BATCH_SIZE, offset=offset)
    return imageResults

'''
Get an entire image batch and save
each image in the correct folder
'''
def getImage(img):
    try:
        print("Getting image:", img)
        imgData = requests.get(img, timeout=(5, 14)).content
        return imgData
    except:
        print("Error getting image:", img, "\n") 

'''
Check to see if number of downloaded
images is equal to the total image count
'''
def checkForFinish(currentImgCount):
    global TOTAL_IMG_COUNT
    if currentImgCount == TOTAL_IMG_COUNT:
        return True
    return False

'''
Gets and stores an entire batch of images
Returns currentImgCount to update the currentImgCount
'''
def storeOneBatch(imageResults, currentImgCount, searchTerm, path):
    global ENCODE_FORMAT
    global TOTAL_IMG_COUNT
    for imageCount in range(len(imageResults.value)):
        if checkForFinish(currentImgCount):
            break
        if checkEncoding(ENCODE_FORMAT, imageResults.value[imageCount]):
            url = getURL(imageResults.value[imageCount])
            imgData = getImage(url)
            if imgData:
                filename = searchTerm + "_" + str(currentImgCount)
                storeImage(path, filename, imgData)
                currentImgCount += 1
    return currentImgCount

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

#Declare global variables
KEY = getAPIKey()
ENCODE_FORMAT = "png"
BATCH_SIZE = 50
TOTAL_IMG_COUNT = 1000

'''
Main function to scrape and save data
'''
def main():
    global KEY
    global BATCH_SIZE
    global TOTAL_IMG_COUNT

    searchTerm = input("Enter the query: ")
    path = "./" + searchTerm + "/"

    os.makedirs(path, exist_ok=True)

    client = ImageSearchAPI(CognitiveServicesCredentials(KEY))

    currentImgCount = 0
    offset = 0
    timerStart = time.time()

    while currentImgCount < TOTAL_IMG_COUNT:
        imageResults = getAllImages(offset, searchTerm, client) 
        if imageResults.value:
            currentImgCount = storeOneBatch(imageResults, currentImgCount, searchTerm, path)
        #The offset is how many images in should the search start with
        offset += BATCH_SIZE

    print("Scraped", currentImgCount, "images of", searchTerm)
    print("Total scrape time:", printTotalTime(timerStart))

if __name__ == "__main__":
    main()
