1  The goal of this project

This project is trying to record every detail in the process of building and deploying a sucessful deep learning model by popular deep learning libraries(keras, fastai). All of the analysis are based on PlantVillage dataset (https://github.com/salathegroup/plantvillage_deeplearning_paper_dataset).

2  The structure of this project

The whole project can be divided into four parts:
data preprocessing -- filter out duplicated images, showing some statstics of the dataset, split the dataset into training set, validation set and testing set (for keras and fastai libraties, just keep .csv files with the image relative path and label is OK; for caffe, need to build a LMDB database to store image matrice) 
disease model training -- by transfer learning from pre-trained models on ImageNet dataset
model visulization -- take Grad-CAM to show the most activated parts of the orginal image in order to tell which part lets the model make the final decisions
model deployment -- take Apache2.4, flask, mod_wsgi and redis to deploy the plant disease model (https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/)

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
