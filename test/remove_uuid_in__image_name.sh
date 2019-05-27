#!/usr/bin/env bash

parent_path="/home/gxty/pycharmProjects/plant_disease_detection_project/test/example_2"
cd ${parent_path}

SAVEIFS=${IFS}
IFS=$(echo -en "\n\b")

for folder in `ls -F | grep "/$"`
do
    for file in `ls ${folder}`
    do 
        new_fileName=`echo ${file:39}`
        mv ${folder}$file ${folder}$new_fileName
    done
done

IFS=SAVEIFS

