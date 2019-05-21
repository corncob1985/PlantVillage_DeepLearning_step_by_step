#!/usr/local/anaconda3/bin/python

import glob
import json
import random
import numpy as np
import os
from os.path import isfile
import math
import shutil

cwd = os.getcwd()
# 31 data types in total, according to the file number under filtered_leafmaps folder.
leaf_map = json.loads(open(cwd + "/" + "processed_datasets/plantVillage/leaf-map.json", "r").read())

INPUT_FOLDER = cwd + "/" + "raw_datasets/images/plantVillage"
OUTPUT_FOLDER = cwd + "/" + "processed_datasets/plantVillage"

def determine_leaf_group(leaf_identifier, className):
    global leaf_map

    try:
        foo = leaf_map[leaf_identifier.lower().strip()]   # leaf_identifier, e.g. 'frec_scab 2907'
        if len(foo) == 1:   # keys with only one value
            return foo[0]   # e.g. 'Apple___Apple_scab:::1'
        else:               # keys with more than one value (2152 keys with 2 values; 20 keys with 3 values)
            for _suggestion in foo:   # ['Blueberry___healthy:::152.0',
                                      # 'Potato___healthy:::38.0',
                                      # 'Soybean___healthy:::304.0']
                if _suggestion.find(className) != -1:
                    return _suggestion   # i.e. 'Potato___healthy:::38.0'
            return str(random.randint(1, 10000000000000000000000))
    except:
        return str(random.randint(1, 10000000000000000000000))   # There are only 31 data types in leaf_map, but there
    # are 38 classes of raw images. Which means images from the missing 7 classes will be allocated into groups with
    # random integer names.


def compute_per_class_distribution(DATASET):
    classMap = {}   # Create an empty dictionary
    count = 0
    for datum in DATASET:
        # [('/.../raw/*/*/0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG', 'Apple___Apple_scab')]
        try:
            classMap[datum[1]].append(datum[0])
            # ['/.../raw/*/*/0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG',
            #  '/.../raw/*/*/4151028c-c8bc-4394-b4a7-aff414864c15___FREC_Scab 3418.JPG']
            count += 1   # Calculate the number of images belonging to the train set or test set.
        except:
            classMap[datum[1]] = [datum[0]]
            count += 1
    for _key in classMap:
        classMap[_key] = len(classMap[_key])   # classMap['Apple___Apple_scab'] =
                                               # the number of images belonging to Apple___Apple_scab

    return classMap


def distribute_buckets(BUCKETS, train_probability):
    train = []   # Create an empty List
    test = []    # Create an empty List

    for _key in BUCKETS.keys():   # 'Apple___Apple_scab:::92.0'
        bucket = BUCKETS[_key]
        # [('/.../raw/*/*/0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG', 'Apple___Apple_scab'),
        #  ('/.../raw/*/*/4151028c-c8bc-4394-b4a7-aff414864c15___FREC_Scab 3418.JPG', 'Apple___Apple_scab')]

        if random.random() <= train_probability:  # random.random() will randomly generate a real number between (0, 1).
            train += bucket
        else:
            test += bucket
    return train, test


folder_name = []
ignored_image = []
ignored_image_absolute_path = []
if isfile(cwd + "/" + "processed_datasets/plantVillage/" + "duplicates.txt"):
    with open(cwd + "/" + "processed_datasets/plantVillage/" + "duplicates.txt", 'rt') as f:
        duplicate_info = f.read().split('\n')[:-1]
        for line in duplicate_info:
            duplicated_image = line.strip().split('\t')[1]
            kept_image = line.strip().split('\t')[2]
            for item in duplicated_image.split(','):
                if item != kept_image:
                    ignored_image.append(item)
                    folder_name.append(line.strip().split('\t')[0])

    print("The duplicated images to be ignored:")                    
    for folder, image in zip(folder_name, ignored_image):
        ignored_image_absolute_path.append(INPUT_FOLDER + "/" + folder + "/" + image)
    
    print('\n'.join(ignored_image_absolute_path))
else:
    print("duplicates.txt does not exist. Please generate this file first by codes in 1.4.")
    

BUCKETS = {}   # Create an empty dictionary
all_images = glob.glob(INPUT_FOLDER + "/*/*")   # "/..." + "/*" + "/*"
for _img in all_images:   # for each image (e.g. 0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG)
    if _img not in ignored_image_absolute_path:
        image_name = _img.split("/")[-1]   # i.e. 0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG
        className = _img.split("/")[-2]    # i.e. Apple___Apple_scab, 38 class names in total.
        # Check if the image belongs to a particular known group
        image_identifier = image_name.split("___")[-1]   # i.e. RS_GLSp 4289.JPG or
                                                               # RS_GLSp 4289 copy 2.jpg or
                                                               # RS_GLSp 4289 copy.jpg or
                                                               # RS_HL 5749 1.JPG
        image_identifier = image_identifier.split(".")[0].strip()   # i.e. RS_GLSp 4289 or
                                                                    # RS_GLSp 4289 copy 2 or
                                                                    # RS_GLSp 4289 copy or
                                                                    # RS_HL 5749 1
        image_identifier = image_identifier.split("copy")[0].strip()   # i.e. RS_GLSp 4289 or RS_HL 5749 1

        group = determine_leaf_group(image_identifier, className)   # 'Apple___Apple_scab:::92.0' or
                                                                    # '2723070300716821278988'

        try:
            BUCKETS[group].append((_img, className))   # BUCKETS['Apple___Apple_scab:::92.0'] =
            # [('/.../raw/*/*/0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG', 'Apple___Apple_scab'),
            # ('/.../raw/*/*/4151028c-c8bc-4394-b4a7-aff414864c15___FREC_Scab 3418.JPG', 'Apple___Apple_scab')]
        except:
            BUCKETS[group] = [(_img, className)]

        
train_probs = [0.8]
for train_prob in train_probs:
    CANDIDATE_DISTRIBUTIONS = []   # Create an empty List
    CANDIDATE_VARIANCES = []       # Create an empty List
    for k in range(1000):
        train, test = distribute_buckets(BUCKETS, train_prob)   # Images belonging to the same leaf_group will
                                                                    # either be train set or test set.
        train_dist = compute_per_class_distribution(train)  # For each data_type (38 data types in total),
                                                                # calculate the number of images in train set.
        test_dist = compute_per_class_distribution(test)    # For each data_type (38 data types in total),
                                                                # calculate the number of images in test set.
        spread_data = []   # Create an empty List
        for _key in train_dist:   # e.g. 'Apple___Apple_scab'
          #  print(_key + ", " + str(train_dist[_key] * 1.0 /(train_dist[_key]+test_dist[_key])))
            if _key in test_dist.keys():
                spread_data.append(train_dist[_key] * 1.0 / (train_dist[_key] + test_dist[_key]))   # For each data_
                # type (38 data types in total), calculate the proportion of images in train set.
            else:
                spread_data.append(1.0)           

        CANDIDATE_DISTRIBUTIONS.append((train, test))   # Record train set and test set of 1000 simulations (k).
        CANDIDATE_VARIANCES.append(np.var(spread_data))   # Record the variance of the proportion of images from
                                                              # 38 data types in train set of 1000 simulations (k).

    train, test = CANDIDATE_DISTRIBUTIONS[np.argmax(CANDIDATE_VARIANCES)]   # Pick out the train and test set with
                                                                                # the maximum variance of the proportion
                                                                                # of images from 38 data types in train
                                                                                # set of 1000 simulations (k).
    print("train/test = ", str((len(train)+0.0)/(len(train)+len(test))))
    print("The number of images in train set:", str(len(train)))
    print("The number of images in test set:", str(len(test)))

    train_dist = compute_per_class_distribution(train)   # For each data_type (38 data types in total),
                                                             # calculate the number of images in train set.
    test_dist = compute_per_class_distribution(test)     # For each data_type (31 data types in total),
                                                             # calculate the number of images in test set.
    spread_data = []   # Create an empty List
    print("The proportion of each class in train set:")
    for _key in train_dist:   # e.g. 'Apple___Apple_scab'
        train_proportion = train_dist[_key] * 1.0 / (train_dist[_key] + test_dist[_key])
        spread_data.append(train_proportion)   # For each data_
                # type (38 data types in total), calculate the proportion of images in train set.
        print(_key + ":" + "%.2f" %train_proportion + ', ',end='')
    print("\n")
     
    target_folder_name = str(int(math.ceil(train_prob * 100))) + "-" + str(int(math.ceil((1 - train_prob) * 100)))   
    # i.e. 20 (or 40 or 50 or 60 or 80)-80 (or 60 or 50 or 40 or 20)

    try:
        if os.path.exists(OUTPUT_FOLDER + "/" + target_folder_name):
            if os.path.isdir(OUTPUT_FOLDER + "/" + target_folder_name):
                shutil.rmtree(OUTPUT_FOLDER + "/" + target_folder_name, ignore_errors=True)
            else:
                os.remove(OUTPUT_FOLDER + "/" + target_folder_name)

        os.mkdir(OUTPUT_FOLDER + "/" + target_folder_name)   # i.e. "/.../lmdb" + "/" + "color (or grayscale or
                                                                 # segmented)-20 (or 40 or 50 or 60 or 80)-80 (or
                                                                 # 60 or 50 or 40 or 20)"
    except:
        pass

    labels_map = {}   # Create an empty dictionary
    for _entry in train:
            # [('/.../raw/*/*/0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG', 'Apple___Apple_scab')]
        try:
            labels_map[_entry[1]] += 1
        except:
            labels_map[_entry[1]] = 1
                           # e.g. labels_map['Apple___Apple_scab'] = the number of train images belonging to
                           # Apple___Apple_scab
    labels_list = sorted(labels_map.keys())

    f = open(OUTPUT_FOLDER + "/" + target_folder_name + "/train_dependence_unbalance.txt", "w")   # i.e. "/..." + "/" + "color (or
                                                                                 # grayscale or segmented)-20 (or 40 or
                                                                                 # 50 or 60 or 80)-80 (or 60 or 50 or
                                                                                 # 40 or 20)" + "/train.txt"
    train_txt = ""
    for _entry in train:
            # [('/.../raw/*/*/0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG', 'Apple___Apple_scab')]
        train_txt += os.path.abspath(_entry[0]) + "\t" + str(labels_list.index(_entry[1])) + "\n"
            # i.e. /.../raw/*/Apple___Apple_scab/0a5e9323-dbad-432d-ac58-d291718345d9___FREC_Scab 3417.JPG 0
    f.write(train_txt)
    f.close()
    print("The train_dependence_unbalance.txt file is under " + OUTPUT_FOLDER + "/" + target_folder_name)

    f = open(OUTPUT_FOLDER + "/" + target_folder_name + "/test_dependence_unbalance.txt", "w")   # i.e. "/..." + "/" + "color (or
                                                                                # grayscale or segmented)-20 (or 40 or
                                                                                # 50 or 60 or 80)-80 (or 60 or 50 or
                                                                                # 40 or 20)" + "/test.txt"
    test_txt = ""
    for _entry in test:
        test_txt += os.path.abspath(_entry[0]) + "\t" + str(labels_list.index(_entry[1])) + "\n"
    f.write(test_txt)
    f.close()
    print("The test_dependence_unbalance.txt file is under " + OUTPUT_FOLDER + "/" + target_folder_name)

    f = open(OUTPUT_FOLDER + "/" + target_folder_name + "/class.txt", "w")   # i.e. "/..." + "/" + "color (or
                                                                                  # grayscale or segmented)-20 (or 40 or
                                                                                  # 50 or 60 or 80)-80 (or 60 or 50 or
                                                                                  # 40 or 20)" + "/labels.txt"
    f.write("\n".join(labels_list))
    f.write("\n")
    f.close()
    # break