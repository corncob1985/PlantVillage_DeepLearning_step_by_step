from keras.models import load_model
import tensorflow as tf
import os
import settings
import helpers
import redis
import json
import numpy as np
import time

# connect to Redis server
db = redis.StrictRedis(host=settings.REDIS_HOST,
                       port=settings.REDIS_PORT,
                       db=settings.REDIS_DB)


def classify_process():
    
    # Choose either gpu or cpu for classification.
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    gpu_options = tf.GPUOptions(allow_growth=True)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
    
    print("* Loading model files...")
    model = load_model("/home/gxty/pycharmProjects/plant_disease_detection_project/models/vgg16_keras_stage_1_group.h5")

    plantVillage_labels_filename = "/home/gxty/pycharmProjects/plant_disease_detection_project/temp/class.txt"
    with open(plantVillage_labels_filename, 'rt') as f:
        labels = f.read().split('\n')[:-1]
    
    keras_label = {'0': 0, '1': 1, '10': 2, '11': 3, '12': 4, '13': 5, '14': 6, '15': 7, '16': 8, '17': 9, '18': 10, '19': 11, '2': 12, '20': 13, '21': 14, '22': 15, '23': 16, '24': 17, '25': 18, '26': 19, '27': 20, '28': 21, '29': 22, '3': 23, '30': 24, '31': 25, '32': 26, '33': 27, '34': 28, '35': 29, '36': 30, '37': 31, '4': 32, '5': 33, '6': 34, '7': 35, '8': 36, '9': 37}
    
    label_actual_keras = dict((v, k) for k, v in keras_label.items())
    
    print("* Model files loaded")

    # continually pool for new images to classify
    while True:
        # attempt to grab a batch of images from the database, then initialize the image IDs and
        # batch of images themselves

        start = time.time()

        queue = db.lrange(settings.IMAGE_QUEUE, 0, settings.BATCH_SIZE - 1)
        imageIDs = []
        batch = None

        # loop over the queue
        for q in queue:
            # deserialize the object and obtain the input image
            q = json.loads(q.decode("utf-8"))
            image = helpers.base64_decode_image(q["image"], settings.IMAGE_DTYPE,
                                                (1, settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH, settings.IMAGE_CHANS))

            # check to see if the batch list is None
            if batch is None:
                batch = image

            # otherwise, stack the data
            else:
                batch = np.vstack([batch, image])   # numpy.vstack: stack arrays in sequence vertically (row wise).

            # update the list of image IDs
            imageIDs.append(q["id"])

        # check to see if we need to process the batch
        if len(imageIDs) > 0:
            # classify the batch
            print("* Batch size: {}".format(batch.shape))
            predictions = model.predict(batch)
            
            # loop over the image IDs and their corresponding set of results from our model
            # initialize the list of output predictions
            output = []
            
            for i in np.arange(predictions.shape[0]):
                top_1 = predictions[i, :].flatten().argsort()[-1]
                pred_label = int(label_actual_keras[top_1])
                r = {"imageID": imageIDs[i], "label": labels[pred_label], "probability": float(predictions[i, top_1])}
                output.append(r)

                # store the output predictions in the database, using the image ID as the key
                # so we can fetch the results

                db.set(imageIDs[i], json.dumps(output))

            # remove the set of images from our queue
            db.ltrim(settings.IMAGE_QUEUE, len(imageIDs), -1)
            print("Done in %.2f s." % (time.time() - start))

        # sleep for a small amount
        time.sleep(settings.SERVER_SLEEP)


# if this is the main thread of execution start the model server process
if __name__ == "__main__":
    classify_process()
