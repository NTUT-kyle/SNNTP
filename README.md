# SNNTP
Simple Neural Network Training Platform

Figma: https://www.figma.com/file/oHCtfONsjfdgkAsljYOnYL/SNNTP?node-id=0%3A1&t=IjL9565CJUpxedQd-1

NN Framwork : Keras(Based on tanserflow)

CNN model design:
  1. Convolution layers:
     - Conv2D layer
     - SeparableConv2D layer
     - Conv2DTranspose layer

  2. Activation layers:
     - ReLU layer
     - Softmax layer
     - LeakyReLU layer
     - PReLU layer
     - ELU layer
     - ThresholdedReLU layer
     
  3. Normalization layers:
     - BatchNormalization layer
     - LayerNormalization layer
     - UnitNormalization layer
     - GroupNormalization layer
 
  4. Pooling layers:
     - MaxPooling
     - AveragePooling
     - GlobalMaxPooling
     - GlobalAveragePooling
  
  5. Core layers:
     - Dense layer

  6. Reshaping layers:
     - Flatten layer
     - Cropping2D layer(Optional)
     - UpSampling2D layer(Optional)
     - ZeroPadding2D layer(Optional)

資料集:
  1. MNIST
  2. CIFAR10

模型儲存 format: h5, tf
