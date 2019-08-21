#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/08/16 12:04
import os
import cv2
import time
import tensorflow as tf
from main_lite_interpreter import find_3_points


def validate_pb_model_video(model_path, input_size=(28, 28), video_source='./Img/'):
    """Validate model performance"""
    # Read the graph.
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    capture = cv2.VideoCapture(video_source)
    with tf.Session() as sess:
        sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

        res, frame = capture.read()
        cnt = 0
        while res:
            img = frame
            inp = cv2.resize(img, input_size, interpolation=cv2.INTER_LINEAR)  # [Key Step]: Change data for train
            img_new = cv2.resize(img, (320, 180), interpolation=cv2.INTER_LINEAR)

            start_time = time.time()
            # out = sess.run([sess.graph.get_tensor_by_name('claasf1_1/dense_1/BiasAdd:0'), ],
            #                feed_dict={'Reshape:0': imgP.reshape(1, imgP.shape[0], imgP.shape[1], 3)})
            # out = sess.run([sess.graph.get_tensor_by_name('dense_1_2/BiasAdd:0'), ],
            #                feed_dict={'input_1_2:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
            out = sess.run([sess.graph.get_tensor_by_name('dense_1/BiasAdd:0'), ],
                           feed_dict={'input_1:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})
            elapsed_time = time.time() - start_time
            print('time: ' + str(elapsed_time) + 'sec')

            predctedArray = out[0][0].astype(int)
            key_points_set = find_3_points(predctedArray[0])

            cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                     (int(key_points_set[2]), int(key_points_set[3])), (255, 0, 0), 2)
            cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                     (int(key_points_set[4]), int(key_points_set[5])), (255, 255, 0), 2)

            cv2.imshow('ShowTag', img_new)
            # cv2.waitKey(1)
            res, frame = capture.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print('This is main_lite_interpreter test....')
    model_lite_path = "./Model/tf_model.pb"
    video_source = "F:\\DataSet_0\\test_videos\\20190723_001.avi"
    validate_pb_model_video(model_lite_path, input_size=(300, 300), video_source=video_source)
    print('It is Ok!')
