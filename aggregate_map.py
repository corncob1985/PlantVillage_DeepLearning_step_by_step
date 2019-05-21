#!/usr/local/anaconda3/bin/python


import os
import glob
import csv


cwd = os.getcwd()
MAP = {}
for _csvfile in glob.glob(cwd + "/" + "raw_datasets/csvs/plantVillage_map/*.csv"):
	csvfile = open(_csvfile, "r")
	reader = csv.DictReader(csvfile)
	_key = _csvfile.split("/")[-1].split(".")[0]
	for row in reader:
		_filename = ".".join(row['File Name'].split(".")[:-1])
		_leaf_id = row['Leaf #']

		_leaf_id = _key+":::"+_leaf_id

		_filename = _filename.lower().strip()

		try:
			MAP[_filename].append(_leaf_id)
		except:
			MAP[_filename] = [_leaf_id]


#for _key in MAP.keys():
#	if len(MAP[_key])==1:
#		print(_key, " ------ ", MAP[_key])


import json

f=open(cwd + "/" + "processed_datasets/plantVillage/leaf-map.json", "w")
f.write(json.dumps(MAP))
f.close()
