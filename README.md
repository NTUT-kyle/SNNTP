# SNNTP
Simple Neural Network Training Platform

Figma: https://www.figma.com/file/oHCtfONsjfdgkAsljYOnYL/SNNTP?node-id=0%3A1&t=IjL9565CJUpxedQd-1

NN Framwork : Keras(Based on tanserflow)

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
