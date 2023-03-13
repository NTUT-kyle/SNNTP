# SNNTP
Simple Neural Network Training Platform

Figma: https://www.figma.com/file/oHCtfONsjfdgkAsljYOnYL/SNNTP?node-id=0%3A1&t=IjL9565CJUpxedQd-1

NN Framwork : Keras(Based on tanserflow)     

Python version : python 3.9.13      
Keras version : 2.11.0     
Flask : 

## Install
### Require Environment:    
1. Python 3.9
   * You can install from [here](https://www.python.org/downloads/release/python-3913/)
   * Enter `python` in the console to check the version
2. pipenv
   * When the first one is done, Enter `pip install pipenv` in the console.
   * Enter `pipenv --version` in the console to check the version

### Install:
1. Complete all required environments
2. Enter `python -m pipenv shell` in the console to enter the virtual environment
3. If you want to confirm your current environment, do the first step again, it will show `No module named pipenv`
4. Enter `pipenv install` in the console to download & install the packages
5. If no errors show up, you're all done!

### Other way:
1. Complete all required environments
2. Enter `.\StartSciprt` in the console 
3. Input `1` then input `2`
4. If no errors show up, you're all done!

## Run server
* Enter `flask run` in the console to start the program
* Or you can Enter `.\StartScript.bat` in the console then input `3` to start program

---

## CNN model design:
### Sequential model
  
## CNN layers design:
### 1. Convolution layers:
#### &nbsp;&nbsp;&nbsp;◆ Conv2D layer

| Parameter | Formate | Example |
|-----|-----|-----|
| filters   | Integer  | 32 |
| kernel_size   | An integer or tuple/list of 2 integers | 3 or (3, 3) |
| strides   | An integer or tuple/list of 2 integers  | 3 or (3, 3) |
| padding |"valid"or"same" |"valid" |

#### &nbsp;&nbsp;&nbsp;◆ SeparableConv2D layer
#### &nbsp;&nbsp;&nbsp;◆ Conv2DTranspose layer
### 2. Activation layers:
#### &nbsp;&nbsp;&nbsp;◆ ReLU layer
#### &nbsp;&nbsp;&nbsp;◆ Softmax layer
#### &nbsp;&nbsp;&nbsp;◆ LeakyReLU layer
#### &nbsp;&nbsp;&nbsp;◆ PReLU layer
#### &nbsp;&nbsp;&nbsp;◆ ELU layer
#### &nbsp;&nbsp;&nbsp;◆ ThresholdedReLU layer
     
### 3. Normalization layers:
#### &nbsp;&nbsp;&nbsp;◆ BatchNormalization layer
#### &nbsp;&nbsp;&nbsp;◆ LayerNormalization layer
#### &nbsp;&nbsp;&nbsp;◆ UnitNormalization layer
#### &nbsp;&nbsp;&nbsp;◆ GroupNormalization layer
 
### 4. Pooling layers:
#### &nbsp;&nbsp;&nbsp;◆ MaxPooling
#### &nbsp;&nbsp;&nbsp;◆ AveragePooling
#### &nbsp;&nbsp;&nbsp;◆ GlobalMaxPooling
#### &nbsp;&nbsp;&nbsp;◆ GlobalAveragePooling
  
### 5. Core layers:
#### &nbsp;&nbsp;&nbsp;◆ Dense layer
#### &nbsp;&nbsp;&nbsp;◆ Dropout layer

### 6. Reshaping layers:
#### &nbsp;&nbsp;&nbsp;◆ Flatten layer
#### &nbsp;&nbsp;&nbsp;◆ Cropping2D layer(Optional)
#### &nbsp;&nbsp;&nbsp;◆ UpSampling2D layer(Optional)
#### &nbsp;&nbsp;&nbsp;◆ ZeroPadding2D layer(Optional)

資料集:
  1. MNIST
  2. CIFAR10

模型儲存 format: h5, tf
