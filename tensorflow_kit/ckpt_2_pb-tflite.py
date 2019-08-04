#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/08/02 12:00
"""
    Derived from the official website:
    https://tensorflow.google.cn/lite/convert/python_api
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.python.tools.freeze_graph import freeze_graph
from tensorflow.python.framework import graph_util
from tensorflow.python.platform import gfile


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


def convert_ckpt_to_tflite(input_checkpoint, input_node_names, output_node_names, output_graph):
    """
    :param input_checkpoint: ckpt files path
    :param input_node_names:
    :param output_node_names:
    :param output_graph:    output path
    :return:
    """
    # ckpt = tf.train.get_checkpoint_state(input_checkpoint)
    # input_checkpoint = ckpt.model_checkpoint_path
    # if not (ckpt and input_checkpoint):
    #     return False
    tf.reset_default_graph()
    saver = tf.train.import_meta_graph(input_checkpoint + '.meta', clear_devices=True)
    # graph = tf.get_default_graph  # Get the default diagram
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
            saver.restore(sess, input_checkpoint)  # Restore the graph and get the data
            temp_pb = 'temp_model.pb'
            temp_frozen_pb = './save/pb/temp_model.pb'
            tf.train.write_graph(sess.graph_def, './save/pb', temp_pb)
            freeze_graph(input_graph='./save/pb/temp_model.pb',
                         input_saver='',
                         input_binary=False,
                         input_checkpoint=input_checkpoint,
                         output_node_names=output_node_names[0],
                         restore_op_name='save/restore_all',
                         filename_tensor_name='save/Const:0',
                         output_graph=output_graph,
                         clear_devices=False,
                         initializer_nodes='')
            print('*******************', output_graph)
        converter = tf.lite.TFLiteConverter.from_frozen_graph(output_graph, input_node_names, output_node_names)
        tflite_model = converter.convert()
        with open("./save/temp_model.tflite", "wb") as f:
            f.write(tflite_model)
            print("[Info]: Covert ckpt file to tflite is Ok!")


def convert_frozenPB_to_tflite(graph_def_file, input_node_name, output_node_name, output_path):
    """
    :param graph_def_file:   Full filepath of file containing frozen GraphDef.
    :param input_node_name:  List of input tensors Name to freeze graph with.
    :param output_node_name: List of output tensors Name to freeze graph with.
    :param output_path:  tflite saved path and file name
    :return:
    """
    converter = tf.lite.TFLiteConverter.from_frozen_graph(graph_def_file, input_node_name, output_node_name)
    tflite_model = converter.convert()
    with open(output_path, "wb") as f:
        f.write(tflite_model)
        print("[Info]: Covert Frozen pb file to tflite is Ok!")


def convert_h5_to_tflite(keras_file):
    # Convert to TensorFlow Lite model.
    print('[Note]: This {0} must be model ,not be weight!'.format(keras_file))
    if os.path.isfile(keras_file):
        print('[Info]: Keras file path: ', keras_file)
        converter = tf.lite.TFLiteConverter.from_keras_model_file(keras_file)
        tflite_model = converter.convert()
        with open("converted_model.tflite", "wb") as f:
            f.write(tflite_model)
            print("Convert h5 to tflite is ok!")
    else:
        print('[Warning]: keras model file does not exist! ')


def fun_test(ckpt_file=None):
    pass
    # converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir='./save/ckpt')
    # tflite_model = converter.convert()
    # with open("./save/new_model.tflite", "wb") as f:
    #     f.write(tflite_model)
    #     print("[Info]: Test is Ok!")


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
    input_node = ["img"]
    output_node = ["out"]
    input_checkpoint = './save/ckpt/model.ckpt'
    out_pb_path = "./save/pb/new_frozen_model.pb"
    out_tflite_path = "./save/model.tflite"
    keras_model = "F:\\projects\\Mask_RCNN_IS\\logs\\shapes20190730T1406\\mask_rcnn_shapes_0003.h5"
    # convert_ckpt_to_tflite(input_checkpoint, input_node, output_node, "./save/pb/new_temp_frozen_model.pb")
    # convert_frozenPB_to_tflite(out_pb_path, input_node, output_node, out_tflite_path)
    # fun_test()
    # official_demo()
    # convert_h5_to_tflite(keras_model)
    # convert_frozenPB_to_tflite(out_pb_path, out_tflite_path)

    print('--------: ending.....')


