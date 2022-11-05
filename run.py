# python3 -m pip install opencv-python

# importing OpenCV, time library
import cv2, time, os
import numpy as np
from datetime import date
from PIL import Image
import requests
from io import BytesIO

# importing datetime class from datetime library
from datetime import datetime

PIXEL_CHANGE_THRESHOLD = 30
FREQUENCY = 10
MOTION_PIXEL_THRESHOLD = 5000
FOLDER = "./motion/"
URL = ""

last_pic = None
image = None

def load_image(path):
	start_time = time.time() * 1000
	# Read an image from path as grayscale image
	image = cv2.imread(path, -1)
	print("[%dms] %s" % ((time.time() * 1000 - start_time), "Finished reading image"))
	return image

def load_image_from_url(url):
	start_time = time.time() * 1000
	response = requests.get(url)
	bytes = BytesIO(response.content)
	pil_image = Image.open(BytesIO(response.content))
	cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
	print("[%dms] %s" % ((time.time() * 1000 - start_time), "Finished reading image"))
	return cv2_image

def store_image(image):
	print(FOLDER + str(date.today()) + "/" + datetime.now().strftime("camera-%d-%m-%Y-%H-%M-%S.png"))
	if not os.path.isdir(FOLDER + str(date.today())):
		os.makedirs(FOLDER + str(date.today()))
	cv2.imwrite(FOLDER + str(date.today()) + "/" + datetime.now().strftime("camera-%d-%m-%Y-%H-%M-%S.png"), image)


# Get environment variables
if os.getenv('PIXEL_CHANGE_THRESHOLD') != None:
	PIXEL_CHANGE_THRESHOLD = float(os.getenv('PIXEL_CHANGE_THRESHOLD'))
if os.getenv('FREQUENCY') != None:
	FREQUENCY = float(os.environ.get('FREQUENCY'))
if os.getenv('MOTION_PIXEL_THRESHOLD') != None:
	MOTION_PIXEL_THRESHOLD = float(os.environ.get('MOTION_PIXEL_THRESHOLD'))
if os.getenv('FOLDER') != None:
	FOLDER = os.environ.get('FOLDER')
if os.getenv('URL') != None:
	URL = os.environ.get('URL')

while(True):
	#blur = load_image('./testimages/1.jpeg')
	image = load_image_from_url(URL)
	# Convert to gray scale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Apply Gaussan blur to the loaded image to reduce noise
	start_time = time.time() * 1000
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	print("[%dms] %s" % ((time.time() * 1000 - start_time), "Finished blur"))

	if last_pic is None:
		last_pic = blur
		continue

	start_time = time.time() * 1000
	diff_frame = cv2.absdiff(blur, last_pic)
	print("[%dms] %s" % ((time.time() * 1000 - start_time), "Finished diff"))

	# Current frame is greater than 30 it will show white color(255)
	start_time = time.time() * 1000
	thresh_frame = cv2.threshold(diff_frame, PIXEL_CHANGE_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
	print("[%dms] %s" % ((time.time() * 1000 - start_time), "Finished thresh"))

	# Finding the bounding contour of moving object
	cnts,_ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		print("Motion area size: %d" % cv2.contourArea(contour))
		if cv2.contourArea(contour) < MOTION_PIXEL_THRESHOLD:
			continue
		print("MOTION")
		store_image(image)

	cv2.imshow("blur", blur)
	cv2.imshow("diff", diff_frame)
	cv2.imshow("thresh", thresh_frame)
	
	key = cv2.waitKey(1)
	# if q entered whole process will stop
	if key == ord('q'):
		break
	# Slow it down a bit
	time.sleep(FREQUENCY)
	# Set the current picture as the last picture
	last_pic = blur

	

