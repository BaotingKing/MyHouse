#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/08/03 12:19
"""
    Derived from the official website:
    https://tensorflow.google.cn/lite/convert/python_api
"""
import os
import time
import cv2
import numpy as np
import tensorflow as tf


def lite_interpreter_demo(lite_path):
    """Demo for interpreter"""
    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=lite_path)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    print('[Info]: Input information: ', str(input_details))
    output_details = interpreter.get_output_details()
    print('[Info]: Output information: ', str(output_details))

    # Test model on random input data.
    input_shape = input_details[0]['shape']
    input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)     # random input...
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print('[Info]: Output result is: ', output_data)


def validate_lite_model(lite_path, input_size=(28, 28), image_path='./Img/'):
    """Validate model performance"""
    model_path = lite_path
    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    print('[Info]: Input information: ', str(input_details))
    output_details = interpreter.get_output_details()
    print('[Info]: Output information: ', str(output_details))

    model_interpreter_time = 0
    start_time = time.time()
    for file in os.listdir(image_path):
        if file[-3:] == 'jpg' or file[-3:] == 'png':
            img_path = os.path.join(image_path, file)
            # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            # res_img = cv2.resize(img, input_size, interpolation=cv2.INTER_CUBIC)   # [Key Step]: Change data for train
            # matrix_img = res_img.reshape((input_size[0] * input_size[1]))
            # print(len(img), len(res_img), len(matrix_img))
            # image_np_expanded = np.expand_dims(matrix_img, axis=0)    # change dimension [N, 1] --> [1, N]

            if img.shape != tuple(input_details[0]['shape'][1:]):
                print('[Debug]: Input data.shape has problem!', img.shape, input_details[0]['shape'])
                continue
            img = [img.astype('float32')]  # must be change type
            model_interpreter_start_time = time.time()
            interpreter.set_tensor(input_details[0]['index'], img)    # [Key Step]: add data

            interpreter.invoke()     # [Key Step]: Call model
            output_data = interpreter.get_tensor(output_details[0]['index'])
            print('result:{}'.format(output_data))
            model_interpreter_time += time.time() - model_interpreter_start_time
    used_time = time.time() - start_time
    print('used_time:{0}'.format(used_time))


if __name__ == '__main__':
    print('This is main_lite_interpreter test....')
    model_lite_path = "./save/converted_model.tflite"
    validate_lite_model(model_lite_path, input_size=(590, 1640))
    print('It is Ok!')
