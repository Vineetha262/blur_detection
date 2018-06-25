# import the necessary packages
from imutils import paths
import argparse
import cv2
import csv
import os #to get file creation time
import math
import datetime

 
def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
    help="path to save the grabbed images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
    help="focus measures that fall below this value will be considered 'blurry'")
ap.add_argument("-o", "--output", required=True,
    help="Specifies the CSV file for the output to be written to")
ap.add_argument("-v", "--video_input", required=True,
	help="Specifies the input video")
ap.add_argument("-c", "--capture_interval", type=int, default=1,
	help="Specifies the interval at which a frame must be captured (in seconds). Default is 1")
args = vars(ap.parse_args())


videoFile = args["video_input"]
imagesFolder = args["images"]
outputCSV = open(args["output"], 'w', newline='')#new line parameter to prevent extra new lines https://stackoverflow.com/a/3348664
interval = args["capture_interval"]

#extracting 1 frame every second
cap = cv2.VideoCapture(videoFile)
frameRate = cap.get(5) #frame rate
totalFrameDigit = len(str(cap.get(7))) #number of digits of total number of frames. We'll use this for formatting the output later
print(totalFrameDigit)
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    #if (frameId % math.floor(frameRate) == 0):
    if (frameId % (math.floor(frameRate)*interval) == 0):
        filename = imagesFolder + "/image_" +  str(int(frameId)).zfill(totalFrameDigit) + ".jpg" #here's where we use totalFrameDigit. Images get saved as IMG 001, IMG 023, IMG 300. Used for listing alphabetically
        cv2.imwrite(filename, frame)
cap.release()
print("Done extracting frames!")


writtenData=[] #array to hold the data we'll write to the csv

vidcap = cv2.VideoCapture(args["video_input"])


# loop over the input images
for imagePath in paths.list_images(args["images"]): #this gives alphabetical list, so be sure to sort your file names accordingly
    # load the image, convert it to grayscale, and compute the
    # focus measure of the image using the Variance of Laplacian
    # method
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    isBlurry = "not blurry"
 
    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
    if fm < args["threshold"]:
        isBlurry = "blurry"
    rowData=[]
    rowData.extend([os.path.abspath(imagePath),isBlurry,fm,os.path.getctime(imagePath),datetime.datetime.fromtimestamp(
        int(os.path.getctime(imagePath))
    ).strftime('%Y-%m-%d %H:%M:%S')
	])
    writtenData.append(rowData)

with outputCSV:
    writer = csv.writer(outputCSV)
    writer.writerows(writtenData)
     
print("Writing complete")