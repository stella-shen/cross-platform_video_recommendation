#!usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os, configparser, json, logging
import h5py

def deep_model_recommendation(k, lam=0, c=0, rho=0, ri=0):
    tf.reset_default_graph()

    #tf graph input and output label
    #n_in is the dimension of the input
    #n_out is the dimension of the output
    X = tf.placeholder('float', [None, n_in])
    Y_ = tf.placeholder('float', [None, n_out])

    #tf graph parameters
    weights = {
        'weight1': tf.Variable(tf.random_uniform([n_in, k], minval=-np.sqrt(6/(n_in+k+1)), maxval=np.sqrt(6/(n_in+k+1)))),
        'weight2': tf.Variable(tf.random_uniform([k, n_out], minval=-np.sqrt(6/(n_out+k+1)), maxval=np.sqrt(6/(n_out+k+1))))
    }
    biases = {
        'bias1': tf.Variable(tf.zeros(k)),
        'bias2': tf.Variable(tf.zeros(n_out))
    }

    #Build the graph
    with tf.name_scope('hidden_layer'):
        hidden_layer = tf.nn.sigmoid(tf.matmul(X, weights['weight1']) + biases['bias1'])
    with tf.name_scope('output'):
        Y = tf.nn.sigmoid(tf.matmul(hidden_layer, weights['weight2']) + biases['bias2'])

    #Calculate loss
    with tf.name_scope('loss'):
        error = tf.nn.l2_loss(Y - Y_)
        regularizer = lam * tf.add_n([tf.nn.l2_loss(i) for i in weights.values()])
        cost_op = error + regularizer
        average_action = tf.reduce_mean(hidden_layer, axis=0)
        cost_op += c * tf.reduce_sum(rho*tf.log(rho/average_action) + (1-rho)*tf.log((1-rho)/(1-average_action)))
    
    optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(cost_op)

    #Initializing the variables
    init_op = tf.global_variables_initializer()

    #Define evaluation metrics
    def calcMAE(tensor):
        return tf.reduce_mean(tf.abs(tensor))

    with tf.name_scope('evaluation'):
        mae_op = calcMAE(Y - Y_)

    #Save and restore all variables
    saver = tf.train.Saver()

    #Define recording metrics
    cost_train = np.zeros(max_iteration)
    mae_train = np.zeros(max_iteration)
    mae_test = np.zeros(max_iteration//test_step)

    #Launch the graph
    with tf.Session() as sess:
        logging.info('initializing...')
        sess.run(init_op)
        
        #Traing cycle
        logging.info('training...')
        for epoch in range(max_iteration):
            opt, cost, mae = sess.run([optimizer, cost_op, mae_op], feed_dict={X: U1_train, Y_: U2_train})
            cost_train[epoch] = cost
            mae_train[epoch] = mae

            #Display logs per epoch step
            if epoch % display_step == 0:
                logging.info('Training -- epoch={} cost={} mae={}'.format(epoch, cost, mae))

            #Test and evaluation
            if epoch % test_step == 0:
                mae, = sess.run([mae_op], feed_dict={X: U1_test, Y_: U2_test})
                mae_test[epoch//test_step] = mae
                logging.info('Testing mae={}'.format(mae))

        saver.save(sess, odir+'model_r{}.ckpt'.format(ri))

    #Plot figures
    plt.figure()
    plt.plot(cost_train)
    plt.savefig(odir+'cost_train_r{}.png'.format(ri))

    plt.figure()
    plt.plot(mae_train)
    plt.savefig(odir+'mae_train_r{}.png'.format(ri))

    plt.figure()
    plt.plot(mae_test)
    plt.savefig(odir+'mae_test_r{}.png'.format(ri))

    plt.close('all')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    logging.info('loading data...')
    with h5py.File('../mat/U1_train.h5', 'r') as f:
        U1_train = f['data'][:]
    with h5py.File('../mat/U2_train.h5', 'r') as f:
        U2_train = f['data'][:]
    with h5py.File('../mat/U1_test.h5', 'r') as f:
        U1_test = f['data'][:]
    with h5py.File('../mat/U2_test.h5', 'r') as f:
        U2_test = f['data'][:]
    logging.info('complete')
    logging.info('')

    batch_size = U1_train.shape[0]
    n_in = U1_train.shape[1]
    n_out = U2_train.shape[1]

    test_id = '1'
    tdir = '../deep_recommendation/test_' + test_id + '/'

    #parameter
    #when hidden layer is none, the hidden units k is not needed
    ks = [40, 50, 60, 80, 100, 120, 150, 180, 200, 250, 300]
    lams = [0, 0.1, 0.01, 0.06, 0.03]
    cs = [1, 3, 10, 30, 50, 80, 100]
    rhos = [0.01, 0.03, 0.05, 0.1]

    #global
    num_replication = 6
    max_iteration = 1000
    learning_rate = 0.001
    display_step = 10
    test_step = 50

    for k in ks:
        for lam in lams:
            for c in cs:
                for rho in rhos:
                    odir = tdir + 'k{}_lam{}_c{}_rho{}/'.format(k, lam, c, rho)
                    if not os.path.exists(odir):
                        os.makedirs(odir)

                    #write config to files
                    cf = configparser.ConfigParser()
                    with open(odir + 'settings.cfg', 'w') as f:
                        cf.add_section('parameter')
                        cf.set('parameter', 'k', json.dumps(k))
                        cf.set('parameter', 'lam', str(lam))
                        cf.set('parameter', 'c', str(c))
                        cf.set('parameter', 'rho', str(rho))

                        cf.add_section('global')
                        cf.set('global', 'num_replication', str(num_replication))
                        cf.set('global', 'max_iteration', str(max_iteration))
                        cf.set('global', 'learning_rate', str(learning_rate))
                        cf.set('global', 'display_step', str(display_step))
                        cf.set('global', 'test_step', str(test_step))
                        cf.write(f)

                    for ri in range(num_replication):
                        # add filehandler to logging
                        fh = logging.FileHandler(filename=odir+'log_r{}'.format(ri), mode='w', encoding='utf-8')
                        fh.setFormatter(logging.Formatter('%(message)s'))
                        fh.setLevel(logging.INFO)
                        logging.root.addHandler(fh)

                        deep_model_recommendation(k, lam, c, rho, ri)

                        logging.root.removeHandler(fh)
