#!/bin/bash

if [ $# != 1 ] ; then
    echo "USAGE: ./ upload_image_by_curl.sh image_name or folder_name(including image files)"
    exit 1;
fi

if [[ -f $1 ]]; then
    echo "$1 file exists."
    curl -X POST -F image=@"$1" "http://localhost:8080/predict"    
else
    if [[ -d $1 ]]; then
    folderName=${1%/}
    echo "${folderName} folder exists."
#    SAVEIFS=${IFS}
#    IFS=$(echo -en "\n\b")
    for file in `ls ${folderName}`
    do
        echo ${folderName}/${file}
        curl -X POST -F image=@"${folderName}/${file}" "http://localhost:8080/predict"
    done
#    IFS=SAVEIFS
    fi    
fi 

