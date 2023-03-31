# SNNTP
Simple Neural Network Training Platform

Figma: https://www.figma.com/file/oHCtfONsjfdgkAsljYOnYL/SNNTP?node-id=0%3A1&t=IjL9565CJUpxedQd-1

NN Framwork : Keras(Based on tanserflow)     

Python version : python 3.9.13      
Keras version : 2.11.0     
Flask : 2.2.3

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
## CNN model setting:
### 1. Probabilistic losses:

| Parameter | Formate | Example |
|-----|-----|-----|
| loss_type | String | "binary_crossentropy", "categorical_crossentropy", "sparse_categorical_crossentropy", "poisson" |

### 2. Optimizers:

| Parameter | Formate | Example |
|-----|-----|-----|
| optimizers_type | String | "SGD", "RMSprop", "Adam", "AdamW", "Adadelta", "Adagrad", "Adamax", "Adafactor", "Nadam", "Ftrl" |

## CNN model design:
### Sequential model
  
## CNN layers design:
### 1. Convolution layers:
#### &nbsp;&nbsp;&nbsp;◇ Conv2D layer

| Parameter | Formate | Example |
|-----|-----|-----|
| filters   | Integer  | 32 |
| kernel_size   | An integer or tuple/list of 2 integers | 3 or (3, 3) |
| strides   | An integer or tuple/list of 2 integers  | 3 or (3, 3) |
| padding |"valid"or"same" |"valid" |

#### &nbsp;&nbsp;&nbsp;◆ SeparableConv2D layer
#### &nbsp;&nbsp;&nbsp;◆ Conv2DTranspose layer
### ◇2. Activation layers:
| Parameter | Formate | Example |
|-----|-----|-----|
| active_type   | String | "softmax", "elu", "selu", "softplus", "softsign", "relu", "tanh", "sigmoid", "hard_sigmoid", "exponential", "linear", "elu", "PReLU ", "LeakyReLU" |
     
### 3. Normalization layers:
#### &nbsp;&nbsp;&nbsp;◆ BatchNormalization layer
#### &nbsp;&nbsp;&nbsp;◆ LayerNormalization layer
#### &nbsp;&nbsp;&nbsp;◆ UnitNormalization layer
#### &nbsp;&nbsp;&nbsp;◆ GroupNormalization layer
 
### 4. Pooling layers:
#### &nbsp;&nbsp;&nbsp;◇ MaxPooling

| Parameter | Formate | Example |
|-----|-----|-----|
| pool_size   | An integer or tuple/list of 2 integers | 3 or (3, 3) |
| strides   | An integer or tuple/list of 2 integers  | 3 or (3, 3) |
| padding |"valid"or"same" |"valid" |
#### &nbsp;&nbsp;&nbsp;◇ AveragePooling

| Parameter | Formate | Example |
|-----|-----|-----|
| pool_size   | An integer or tuple/list of 2 integers | 3 or (3, 3) |
| strides   | An integer or tuple/list of 2 integers  | 3 or (3, 3) |
| padding |"valid"or"same" |"valid" |
#### &nbsp;&nbsp;&nbsp;◆ GlobalMaxPooling
#### &nbsp;&nbsp;&nbsp;◆ GlobalAveragePooling
  
### 5. Core layers:
#### &nbsp;&nbsp;&nbsp;◇ Dense layer

| Parameter | Formate | Example |
|-----|-----|-----|
| units(不開放)   | An integer | 3 |
| use_bias   | Bool  | True |
### 6. Reshaping layers:
#### &nbsp;&nbsp;&nbsp;◇ Flatten layer
#### &nbsp;&nbsp;&nbsp;◆ Cropping2D layer(Optional)
#### &nbsp;&nbsp;&nbsp;◆ UpSampling2D layer(Optional)
#### &nbsp;&nbsp;&nbsp;◆ ZeroPadding2D layer(Optional)

### 7. Regularization  layers:
#### &nbsp;&nbsp;&nbsp;◇ Dropout layer

| Parameter | Formate | Example |
|-----|-----|-----|
| rate   | An double between 0~1 | 0.66 |
| seed   | An integer | 3 |

## CNN model.json example:
```yaml
{
  "product": "Live JSON generator",
  "version": 3.1,
  "releaseDate": "2014-06-25T00:00:00.000Z",
  "demo": true,
  "person": {
    "id": 12345,
    "name": "John Doe",
    "phones": {
      "home": "800-123-4567",
      "mobile": "877-123-1234"
    },
    "email": [
      "jd@example.com",
      "jd@example.org"
    ],
    "dateOfBirth": "1980-01-02T00:00:00.000Z",
    "registered": true,
    "emergencyContacts": [
      {
        "name": "Jane Doe",
        "phone": "888-555-1212",
        "relationship": "spouse"
      },
      {
        "name": "Justin Doe",
        "phone": "877-123-1212",
        "relationship": "parent"
      }
    ]
  }
}
```
## 資料集:
  1. MNIST
  2. CIFAR10

模型儲存 format: h5, tf
