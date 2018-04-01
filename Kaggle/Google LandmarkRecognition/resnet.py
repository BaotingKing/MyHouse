'''

resnet model, v1 and v2

'''

import tensorflow as tf
import batch_norm
import math


def res_unit_v2(input, feature_map_in, feature_map_out, stride, is_training, scope, WEIGHT_DECAY):
	if(feature_map_out%4!=0):
		raise('output feature map num is not a multiple of 4, please re-design!')
	bottleneck_feature_map=feature_map_out//4
	
	if feature_map_in==feature_map_out:# keeping feature map number
		with tf.name_scope('conv1x1'):
			bn1=batch_norm.bn_layer_top(input, scope+'_conv1x1', is_training)
			relu1=tf.nn.relu(bn1)
			w1=tf.Variable(tf.random_normal([1, 1, feature_map_in, bottleneck_feature_map], stddev=math.sqrt(2/(feature_map_in))), dtype=tf.float32)
			b1=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv1=tf.nn.conv2d(relu1, w1, strides=[1, stride, stride, 1], padding='SAME')+b1
			tf.add_to_collection('losses', tf.nn.l2_loss(w1)*WEIGHT_DECAY)
		with tf.name_scope('conv3x3'):
			bn2=batch_norm.bn_layer_top(conv1, scope+'_conv3x3', is_training)
			relu2=tf.nn.relu(bn2)
			w2=tf.Variable(tf.random_normal([3, 3, bottleneck_feature_map, bottleneck_feature_map], stddev=math.sqrt(2/(9*bottleneck_feature_map))), dtype=tf.float32)
			b2=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv2=tf.nn.conv2d(relu2, w2, strides=[1, 1, 1, 1], padding='SAME')+b2
			tf.add_to_collection('losses', tf.nn.l2_loss(w2)*WEIGHT_DECAY)
		with tf.name_scope('conv1x1_2'):
			bn3=batch_norm.bn_layer_top(conv2, scope+'_conv1x1_2', is_training)
			relu3=tf.nn.relu(bn3)
			w3=tf.Variable(tf.random_normal([1, 1, bottleneck_feature_map, feature_map_out], stddev=math.sqrt(2/bottleneck_feature_map)), dtype=tf.float32)
			b3=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[feature_map_out]), dtype=tf.float32)
			output=tf.nn.conv2d(relu3, w3, strides=[1, 1, 1, 1], padding='SAME')+b3
			tf.add_to_collection('losses', tf.nn.l2_loss(w3)*WEIGHT_DECAY)
		return tf.add(input, output)
	else: # increasing feature map number
		bn_input=batch_norm.bn_layer_top(input, scope+'_common', is_training)
		relu_input=tf.nn.relu(bn_input)
		with tf.name_scope('conv1x1'):
			w1=tf.Variable(tf.random_normal([1, 1, feature_map_in, bottleneck_feature_map], stddev=math.sqrt(2/feature_map_in)), dtype=tf.float32)
			b1=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv1=tf.nn.conv2d(relu_input, w1, strides=[1, stride, stride, 1], padding='SAME')+b1
			tf.add_to_collection('losses', tf.nn.l2_loss(w1)*WEIGHT_DECAY)
		with tf.name_scope('conv3x3'):
			bn2=batch_norm.bn_layer_top(conv1, scope+'_conv3x3', is_training)
			relu2=tf.nn.relu(bn2)
			w2=tf.Variable(tf.random_normal([3, 3, bottleneck_feature_map, bottleneck_feature_map], stddev=math.sqrt(2/(9*bottleneck_feature_map))), dtype=tf.float32)
			b2=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv2=tf.nn.conv2d(relu2, w2, strides=[1, 1, 1, 1], padding='SAME')+b2
			tf.add_to_collection('losses', tf.nn.l2_loss(w2)*WEIGHT_DECAY)
		with tf.name_scope('conv1x1_2'):
			bn3=batch_norm.bn_layer_top(conv2, scope+'_conv1x1_2', is_training)
			relu3=tf.nn.relu(bn3)
			w3=tf.Variable(tf.random_normal([1, 1, bottleneck_feature_map, feature_map_out], stddev=math.sqrt(2/bottleneck_feature_map)), dtype=tf.float32)
			b3=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[feature_map_out]), dtype=tf.float32)
			output=tf.nn.conv2d(relu3, w3, strides=[1, 1, 1, 1], padding='SAME')+b3
			tf.add_to_collection('losses', tf.nn.l2_loss(w3)*WEIGHT_DECAY)
		with tf.name_scope('shortcut'):
			w_shortcut=tf.Variable(tf.random_normal([1, 1, feature_map_in, feature_map_out], stddev=math.sqrt(2/feature_map_in)), dtype=tf.float32)
			b_shortcut=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[feature_map_out]))
			shortcut_input=tf.nn.conv2d(relu_input, w_shortcut, strides=[1, stride, stride, 1], padding='SAME')+b_shortcut
			tf.add_to_collection('losses', tf.nn.l2_loss(w_shortcut)*WEIGHT_DECAY)
		return tf.add(shortcut_input, output)
		

def res_blk_v2(input, fm_in, fm_out, stride, count, is_training, scope, WEIGHT_DECAY):
	for k in range(count):
		with tf.name_scope(scope):
			if k==0:
				tmp=res_unit_v2(input, fm_in, fm_out, stride, is_training, scope+str(k), WEIGHT_DECAY)
			else:
				tmp=res_unit_v2(tmp, fm_out, fm_out, 1, is_training, scope+str(k), WEIGHT_DECAY)
	output=tmp
	return output 


def res_unit_v1(input, feature_map_in, feature_map_out, stride, is_training, scope, WEIGHT_DECAY):
	if(feature_map_out%4!=0):
		raise('output feature map num is not a multiple of 4, please re-design!')
	bottleneck_feature_map=feature_map_out//4
	
	if feature_map_in==feature_map_out:# keeping feature map number
		with tf.name_scope('conv1x1'):
			w1=tf.Variable(tf.random_normal([1, 1, feature_map_in, bottleneck_feature_map], stddev=math.sqrt(2/(feature_map_in))), dtype=tf.float32)
			b1=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv1=tf.nn.conv2d(input, w1, strides=[1, stride, stride, 1], padding='SAME')+b1
			bn1=batch_norm.bn_layer_top(conv1, scope+'_conv1x1', is_training)
			relu1=tf.nn.relu(bn1)
			tf.add_to_collection('losses', tf.nn.l2_loss(w1)*WEIGHT_DECAY)
		with tf.name_scope('conv3x3'):
			w2=tf.Variable(tf.random_normal([3, 3, bottleneck_feature_map, bottleneck_feature_map], stddev=math.sqrt(2/(9*bottleneck_feature_map))), dtype=tf.float32)
			b2=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv2=tf.nn.conv2d(relu1, w2, strides=[1, 1, 1, 1], padding='SAME')+b2
			bn2=batch_norm.bn_layer_top(conv2, scope+'_conv3x3', is_training)
			relu2=tf.nn.relu(bn2)
			tf.add_to_collection('losses', tf.nn.l2_loss(w2)*WEIGHT_DECAY)
		with tf.name_scope('conv1x1_2'):
			w3=tf.Variable(tf.random_normal([1, 1, bottleneck_feature_map, feature_map_out], stddev=math.sqrt(2/bottleneck_feature_map)), dtype=tf.float32)
			b3=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[feature_map_out]), dtype=tf.float32)
			conv3=tf.nn.conv2d(relu2, w3, strides=[1, 1, 1, 1], padding='SAME')+b3
			bn3=batch_norm.bn_layer_top(conv3, scope+'_conv1x1_2', is_training)
			output=tf.nn.relu(bn3+input)
			tf.add_to_collection('losses', tf.nn.l2_loss(w3)*WEIGHT_DECAY)
		return output
	else: # increasing feature map number
		with tf.name_scope('conv1x1'):
			w1=tf.Variable(tf.random_normal([1, 1, feature_map_in, bottleneck_feature_map], stddev=math.sqrt(2/feature_map_in)), dtype=tf.float32)
			b1=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv1=tf.nn.conv2d(input, w1, strides=[1, stride, stride, 1], padding='SAME')+b1
			bn1=batch_norm.bn_layer_top(conv1, scope+'_conv1x1', is_training)
			relu1=tf.nn.relu(bn1)
			tf.add_to_collection('losses', tf.nn.l2_loss(w1)*WEIGHT_DECAY)
		with tf.name_scope('conv3x3'):
			w2=tf.Variable(tf.random_normal([3, 3, bottleneck_feature_map, bottleneck_feature_map], stddev=math.sqrt(2/(9*bottleneck_feature_map))), dtype=tf.float32)
			b2=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[bottleneck_feature_map]), dtype=tf.float32)
			conv2=tf.nn.conv2d(relu1, w2, strides=[1, 1, 1, 1], padding='SAME')+b2
			bn2=batch_norm.bn_layer_top(conv2, scope+'_conv3x3', is_training)
			relu2=tf.nn.relu(bn2)
			tf.add_to_collection('losses', tf.nn.l2_loss(w2)*WEIGHT_DECAY)
		with tf.name_scope('conv1x1_2'):
			w3=tf.Variable(tf.random_normal([1, 1, bottleneck_feature_map, feature_map_out], stddev=math.sqrt(2/bottleneck_feature_map)), dtype=tf.float32)
			b3=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[feature_map_out]), dtype=tf.float32)
			conv3=tf.nn.conv2d(relu2, w3, strides=[1, 1, 1, 1], padding='SAME')+b3
			bn3=batch_norm.bn_layer_top(conv3, scope+'_conv1x1_2', is_training)
			tf.add_to_collection('losses', tf.nn.l2_loss(w3)*WEIGHT_DECAY)
		with tf.name_scope('shortcut'):
			w_shortcut=tf.Variable(tf.random_normal([1, 1, feature_map_in, feature_map_out], stddev=math.sqrt(2/feature_map_in)), dtype=tf.float32)
			b_shortcut=tf.Variable(tf.constant(0.0, dtype=tf.float32, shape=[feature_map_out]))
			shortcut_input=tf.nn.conv2d(input, w_shortcut, strides=[1, stride, stride, 1], padding='SAME')+b_shortcut
			bn_shortcut=batch_norm.bn_layer_top(shortcut_input, scope+'shortcut', is_training)
			tf.add_to_collection('losses', tf.nn.l2_loss(w_shortcut)*WEIGHT_DECAY)
		return tf.nn.relu(bn3+bn_shortcut)


def res_blk_v1(input, fm_in, fm_out, stride, count, is_training, scope, WEIGHT_DECAY):
	for k in range(count):
		with tf.name_scope(scope):
			if k==0:
				tmp=res_unit_v1(input, fm_in, fm_out, stride, is_training, scope+str(k), WEIGHT_DECAY)
			else:
				tmp=res_unit_v1(tmp, fm_out, fm_out, 1, is_training, scope+str(k), WEIGHT_DECAY)
	output=tmp
	return output 
