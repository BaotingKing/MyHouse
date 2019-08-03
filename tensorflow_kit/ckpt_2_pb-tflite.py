#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/08/02 12:00
"""
    Derived from the official website:
    https://tensorflow.google.cn/lite/convert/python_api
"""
import tensorflow as tf
from tensorflow.python.tools.freeze_graph import freeze_graph
from tensorflow.python.framework import graph_util
from tensorflow.lite import toco


def saver_ckpt(session, flag=True, model_path='./log'):
    saver = tf.train.Saver()
    if flag:
        ckpt = tf.train.get_checkpoint_state(model_path)
    else:
        ckpt = tf.train.latest_checkpoint('ckpt/')

    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(session, ckpt.model_checkpoint_path)
        return True
    else:
        return False


def convert_ckpt_to_tflite(model_path, output_graph):
    """
    :param input_checkpoint: ckpt files path
    :param output_graph:    output path
    :return:
    """
    # ckpt = tf.train.get_checkpoint_state(model_path)
    # input_checkpoint = ckpt.model_checkpoint_path
    # if not (ckpt and input_checkpoint):
    #     return False
    tf.reset_default_graph()
    input_checkpoint = model_path
    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=True)
    graph = tf.get_default_graph  # Get the default diagram
    output_node_names = 'v2'      # [Note]: *********
    method = 1
    if method == 0:
        with tf.Session() as sess:
            saver.restore(sess, input_checkpoint)    # Restore the graph and get the data
            output_graph_def = graph_util.convert_variables_to_constants(
                sess=sess,
                input_graph_def=sess.graph_def,
                output_node_names=output_node_names.split(',')
            )
            with tf.gfile.GFile("./save/pb/new_frozen_model.pb", "wb") as f:
                f.write(output_graph_def.SerializeToString())
            print("%d ops in the final graph." % len(output_graph_def.node))  # print current graph operation nodes
    elif method == 1:
        with tf.Session() as sess:
            tf.train.write_graph(sess.graph_def, './save', 'model.pb')
            # saver.restore(sess, input_checkpoint)  # Restore the graph and get the data
            freeze_graph(input_graph='./save/model.pb',
                         input_saver='',
                         input_binary=False,
                         input_checkpoint='./save/model.ckpt',
                         output_node_names='v2',
                         restore_op_name='save/restore_all',
                         filename_tensor_name='save/Const:0',
                         output_graph='./save/pb/new_frozen_model.pb',
                         clear_devices=False,
                         initializer_nodes='')

            # input = ["v1"]
            # input_tensor_shape = {"v1": [1, 2]}
            # output = ["v2"]
            # path = "./save/pb/new_frozen_model.pb"
            # converter = tf.lite.TocoConverter.from_frozen_graph(path, input, output, input_tensor_shape)
            # tflite_model = converter.convert()
            # with open("./save/pb/new_frozen_model.tflite", "wb") as f:
            #     f.write(tflite_model)
            print('-------------: I am Ok!')


def convert_ckpt_to_tflite_test(model_path, output_graph):
    converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
    pass


def convert_h5_to_tflite(keras_file):
    # Convert to TensorFlow Lite model.
    keras_file = "keras_model.h5"
    converter = tf.lite.TFLiteConverter.from_keras_model_file(keras_file)
    tflite_model = converter.convert()
    with open("converted_model.tflite", "wb") as f:
        f.write(tflite_model)
        print("Convert h5 to tflite is ok!")

def official_demo():
    img = tf.placeholder(name="img", dtype=tf.float32, shape=(1, 590, 1640, 3))
    var = tf.get_variable("weights", dtype=tf.float32, shape=(1, 590, 1640, 3))
    val = img + var
    out = tf.identity(val, name="out")
    init_op = tf.global_variables_initializer()
    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.save(sess, "./save/ckpt/model.ckpt")  # 将模型保存到save/model.ckpt文件
        # tf.train.write_graph(sess.graph_def, "save/", 'model.pb', as_text=False)
        tf.train.write_graph(sess.graph_def, "./save/pb/", 'model.pb')
        freeze_graph(input_graph='./save/pb/model.pb',
                     input_saver='',
                     input_binary=False,
                     input_checkpoint='./save/ckpt/model.ckpt',
                     output_node_names='out',
                     restore_op_name='save/restore_all',
                     filename_tensor_name='save/Const:0',
                     output_graph='./save/pb/new_frozen_model.pb',
                     clear_devices=True,
                     initializer_nodes='')
        converter = tf.lite.TFLiteConverter.from_session(sess, [img], [out])
        tflite_model = converter.convert()
        open("./save/converted_model.tflite", "wb").write(tflite_model)


if __name__ == '__main__':
    print('--------: It is begin.....', tf.__version__)
    input_checkpoint = 'save/ckpt/model.ckpt'
    out_pb_path = "save/pb/graph_model.pb"
    # convert_ckpt_to_tflite(input_checkpoint, out_pb_path)
    # official_demo()
    convert_h5_to_tflite("F:\\projects\\Mask_RCNN_IS\\logs\\shapes20190730T1406\\mask_rcnn_shapes_0003.h5")
    # input = ["enqueue_input/random_shuffle_queue"]
    # output = ["classf1_1/dense_1/BiasAdd"]
    # output = ["ConvNet/conv2d/bias/read"]
    # path = "./save/pb/new_frozen_model.pb"
    # path = "./Model/frozentensorflowModel.pb"
    # converter = tf.lite.TocoConverter.from_frozen_graph(path, input, output)
    # tflite_model = converter.convert()
    # with open("./save/pb/new_frozen_model.tflite", "wb") as f:
    #     f.write(tflite_model)

    print('--------: ending.....')


