import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as img
import math
import time
import argparse
import os.path
import batch_norm
import csv
import os



import resnet
import read_img
import dataaug







IMAGE_SIZE = read_img.IMAGE_SIZE
IMAGE_CHANNEL = 3
FEATURE_MAP_PER_STAGE = [32, 64, 128, 256, 512, 1024]
MODEL_DEPTH = 2 + 9 * 1
FLAGS = None
WEIGHT_DECAY = 0.0001
IMAGE_PATH=read_img.img_dir




def input_placeholders():
    image_pl = tf.placeholder(tf.float32, shape=[None, IMAGE_SIZE[0], IMAGE_SIZE[1], IMAGE_CHANNEL])
    label_pl = tf.placeholder(tf.int32, shape=[None])
    return image_pl, label_pl


def stage0(image_pl, is_training):
    with tf.name_scope('stage0'):
        w = tf.Variable(tf.random_normal([3, 3, IMAGE_CHANNEL, FEATURE_MAP_PER_STAGE[0]],
                                         stddev=math.sqrt(2 / (9 * IMAGE_CHANNEL))), dtype=tf.float32)
        b = tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[FEATURE_MAP_PER_STAGE[0]]), dtype=tf.float32)
        y0 = tf.nn.conv2d(image_pl, w, strides=[1, 1, 1, 1], padding='SAME') + b
        tf.add_to_collection('losses', tf.nn.l2_loss(w) * WEIGHT_DECAY)
    return y0


def stage1(y0, fm_in, fm_out, stride, count, is_training):
    with tf.name_scope('stage1'):
        y1 = resnet.res_blk_v2(y0, fm_in, fm_out, stride, count, is_training, 'BN_stage1', WEIGHT_DECAY)
    return y1


def stage2(y1, fm_in, fm_out, stride, count, is_training):
    with tf.name_scope('stage2'):
        y2 = resnet.res_blk_v2(y1, fm_in, fm_out, stride, count, is_training, 'BN_stage2', WEIGHT_DECAY)
    return y2


def stage3(y2, fm_in, fm_out, stride, count, is_training):
    with tf.name_scope('stage3'):
        y3 = resnet.res_blk_v2(y2, fm_in, fm_out, stride, count, is_training, 'BN_stage3', WEIGHT_DECAY)
    return y3


def stage4(y2, fm_in, fm_out, stride, count, is_training):
    with tf.name_scope('stage4'):
        y3 = resnet.res_blk_v2(y2, fm_in, fm_out, stride, count, is_training, 'BN_stage4', WEIGHT_DECAY)
    return y3


def stage5(y2, fm_in, fm_out, stride, count, is_training):
    with tf.name_scope('stage5'):
        y3 = resnet.res_blk_v2(y2, fm_in, fm_out, stride, count, is_training, 'BN_stage5', WEIGHT_DECAY)
    return y3


def final_stage(y3, is_training):
    with tf.name_scope('final'):
        z1=batch_norm.bn_layer_top(y3, 'BN_final', is_training)
        z2 = tf.nn.relu(z1)
        z3 = tf.nn.avg_pool(z2, ksize=[1, 7, 7, 1], strides=[1, 7, 7, 1], padding='VALID')
        w_out = tf.Variable(
            tf.random_normal([z3.shape.as_list()[-1], 120], stddev=math.sqrt(2 / z3.shape.as_list()[-1])),
            dtype=tf.float32)
        b_out = tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[120]), dtype=tf.float32)
        softmax_linear = tf.matmul(tf.reshape(z3, [-1, w_out.shape.as_list()[0]]), w_out) + b_out
        tf.add_to_collection('losses', tf.nn.l2_loss(w_out) * WEIGHT_DECAY)
    return softmax_linear




def mnist_resnet_model(image_pl, is_training):
    n=2
    y=stage0(image_pl, is_training)
    y=stage1(y, FEATURE_MAP_PER_STAGE[0], FEATURE_MAP_PER_STAGE[1], 2, n, is_training)
    y=stage2(y, FEATURE_MAP_PER_STAGE[1], FEATURE_MAP_PER_STAGE[2], 2, n, is_training)
    y=stage3(y, FEATURE_MAP_PER_STAGE[2], FEATURE_MAP_PER_STAGE[3], 2, n, is_training)
    y = stage4(y, FEATURE_MAP_PER_STAGE[3], FEATURE_MAP_PER_STAGE[4], 2, n, is_training)
    y = stage5(y, FEATURE_MAP_PER_STAGE[4], FEATURE_MAP_PER_STAGE[5], 2, n, is_training)
    prob=tf.cond(is_training, lambda : 0.5, lambda : 1.0)
    y=tf.nn.dropout(y, prob)
    final=final_stage(y, is_training)
    return final


def logits_to_softmax(logits):
    return tf.nn.softmax(logits)


def _loss(label_pl, logits):
    with tf.name_scope('total_loss'):
        ce_loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=label_pl)
        ce_mean = tf.reduce_mean(ce_loss)
        tf.add_to_collection('losses', ce_mean)
        total_loss = tf.add_n(tf.get_collection('losses'))
    return total_loss


def _predict_prob(image_pl, image, softmax, sess, is_training_pl):
    softmax_val=sess.run(softmax, feed_dict={image_pl: image, is_training_pl: False})
    return softmax_val


def _train(loss, lr_placeholder):
    train_op = tf.train.MomentumOptimizer(lr_placeholder, 0.9).minimize(loss)
    return train_op


def fill_feed_dict(image_pl, label_pl, is_train_pl, databatch, is_training, lr_pl, lr):
    dd = {image_pl: databatch[0], label_pl: np.int32(databatch[1]), is_train_pl: is_training, lr_pl: lr}
    return dd


def _correct_count(logits, labels):
    cnt = tf.nn.in_top_k(logits, labels, 1)
    count = tf.reduce_sum(tf.cast(cnt, tf.float32))
    return count


def predict(logits):
    pred = tf.argmax(logits, axis=1)
    return pred


def do_eval(sess, correct_count, image_pl, label_pl, is_train_pl, data, lr_pl, lr, image_path):
    num_batch = data._size // FLAGS.batch_size
    num_used = num_batch * FLAGS.batch_size
    cnt = 0
    for step in range(num_batch):
        data_batch, label_batch = read_img.image_batch_from_df(data.next_batch(FLAGS.batch_size), image_path)
        feed_dict={image_pl: data_batch, label_pl: label_batch, is_train_pl:False, lr_pl:lr}
        delta = sess.run(correct_count, feed_dict=feed_dict)
        cnt += delta
    accuracy = cnt / num_used
    print('accuracy: %f%%\n' % (accuracy * 100))


def submit_to_csv(image_names, pred_val):
    with open('submission.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['id']+read_img.dog_breeds)
        for k in range(len(image_names)):
            writer.writerow([image_names[k].split('.')[0]]+pred_val[k, :].tolist())





def train_model():
    data_train, data_val, data_test = read_img.read_img_file()

    with tf.Graph().as_default():
        image_pl, label_pl = input_placeholders()
        is_training_pl = tf.placeholder(tf.bool)
        lr_pl = tf.placeholder(tf.float32)

        logits = mnist_resnet_model(image_pl, is_training_pl)
        softmax=logits_to_softmax(logits)

        loss = _loss(label_pl, logits)
        train_op = _train(loss, lr_pl)
        correct_count = _correct_count(logits, label_pl)
        pred = predict(logits)
        init = tf.global_variables_initializer()

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        sess = tf.Session(config=config)

        sess.run(init)


        t0 = time.time()

        for k in range(FLAGS.max_step):
            data_batch = read_img.get_next_batch(data_train, FLAGS.batch_size, IMAGE_PATH[0])
            _, loss_val, corr_cnt = sess.run([train_op, loss, correct_count],
                                             feed_dict={image_pl: dataaug.data_aug(data_batch[0]),
                                                        label_pl: data_batch[1], is_training_pl: True,
                                                        lr_pl: FLAGS.learning_rate})

            if (k + 1) % 100 == 0:
                t = time.time() - t0
                print('time elapsed: %fs, step=%d, train loss=%f, correct_cnt in train batch=%d\n' % (
                t, k, loss_val, corr_cnt))
            if (k + 1) % 1000 == 0:
                print('eval train set, ', end='')
                do_eval(sess, correct_count, image_pl, label_pl, is_training_pl, data_train, lr_pl, FLAGS.learning_rate, IMAGE_PATH[0])
                print('eval val set, ', end='')
                do_eval(sess, correct_count, image_pl, label_pl, is_training_pl, data_val, lr_pl, FLAGS.learning_rate, IMAGE_PATH[0])
            if (k == 400):
                FLAGS.learning_rate = 0.1
            elif (k == 10e3):
                FLAGS.learning_rate = 0.01
            elif (k == 20e3):
                FLAGS.learning_rate = 0.001
            elif (k == 30e3):
                FLAGS.learning_rate = 0.0001

        # prediction
        pred_probability = np.zeros(shape=(data_test._size, 120), dtype=np.float32)
        for k in range(np.int(np.ceil(pred_probability.shape[0] / 100.0))):
            range_example=data_test._df[k * 100:np.min([(k + 1) * 100, pred_probability.shape[0]])]
            test_batch=read_img.image_batch_from_df(range_example, IMAGE_PATH[1])
            pred_probability[k * 100:np.min([(k + 1) * 100, pred_probability.shape[0]])] = sess.run(softmax, feed_dict={
                image_pl: test_batch[0], \
                label_pl: test_batch[1], is_training_pl: False, lr_pl: FLAGS.learning_rate})

        submit_to_csv(read_img.test_images, pred_probability)


def main():
    train_model()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--batch_size',
        type=int,
        default=16,
        help='batch size'
    )
    parser.add_argument(
        '--max_step',
        type=int,
        default=40000,
        help='max train steps'
    )
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=0.01,
        help='initial learning rate'
    )

    FLAGS, _ = parser.parse_known_args()
    main()

