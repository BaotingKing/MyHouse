import tensorflow as tf
import numpy as np


#incorrect
def batch_norm(x, scope_bn, is_training):
    shape_list=x.shape.as_list()
    with tf.variable_scope(scope_bn):
        beta=tf.Variable(tf.constant(0.0, shape=[shape_list[-1]]), name='beta', trainable=True)
        gamma=tf.Variable(tf.constant(1.0, shape=[shape_list[-1]]), name='gamma', trainable=True)
        axes=np.arange(len(shape_list)-1)
        batch_mean, batch_var=tf.nn.moments(x, axes, name='moments', keep_dims=True)
        ema=tf.train.ExponentialMovingAverage(decay=0.999)
        def mean_var_with_update():
            ema_apply_op=ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)
        mean, var=tf.cond(is_training, mean_var_with_update, lambda: (ema.average(batch_mean), ema.average(batch_var)))
        x_normed=tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
    return x_normed 

#incorrect
def batch_norm_v2(x, scope_bn, is_training, decay=0.999):
    shape_list=x.shape.as_list()
    with tf.variable_scope(scope_bn):
        beta=tf.get_variable('beta', [shape_list[-1]], initializer=tf.constant_initializer(0.0), trainable=True)
        gamma=tf.get_variable('gamma', [shape_list[-1]], initializer=tf.constant_initializer(1.0), trainable=True)
        moving_avg = tf.get_variable("moving_avg", [shape_list[-1]], initializer=tf.constant_initializer(0.0), trainable=False)
        moving_var = tf.get_variable("moving_var", [shape_list[-1]], initializer=tf.constant_initializer(1.0), trainable=False)
    axes=np.arange(len(shape_list)-1)
    batch_mean, batch_var=tf.nn.moments(x, axes, name='moments', keep_dims=True)
    batch_mean=tf.reshape(batch_mean, [shape_list[-1]])
    batch_var=tf.reshape(batch_var, [shape_list[-1]])
    mean_update_op=tf.assign(moving_avg, moving_avg*decay+batch_mean*(1-decay))
    var_update_op=tf.assign(moving_var, moving_var*decay+batch_var*(1-decay))
    mean_var_update_op=[mean_update_op, var_update_op]
    mean, var=tf.cond(is_training, lambda: (batch_mean, batch_var), lambda: (moving_avg, moving_var))
    with tf.control_dependencies(mean_var_update_op):
        x_normed=tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
    return x_normed

#incorrect
def batch_norm_layer(x, scope_bn, is_training_pl):
    bn_train=tf.contrib.layers.batch_norm(x, center=True, scale=True, epsilon=0.001, is_training=True, updates_collections=None, reuse=None, scope=scope_bn)
    bn_test=tf.contrib.layers.batch_norm(x, center=True, scale=True, epsilon=0.001, is_training=False, updates_collections=None, reuse=True, scope=scope_bn)
    return tf.cond(is_training_pl, lambda:bn_train, lambda:bn_test)


def bn_layer(x, scope, is_training, epsilon=0.001, decay=0.99, reuse=None):
    """
    Performs a batch normalization layer

    Args:
        x: input tensor
        scope: scope name
        is_training: python boolean value
        epsilon: the variance epsilon - a small float number to avoid dividing by 0
        decay: the moving average decay

    Returns:
        The ops of a batch normalization layer
    """
    with tf.variable_scope(scope, reuse=reuse):
        shape = x.get_shape().as_list()
        # gamma: a trainable scale factor
        gamma = tf.get_variable("gamma", shape[-1], initializer=tf.constant_initializer(1.0), trainable=True)
        # beta: a trainable shift value
        beta = tf.get_variable("beta", shape[-1], initializer=tf.constant_initializer(0.0), trainable=True)
        moving_avg = tf.get_variable("moving_avg", shape[-1], initializer=tf.constant_initializer(0.0), trainable=False)
        moving_var = tf.get_variable("moving_var", shape[-1], initializer=tf.constant_initializer(1.0), trainable=False)
        if is_training:
            # tf.nn.moments == Calculate the mean and the variance of the tensor x
            avg, var = tf.nn.moments(x, np.arange(len(shape)-1), keep_dims=True)
            avg=tf.reshape(avg, [avg.shape.as_list()[-1]])
            var=tf.reshape(var, [var.shape.as_list()[-1]])
            #update_moving_avg = moving_averages.assign_moving_average(moving_avg, avg, decay)
            update_moving_avg=tf.assign(moving_avg, moving_avg*decay+avg*(1-decay))
            #update_moving_var = moving_averages.assign_moving_average(moving_var, var, decay)
            update_moving_var=tf.assign(moving_var, moving_var*decay+var*(1-decay))
            control_inputs = [update_moving_avg, update_moving_var]
        else:
            avg = moving_avg
            var = moving_var
            control_inputs = []
        with tf.control_dependencies(control_inputs):
            output = tf.nn.batch_normalization(x, avg, var, offset=beta, scale=gamma, variance_epsilon=epsilon)

    return output

# correct
def bn_layer_top(x, scope, is_training, epsilon=0.001, decay=0.99):
    """
    Returns a batch normalization layer that automatically switch between train and test phases based on the 
    tensor is_training

    Args:
        x: input tensor
        scope: scope name
        is_training: boolean tensor or variable
        epsilon: epsilon parameter - see batch_norm_layer
        decay: epsilon parameter - see batch_norm_layer

    Returns:
        The correct batch normalization layer based on the value of is_training
    """
    #assert isinstance(is_training, (ops.Tensor, variables.Variable)) and is_training.dtype == tf.bool

    return tf.cond(
        is_training,
        lambda: bn_layer(x=x, scope=scope, epsilon=epsilon, decay=decay, is_training=True, reuse=None),
        lambda: bn_layer(x=x, scope=scope, epsilon=epsilon, decay=decay, is_training=False, reuse=True),
    )
    
