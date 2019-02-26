# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.ops import rnn, rnn_cell



mnist = input_data.read_data_sets('/tmp/data', one_hot=True)


# Cycles of feed forward + backpropagation
n_epochs = 3
n_classes = 10
batch_size = 128
chunk_size = 28
n_chunks = 28
rnn_size = 128

X = tf.placeholder('float',[None, n_chunks, chunk_size])
y = tf.placeholder('float')


def recurrent_neural_network(x):
    layer = {'weights':tf.Variable(tf.random_normal([rnn_size,n_classes])),
             'biases':tf.Variable(tf.random_normal([n_classes]))}

    x = tf.transpose(x, [1,0,2])
    x = tf.reshape(x, [-1, chunk_size])
    x = tf.split(x, n_chunks, 0)

    lstm_cell = rnn_cell.BasicLSTMCell(rnn_size,state_is_tuple=True)
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    output = tf.matmul(outputs[-1],layer['weights']) + layer['biases']

    return output



def train_neural_network(X):
    # Get output from neural network
    prediction = recurrent_neural_network(X)
    # Get cost
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))

    # default learning rate = 0.001
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    
    
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        # Training data
        for epoch in range(n_epochs):
            epoch_loss = 0
            
            for _ in range(int(int(mnist.train.num_examples/batch_size))):
                epoch_X, epoch_y = mnist.train.next_batch(batch_size)
                epoch_X = epoch_X.reshape(batch_size, n_chunks, chunk_size)
                _, c = sess.run([optimizer,cost], feed_dict={X: epoch_X, y: epoch_y}) # c = cost
                epoch_loss += c
            print('Epoch:', epoch, 'completed out of', n_epochs, 'loss:', epoch_loss)
             
        
        
        # 
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:', accuracy.eval({X:mnist.test.images.reshape(-1, n_chunks, chunk_size), y: mnist.test.labels}))



train_neural_network(X)



