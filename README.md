1  The goal of this project

This project is trying to record every detail in the process of building a sucessful deep learning model. All of the analysis are based on PlantVillage dataset (https://github.com/salathegroup/plantvillage_deeplearning_paper_dataset).

2  The structure of this project

The planned structure of project is showing below, right now I only finished the dataset_split.ipynb part, in which I try to get some insight of the PlantVillage dataset, and make the train/test set split with and without consideration of class imbalanced problem, which is ignored in the original publication (Mohanty SP, Hughes DP, Salathé M. Using deep learning for image-based plant disease detection. Front Plant Sci 2016; 7:1419.). Next, I will use classic Convolution Neural Network (CNN) architechture, such as AlexNet, VGG 16/19, Xception and ResNet50 to train the plant disease model. For learning rate is one of the most important hyperparameter in deep learning, and I will take advantage of the most advanced strategies to figure out the optimal value and optimal traing process, such as differential learning rates, cyclical learning rates, Cosine annealing, stochasitic gradient descent with warm restarts, and so on.

|--- PlantVillage_DeepLearning_step_by_step

|     |--- pdd_AlexNet.ipynb (coming soon ...)

|     |--- pdd_VGGNet16.ipynb (coming soon ...)

|     |--- pdd_VGGNet19.ipynb (coming soon ...)

|     |--- pdd_Xception.ipynb (coming soon ...)

|     |--- pdd_ResNet50.ipynb (coming soon ...)

|     |--- dataset_split.ipynb

|     |--- raw_datasets

|     |    |--- images

|     |    |    |--- plantVillage

|     |    |    |    |--- Apple___Apple_scab

|     |    |    |    |    |--- *.jpg

|     |    |    |    |--- Tomato___healthy

|     |    |--- csvs

|     |    |    |--- plantVillage_map

|     |    |    |    |--- Apple___Apple_scab.csv

|     |    |    |    |--- Tomato___healthy.csv

|     |--- processed_datasets

|     |    |--- plantVillage

|     |    |    |--- 80-20

|     |    |    |    |--- class.txt

|     |    |    |    |--- train_*.txt

|     |    |    |    |--- test_*.txt 

|     |    |    |--- leaf-map-1to1.json

|     |    |    |--- duplicates.txt

|     |    |    |--- *.pickle

3  The prerequisite of hardware and software

For image task, I sugggest to deploy a computer with at least one GPU of accelerated graphics memory >= 6G, 12G is much better. For software part, I highly recommend NVIDIA GPU driver + Anaconda + jupyter notebook + pycharm, in which Anaconda is the most important, you can easily use 'conda create' command to create correponding virtual environment with the popular deep learning frames, such as tensorflow, keras, pytorch, fast.ai libraries, and without any annoying operations among differnt versions of CUDA and cudnn and deep learning frames. I will use the following softwares in my project.

anaconda python==3.6

cudatoolkit==9.2

tensorflow-gpu==1.12.0

keras==2.2.4

pytorch

torchvision

fastai

opencv==3.4.2

4  Welcome to contact me

When you have any problem relating to this project, please send to wangyuting@telebody.cn
