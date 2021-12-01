# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Dongze Xie & Guochen Yu time: 2021/12/01
# implement ADP algorithm

import tensorflow as tf
import numpy as np
pattern_dict = {'bla_pattern_01': [1, 1, 1, 1, 1],         'bla_pattern_02': [-1, 1, 1, 1, 1, -1],
                'bla_pattern_03': [-1, 1, 1, 1, -1, -1],   'bla_pattern_04': [-1, -1, 1, 1, 1, -1],
                'bla_pattern_05': [-1, 1, 1, -1, 1, -1],   'bla_pattern_06': [-1, 1, -1, 1, 1, -1],
                'bla_pattern_07': [1, 1, 1, 1, -1],        'bla_pattern_08': [-1, 1, 1, 1, 1],
                'bla_pattern_09': [1, 1, -1, 1, 1],        'bla_pattern_10': [1, -1, 1, 1, 1],
                'bla_pattern_11': [1, 1, 1, -1, 1],        'bla_pattern_12': [-1, -1, 1, 1, -1, -1],
                'bla_pattern_13': [-1, -1, 1, -1, 1, -1],  'bla_pattern_14': [-1, 1, -1, 1, -1, -1],
                'bla_pattern_15': [-1, -1, -1, 1, -1, -1], 'bla_pattern_16': [-1, -1, 1, -1, -1, -1],
                'bla_pattern_17': [-1, 1, -1, -1, 1, -1],  'bla_pattern_18': [1, -1, -1, -1, 1],
                'bla_pattern_19': [1, 1, -1, -1, 1],       'bla_pattern_20': [1, 1, -1, -1, -1],
                'whi_pattern_01': [0, 0, 0, 0, 0],         'whi_pattern_02': [-1, 0, 0, 0, 0, -1],
                'whi_pattern_03': [-1, 0, 0, 0, -1, -1],   'whi_pattern_04': [-1, -1, 0, 0, 0, -1],
                'whi_pattern_05': [-1, 0, 0, -1, 0, -1],   'whi_pattern_06': [-1, 0, -1, 0, 0, -1],
                'whi_pattern_07': [0, 0, 0, 0, -1],        'whi_pattern_08': [-1, 0, 0, 0, 0],
                'whi_pattern_09': [0, 0, -1, 0, 0],        'whi_pattern_10': [0, -1, 0, 0, 0],
                'whi_pattern_11': [0, 0, 0, -1, 0],        'whi_pattern_12': [-1, -1, 0, 0, -1, -1],
                'whi_pattern_13': [-1, -1, 0, -1, 0, -1],  'whi_pattern_14': [-1, 0, -1, 0, -1, -1],
                'whi_pattern_15': [-1, -1, -1, 0, -1, -1], 'whi_pattern_16': [-1, -1, 0, -1, -1, -1],
                'whi_pattern_17': [-1, 0, -1, -1, 0, -1],  'whi_pattern_18': [0, -1, -1, -1, 0],
                'whi_pattern_19': [0, 0, -1, -1, 0],       'whi_pattern_20': [0, 0, -1, -1, -1]}


class ADP(object):
    def __init__(self, _board, _select_color, _player_turn):
        self.board = _board
        self.select_color = _select_color
        self.player_turn = _player_turn
        self.input_x = [0.]*122

    def init_input(self):
        # pattern_number = 0
        pattern_number_list = []
        for pattern in pattern_dict.values():
            print(pattern)
            pattern_number = self.find_pattern_number(pattern)
            pattern_number_list.append(pattern_number)
        if self.select_color == 1:  # computer select black
            for i in range(len(pattern_number_list)-20):
                self.input_x[i] = pattern_number_list[i]  # input node of the number of specific shape pattern for black 
                self.input_x[i+20] = pattern_number_list[i+20]  # input node of the number of specific shape pattern for white
                if self.player_turn == 1:  # current turn，human black，AI white
                    # black side
                    if pattern_number_list[i] != 0:  # some specific shape pattern shows
                        self.input_x[i+40] = 0
                        self.input_x[i*2+40] = 1
                    else:                            # some specific shape pattern doesnot show
                        self.input_x[i+40] = 0
                        self.input_x[i*2+40] = 0
                    # white side
                    if pattern_number_list[i+20] != 0:
                        self.input_x[i+80] = 1
                        self.input_x[i*2+80] = 0
                    else:
                        self.input_x[i+80] = 0
                        self.input_x[i*2+80] = 0
                    self.input_x[110] = 1
                    self.input_x[111] = 0

                if self.player_turn == 0:  # current turn，human white，AI black
                    # black side
                    if pattern_number_list[i] != 0:
                        self.input_x[i+40] = 0
                        self.input_x[i*2+40] = 1
                    else:
                        self.input_x[i+40] = 0
                        self.input_x[i*2+40] = 0
                    # white side
                    if pattern_number_list[i+20] != 0:
                        self.input_x[i+80] = 1
                        self.input_x[i*2+80] = 0
                    else:
                        self.input_x[i+80] = 0
                        self.input_x[i*2+80] = 0
                    self.input_x[110] = 1
                    self.input_x[111] = 0

        for i in range(len(pattern_number_list)):
            if self.player_turn == 1:
                self.input_x[i] = pattern_number_list[i]
                self.input_x[40+i] = 0

    def find_pattern_number(self, _pattern):
        # search for the twenty corresponding shape pattern,and return the number count 
        _pattern_number = 0
        k = len(_pattern)
        # x orientation
        for i in range(15):
            for j in range(15):
                # tmp_pattern = [self.board[i][j], self.board[i][j+1], self.board[i][j+2],
                #                self.board[i][j+3], self.board[i][j+4], self.board[i][j+5]]
                # if tmp_pattern == _pattern:
                #     _pattern_number += 1
                # x direction
                tmp_pattern = []
                for l in range(k):
                    tmp_pattern = tmp_pattern.append(self.board[i][j+l])
                if tmp_pattern == _pattern:
                    _pattern_number += 1
                # y direction
                tmp_pattern = []
                for l in range(k):
                    tmp_pattern = tmp_pattern.append(self.board[i+l][j])
                if tmp_pattern == _pattern:
                    _pattern_number += 1
                # y=x direction
                tmp_pattern = []
                for l in range(k):
                    tmp_pattern = tmp_pattern.append(self.board[i+l][j-l])
                if tmp_pattern == _pattern:
                    _pattern_number += 1
                # y=-x direction
                tmp_pattern = []
                for l in range(k):
                    tmp_pattern = tmp_pattern.append(self.board[i+l][j+l])
                if tmp_pattern == _pattern:
                    _pattern_number += 1
        return _pattern_number
        # y orientation
        # for i in range(15):
        #     for j in range(15):
        #         tmp_pattern = [self.board[i][j], self.board[i+1][j], self.board[i+2][j],
        #                        self.board[i+3][j], self.board[i+4][j], self.board[i+5][j]]
        #         if tmp_pattern == _pattern:
        #             _pattern_number += 1
        # # y=x orientation
        # for i in range(15):
        #     for j in range(15):
        #         tmp_pattern = [self.board[i][j], self.board[i-1][j+1], self.board[i-2][j+2],
        #                        self.board[i-3][j+3], self.board[i-4][j+4], self.board[i-5][j+5]]
        #         if tmp_pattern == _pattern:
        #             _pattern_number += 1
        # # y=-x orientation
        # for i in range(15):
        #     for j in range(15):
        #         tmp_pattern = [self.board[i][j], self.board[i-1][j-1], self.board[i-2][j-2],
        #                        self.board[i-3][j-3], self.board[i-4][j-4], self.board[i-5][j-5]]
        #         if tmp_pattern == _pattern:
        #             _pattern_number += 1
        #return _pattern_number

    def init_weight(self, _input):
        pass

    def critic_network(self):
        def add_layer(input_data, in_size, out_size, activity_function=None):

            weights = tf.Variable(tf.truncated_normal([in_size, out_size], mean=0, stddev=0.1))  # initialize weight using partial normal distribution
            # basis = tf.Variable(tf.zeros([1, outSize]) + 0.1)  # no need for now
            weights_plus_b = tf.matmul(input_data, weights)  # + basis
            if activity_function is None:
                output = weights_plus_b
            else:
                output = activity_function(weights_plus_b)
            return output

        # x_data = np.linspace(-1, 1, 300)[:, np.newaxis]  #transpose vector( zhuanzhi xiangliang)
        # noise = np.random.normal(0, 0.05, x_data.shape)
        # y_data = np.square(x_data) + 0.5 + noise

        xs = tf.placeholder(tf.float32, [122, 1])  
        ys = tf.placeholder(tf.float32, [60, 1])

        l1 = add_layer(xs, 122, 60, activity_function=tf.nn.sigmoid)
        # sigmoid is a kind of excitation function，122 input nodes，60 hidden nodes(still need more time to figure out)
        l2 = add_layer(l1, 60, 1, activity_function=tf.nn.sigmoid)
        # 60 hidden layer nodes，one input layer node
        loss = tf.reduce_mean(tf.reduce_sum(tf.square((ys - l2)), reduction_indices=[1]))  

        train = tf.train.GradientDescentOptimizer(0.1).minimize(loss)  # choose gradient descent method

        init = tf.initialize_all_variables()
        sess = tf.Session()
        # sess = tf.InteractiveSession()
        sess.run(init)

        # for i in range(10000):
        #     sess.run(train, feed_dict={xs: self.x_data})
        #     if i % 50 == 0:
        #         print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))

    def action_policy(self):
        pass

    def back_propagation(self):
        pass


if __name__ == "__main__":
    pass

