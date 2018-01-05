import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

INPUT_NODE_NUMBER = 784
OUTPUT_NODE_NUMBER = 10

LEARNING_RATE = 0.01
EPOCHES_NUMBER = 1000


def layer(name, input, shape, activation=tf.nn.relu):
    with tf.variable_scope(name):
        w = tf.get_variable('weight', shape, initializer=tf.random_normal_initializer)
        b = tf.zeros((1, shape[1]), name='biase')
        a = activation(tf.matmul(input, w) + b)
    return a


def reference(x, activation = tf.nn.relu):
    layer1 = layer('hidden1', x, (INPUT_NODE_NUMBER, 1000))
    layer2 = layer('hidden2', layer1, (1000, 500))
    layer3 = layer('output', layer2, (500, 10), activation=tf.identity)
    return layer3


x = tf.placeholder(shape=(None, 784), dtype=tf.float32, name='x')
y = tf.placeholder(shape=(None, 10), dtype=tf.int8, name='y')

y_ = reference(x)
cross_entropy_cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_))

train_op = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cross_entropy_cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    mnist = input_data.read_data_sets('dir_with_mnist_data_files', one_hot=True, seed=3)

    for i in range(EPOCHES_NUMBER):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size=100)
        _, cost = sess.run([train_op, cross_entropy_cost], feed_dict={x:batch_xs, y:batch_ys})

        if i % 50 == 0:
            print("cost %f" % cost)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    accuracy = sess.run(accuracy, feed_dict={x: mnist.validation.images, y :mnist.validation.labels})
    print("accuracy: %s"%accuracy)
















