'''
Created on Jun 16, 2016

@author: Levan Tsinadze
'''

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

from cnn_functions import conv_net
from weights_biases import weights
from weights_biases import biases

from parameters_saver import parameters_file_conv_saved as model_path_saved

mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)
# Network Parameters
n_input = 784 # MNIST data input (img shape: 28*28)
n_classes = 10 # MNIST total classes (0-9 digits)
dropout = 0.75 # Dropout, probability to keep units

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)


# Construct model
pred = conv_net(x, weights, biases, keep_prob)

# Evaluate model
recognize_image = tf.argmax(pred, 1)

correct_pred = tf.equal(recognize_image, tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

save_path = 'parameters/cnn/images/recognition/convolution/parameters/conv_model.ckpt'
saver = tf.train.Saver()
init = tf.initialize_all_variables()
model_path = model_path_saved

with tf.Session() as sess:
    print 'Start session'
    # Initialize variables
    load_path = saver.restore(sess, model_path)
    print "Model restored from file: %s" % save_path
    print load_path
    
    # Calculate accuracy for 256 mnist test images
    print "Testing Accuracy:", \
        sess.run(accuracy, feed_dict={x: mnist.test.images[:256],
                                      y: mnist.test.labels[:256],
                                      keep_prob: 1.})
