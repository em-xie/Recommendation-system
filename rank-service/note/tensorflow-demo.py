import tensorflow as tf
import pandas as pd
import numpy as np
from svd import Svd
import math
import time
import util
from tensorflow import keras
# f(a,b) = 3a - 2b
# a_vec = np.random.randint(10, size=1000)
# b_vec = np.random.randint(10, size=1000)
#
# print(a_vec[:10])
#
# print(b_vec[:10])
#
# f_vec = a_vec * 3 - b_vec * 2
# print(f_vec[:10])


# keras model


# # 构建模型
# model = keras.Sequential([
#     #1层神经网络 2个输入 一个输出相连 1个神经元
#     keras.layers.Dense(1, input_dim=2)
#
# ])
# model.compille(
#     loss='mean_squared_error'
# )
# input = np.stack([a_vec,b_vec],axis=1)
# print(input)
#
# model.fit(input,f_vec,epochs=300)
# preds = model(input)
# print(preds[:10])
#
# def show_diff(preds,ys,m):
#     preds = preds.numpy()
#     preds = [int(np.round(x))for x in preds[:m]]
#     print(preds)
#     print(list(ys[:m]))
#
# show_diff(preds,f_vec,10)
# model.trainable_variables

# anime_df = pd.read_csv('E://PyCode/Recommendation-system/dataset/anime.csv', index_col='anime_id')
data = pd.read_csv('E://PyCode/Recommendation-system/dataset/rating.csv')
# 数据数量
size = np.size(data['user_id'])
print(size)
# 批次
epoch = 5
# 一批数量
batch_size = 1000

user_batch = tf.placeholder(tf.int32, shape=[None], name='user_id')
item_batch = tf.placeholder(tf.int32, shape=[None], name='item_id')
rate_batch = tf.placeholder(tf.float32, shape=[None], name="rating")


svd = Svd(32, size, size)

infer, regularizer = svd.model(user_batch, item_batch)

global_step = tf.train.get_or_create_global_step()

cost, train_op = svd.optimization(infer, regularizer, rate_batch)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    train_size = int(math.ceil(epoch * size / batch_size))

    for i in range(train_size):

        batch_data = util.random_batch(batch_size, data, size)

        feed_dict = {
            user_batch: util.user_to_inner_index(batch_data['user_id'], data['user_id']),
            item_batch: util.item_to_inner_index(batch_data['anime_id'], data['user_id']),
            rate_batch: batch_data['rating'],
        }
        pred_batch, _ = sess.run([infer, train_op], feed_dict=feed_dict)
        loss = np.sqrt(np.mean(np.power(pred_batch - batch_data['rating'], 2)))
        if i % 1000 == 0:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'loss: ' + str(loss))

    save_path = tf.train.Saver(max_to_keep=1).save(sess, "./ckpt")
    print("Model saved in file: %s" % save_path)