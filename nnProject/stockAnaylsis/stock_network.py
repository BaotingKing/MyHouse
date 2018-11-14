#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2018/11/7

import numpy as np
import pandas as pd
import config as cfg
import random


def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))


def sigmoid_prim(z):
    """sigmoid函数的导数"""
    return sigmoid(z)*(1 - sigmoid(z))


def activation_fun(z, mode='sigmoid'):
    if mode == 'sigmoid':
        z = 1.0/(1.0+np.exp(-z))
    else:
        z = z
    return z


def activation_diff(z, mode='sigmoid'):
    if mode == 'sigmoid':
        z = sigmoid(z)*(1 - sigmoid(z))
    else:
        z = z
    return z


def parameters_init():
    pass


class StockNetwork(object):
    def __init__(self, sizes=0, param_from_csv=False):
        """参数sizes表示每一层神经元的个数，如[2,3,1],表示第一层有2个神经元，
        第二层有3个神经元，第三层有1个神经元."""
        self.num_layers = len(sizes)
        self.sizes = sizes
        np.random.seed(5)
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

        if param_from_csv:
            df_param = pd.read_csv('./data/parameters.csv')
            biases = df_param['biases']
            weights = df_param['weights']
            if (self.biases.shape != biases.shape) | (self.weights.shape != weights.shape):
                print('[Debug]: Parameter sizes do not match!')
            self.biases = biases
            self.weights = weights

    def forward(self, x, flag=1):
        """forward propagation"""
        activation = x
        activations = [x]    # store all activations, layer by layer

        zs = []    # store all z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = activation_fun(z)
            activations.append(activation)

        y = activations[-1]

        if flag == 1:
            return y, zs, activations
        else:
            return y

    def backward(self, x, y_):
        """返回一个元组(n_biase, n_weight)代表目标函数的梯度."""
        nabla_biase = [np.zeros(b.shape) for b in self.biases]
        nabla_weight = [np.zeros(w.shape) for w in self.weights]

        # forward propagation
        y, zs, activations = self.forward(x)

        # backward propagation=====>>>>Chain derivative process
        delta = (y - y_) * activation_diff(zs[-1])    # y表示预测结果，y_表示真实结果

        nabla_biase[-1] = delta
        nabla_weight[-1] = np.dot(delta, activations[-2].transpose())
        """l = 1表示最后一层神经元，l = 2是倒数第二次神经元，以此类推"""
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = activation_diff(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_biase[-l] = delta
            nabla_weight[-l] = np.dot(delta, activations[-l - 1].transpose())
        return nabla_biase, nabla_weight

    def update_mini_batch(self, mini_batch, learn_rate):
        """使用后向传播算法进行参数更新.mini_batch是一个元组(x, y)的列表、learn_rate是学习速率"""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        for n in range(len(mini_batch)):
            if n < cfg.g_fitting_size:
                continue
            elif len(mini_batch) < cfg.g_fitting_size:
                break

            X = []
            for x, y_ in mini_batch[n - cfg.g_fitting_size:n]:
                X.extend(x)

            x, y_ = mini_batch[n]

            delta_nabla_b, delta_nabla_w = self.backward(np.array(X), y_)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            self.weights = [w - (learn_rate / len(mini_batch)) * nw
                            for w, nw in zip(self.weights, nabla_w)]
            self.biases = [b - (learn_rate / len(mini_batch)) * nb
                           for b, nb in zip(self.biases, nabla_b)]

    def SGD(self, training_data, epochs, mini_batch_size, learn_rate, test_data=None):
        """Stochastic gradient descent algorithm"""

        n_train = len(training_data)
        for j in range(epochs):
            mini_batches = []
            # random.shuffle(training_data)
            # mini_batches = [
            #     training_data[k:k+mini_batch_size]
            #     for k in range(0, n_train, mini_batch_size)
            # ]
            for k in range(0, n_train, mini_batch_size):
                if k == 0:
                    mini_batches.append(training_data[k:k + mini_batch_size])
                else:
                    mini_batches.append(training_data[k - 3:k + mini_batch_size])

            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, learn_rate=learn_rate)

            if test_data:
                print("Epoch {0}: {1} / {2}".
                      format(j, self.evaluate(test_data), len(test_data)))
            else:
                print("Epoch {0} complete".format(j))
                # print('The biases is\n{0}\n{1}\n:'.format(len(self.biases), self.biases))
                # print('The weights is\n{0}\n{1}\n:'.format(len(self.weights), self.weights))

        if test_data:
            df_param = pd.DataFrame({'biases': self.biases, 'weights': self.weights})
            df_param.to_csv('./data/parameters.csv')

    def evaluate(self, test_data):
        """返回预测正确的个数"""
        g_max_close = cfg.get_value('g_max_close')
        g_min_close = cfg.get_value('g_min_close')
        cnt = 0
        denominator = g_max_close - g_min_close
        for n in range(len(test_data)):
            if n < cfg.g_fitting_size:
                continue
            elif len(test_data) < cfg.g_fitting_size:
                print('The amount of data is too small, must big than{0}'.format(cfg.g_fitting_size))
                break

            X = []
            for x, y_ in test_data[n - cfg.g_fitting_size:n]:
                X.extend(x)

            _, y_ = test_data[n]
            y = self.forward(X, flag=0)

            y = y * denominator + g_min_close
            y_ = y_ * denominator + g_min_close

            if abs(y - y_) <= 1e-1:
                cnt += 1

        return cnt
        # return sum(int(x == y_) for (x, y_) in test_results)









