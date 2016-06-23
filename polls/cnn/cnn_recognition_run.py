'''
Created on Jun 16, 2016

@author: Levan Tsinadze
'''

from cnn_image_reader import read_image_file
import tensorflow as tf
from src.cnn.mnist.cnn_files import training_file


# Network Parameters
n_input = 784  # MNIST data input (img shape: 28*28)
n_classes = 10  # MNIST total classes (0-9 digits)

class recognizer:
    
        # Create some wrappers for simplicity
    def conv2d(self, x, W, b, strides=1):
        # Conv2D wrapper, with bias and relu activation
        x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
        x = tf.nn.bias_add(x, b)
        return tf.nn.relu(x)
    
    
    def maxpool2d(self, x, k=2):
        # MaxPool2D wrapper
        return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],
                              padding='SAME')
    
    
    # Create model
    def conv_net(self, x, weights, biases, dropout):
        # Reshape input picture
        x = tf.reshape(x, shape=[-1, 28, 28, 1])
    
        # Convolution Layer
        conv1 = self.conv2d(x, weights['wc1'], biases['bc1'])
        # Max Pooling (down-sampling)
        conv1 = self.maxpool2d(conv1, k=2)
    
        # Convolution Layer
        conv2 = self.conv2d(conv1, weights['wc2'], biases['bc2'])
        # Max Pooling (down-sampling)
        conv2 = self.maxpool2d(conv2, k=2)
    
        # Fully connected layer
        # Reshape conv2 output to fit fully connected layer input
        fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
        fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])
        fc1 = tf.nn.relu(fc1)
        # Apply Dropout
        fc1 = tf.nn.dropout(fc1, dropout)
    
        # Output, class prediction
        out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])
        
        return out
    
    def get_pred(self):
        
        # Store layers weight & bias
        self.weights = {
            # 5x5 conv, 1 input, 32 outputs
            'wc1': tf.Variable(tf.random_normal([5, 5, 1, 32])),
            # 5x5 conv, 32 inputs, 64 outputs
            'wc2': tf.Variable(tf.random_normal([5, 5, 32, 64])),
            # fully connected, 7*7*64 inputs, 1024 outputs
            'wd1': tf.Variable(tf.random_normal([7 * 7 * 64, 1024])),
            # 1024 inputs, 10 outputs (class prediction)
            'out': tf.Variable(tf.random_normal([1024, n_classes]))
        }
        
        self.biases = {
            'bc1': tf.Variable(tf.random_normal([32])),
            'bc2': tf.Variable(tf.random_normal([64])),
            'bd1': tf.Variable(tf.random_normal([1024])),
            'out': tf.Variable(tf.random_normal([n_classes]))
        }
        # tf Graph input
        self.x = tf.placeholder(tf.float32, [None, n_input])
        self.keep_prob = tf.placeholder(tf.float32)  # dropout (keep probability)
        # Construct model
        pred = self.conv_net(self.x, self.weights, self.biases, self.keep_prob)
        
        return pred
    
    def recognize_image(self):
        
        pred = self.get_pred()
        
        # Evaluate model
        recognize_image = tf.argmax(pred, 1)
        
        saver = tf.train.Saver()
        tf.initialize_all_variables()
        tr_files = training_file()
        model_path = tr_files.get_files_directory()
                
            # dig_bytes = open(image_path, "rb").read()
            # print mnist.test.images[15]
        
        with tf.Session() as sess:
            print 'Start session'
            # Initialize variables
            saver.restore(sess, model_path)
            print "Model restored from file: %s" % model_path
            image_rec = read_image_file('/storage/ann/digits/torecogn')
            # Calculate accuracy for 256 mnist test images
            resp_dgt = sess.run(recognize_image, feed_dict={self.x: image_rec,
                                              self.keep_prob: 0.75})
            print "Recognized image:", resp_dgt[0]
        
        return resp_dgt[0]
        
