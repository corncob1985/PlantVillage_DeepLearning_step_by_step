# USAGE
# python stress_test.py

# import the necessary packages
from threading import Thread
import requests
import time

# initialize the Crop Diseases Detection APP endpoint URL along with the input
# image path
CROP_DISEASES_APP_URL = "http://localhost:8080/predict"
IMAGE_PATH = "corn_northern_leaf_blight.JPG"

# initialize the number of requests for the stress test along with the sleep amount between requests
NUM_REQUESTS = 500
SLEEP_COUNT = 0.05


def call_predict_endpoint(n):
    # load the input image and construct the payload for the request
    image = open(IMAGE_PATH, "rb").read()
    payload = {"image": image}

    # submit the request
    r = requests.post(CROP_DISEASES_APP_URL, files=payload).json()

    # ensure the request was successful
    if r["success"]:
        print("[INFO] thread {} OK".format(n))

    # otherwise, the request failed
    else:
        print("[INFO] thread {} FAILED".format(n))


# loop over the number of threads
for i in range(0, NUM_REQUESTS):
    # start a new thread to call the APP
    t = Thread(target=call_predict_endpoint, args=(i,))
    t.daemon = True
    t.start()
    time.sleep(SLEEP_COUNT)

# insert a long sleep so we can wait until the server finished processing the images
time.sleep(300)
