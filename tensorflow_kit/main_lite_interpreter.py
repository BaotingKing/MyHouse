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
    input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)  # random input...
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
            res_img = cv2.resize(img, input_size, interpolation=cv2.INTER_LINEAR)  # [Key Step]: Change data for train
            # matrix_img = res_img.reshape((input_size[0] * input_size[1]))
            # print(len(img), len(res_img), len(matrix_img))
            # image_np_expanded = np.expand_dims(matrix_img, axis=0)    # change dimension [N, 1] --> [1, N]

            if res_img.shape != tuple(input_details[0]['shape'][1:]):
                print('[Debug]: Input data.shape has problem!', res_img.shape, input_details[0]['shape'])
                continue
            res_img_float = [res_img.astype('float32')]  # must be change type
            model_interpreter_start_time = time.time()
            interpreter.set_tensor(input_details[0]['index'], res_img_float)  # [Key Step]: add data

            interpreter.invoke()  # [Key Step]: Call model
            output_data = interpreter.get_tensor(output_details[0]['index'])
            print('result:{}'.format(output_data))
            model_interpreter_time += time.time() - model_interpreter_start_time
    used_time = time.time() - start_time
    print('used_time:{0}'.format(used_time))


def validate_lite_model_video(lite_path, input_size=(28, 28), video_source='./Img/'):
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

    capture = cv2.VideoCapture(video_source)
    res, frame = capture.read()
    cnt = 0
    while res:
        img = frame
        res_img = cv2.resize(img, input_size, interpolation=cv2.INTER_LINEAR)  # [Key Step]: Change data for train
        img_new = cv2.resize(img, (320, 180), interpolation=cv2.INTER_LINEAR)
        if res_img.shape != tuple(input_details[0]['shape'][1:]):
            print('[Debug]: Input data.shape has problem!', res_img.shape, input_details[0]['shape'])
            continue
        res_img_float = [res_img.astype('float32')]  # must be change type
        model_interpreter_start_time = time.time()
        interpreter.set_tensor(input_details[0]['index'], res_img_float)  # [Key Step]: add data

        interpreter.invoke()  # [Key Step]: Call model
        output_data = interpreter.get_tensor(output_details[0]['index'])
        print('result{0}:{1}'.format(cnt, output_data[0]))
        cnt += 1
        model_interpreter_time += time.time() - model_interpreter_start_time
        output_data = output_data[0]
        key_points_set = [output_data[0], output_data[1], 0, 0, 0, 0]
        if 0 < output_data[2] < 180:
            key_points_set[2] = 0
            key_points_set[3] = output_data[2]
        elif 180 <= output_data[2] <= 179 + 319:
            key_points_set[2] = output_data[2] - 179
            key_points_set[3] = 179
        elif 179 + 319 < output_data[2] <= 179 + 319 + 179:
            key_points_set[2] = output_data[2] - 179 - 319
            key_points_set[3] = 319

        if 0 < output_data[3] < 180:
            key_points_set[4] = 0
            key_points_set[5] = output_data[3]
        elif 180 <= output_data[3] <= 179 + 319:
            key_points_set[4] = output_data[3] - 179
            key_points_set[5] = 179
        elif 179 + 319 < output_data[3] <= 179 + 319 + 179:
            key_points_set[4] = output_data[3] - 179 - 319
            key_points_set[5] = 319

        cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                 (int(key_points_set[2]), int(key_points_set[3])), (255, 0, 0), 2)
        cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                 (int(key_points_set[4]), int(key_points_set[5])), (255, 255, 0), 2)

        cv2.imshow('ShowTag', img_new)
        # cv2.waitKey(1)
        res, frame = capture.read()
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.waitKey(0)
    used_time = time.time() - start_time
    print('used_time:{0}'.format(used_time))


def Lane_lite_model(lite_path, input_size=(28, 28), image_path='./Img/'):
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
        file = "00210.jpg"
        if file[-3:] == 'jpg' or file[-3:] == 'png':
            img_path = os.path.join(image_path, file)
            img = cv2.imread(img_path)

            res_img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_LINEAR)  # [Key Step]: Change data for train
            img_new = cv2.resize(img, (320, 180), interpolation=cv2.INTER_LINEAR)

            if res_img.shape != tuple(input_details[0]['shape'][1:]):
                print('[Debug]: Input data.shape has problem!', res_img.shape, input_details[0]['shape'])
                continue
            res_img_float = [res_img.astype('float32')]  # must be change type

            # f = open("axis_python.txt", 'w+')
            # for i in range(300):
            #     for j in range(300):
            #         for p in range(3):
            #             cnt = i*900 + j*3 + p
            #             print('{0}      {1}'.format(cnt, res_img_float[0][i][j][p]), file=f)

            model_interpreter_start_time = time.time()
            interpreter.set_tensor(input_details[0]['index'], res_img_float)  # [Key Step]: add data

            interpreter.invoke()  # [Key Step]: Call model
            output_data = interpreter.get_tensor(output_details[0]['index'])
            print('result:{}'.format(output_data))
            model_interpreter_time += time.time() - model_interpreter_start_time
            output_data = output_data[0]
            key_points_set = [output_data[0], output_data[1], 0, 0, 0, 0]
            if 0 < output_data[2] < 180:
                key_points_set[2] = 0
                key_points_set[3] = output_data[2]
            elif 180 <= output_data[2] <= 179 + 319:
                key_points_set[2] = output_data[2] - 179
                key_points_set[3] = 179
            elif 179 + 319 < output_data[2] <= 179 + 319 + 179:
                key_points_set[2] = 319
                key_points_set[3] = 179 * 2 - output_data[2] + 319

            if 0 < output_data[3] < 180:
                key_points_set[4] = 0
                key_points_set[5] = output_data[3]
            elif 180 <= output_data[3] <= 179 + 319:
                key_points_set[4] = output_data[3] - 179
                key_points_set[5] = 179
            elif 179 + 319 < output_data[3] <= 179 + 319 + 179:
                key_points_set[4] = 319
                key_points_set[5] = 179 * 2 - output_data[2] + 319

            cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                     (int(key_points_set[2]), int(key_points_set[3])), (255, 0, 0), 2)
            cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                     (int(key_points_set[4]), int(key_points_set[5])), (255, 255, 0), 2)

            cv2.imshow('ShowTag', img_new)
            cv2.waitKey(0)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                cv2.waitKey(0)

    used_time = time.time() - start_time
    print('used_time:{0}'.format(used_time))


if __name__ == '__main__':
    print('This is main_lite_interpreter test....')
    model_lite_path = "./save/temp_converted_model.tflite"
    model_lite_path = "./Model/LwdsModel.tflite"
    video_source = "F:\\DataSet_0\\test_videos\\20190723_001.avi"
    # validate_lite_model(model_lite_path, input_size=(300, 300))
    Lane_lite_model(model_lite_path, input_size=(300, 300))
    # validate_lite_model_video(model_lite_path, input_size=(300, 300), video_source=video_source)
    print('It is Ok!')
