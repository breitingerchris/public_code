import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

n1 = 500
n2 = 500
n3 = 500

cl = 10

x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

def nn(data):
    h1 = {
        'weights': tf.Variable(tf.random_normal([784, n1])),
        'biases': tf.Variable(tf.random_normal([n1]))
    }
    h2 = {
        'weights': tf.Variable(tf.random_normal([n1, n2])),
        'biases': tf.Variable(tf.random_normal([n2]))
    }
    h3 = {
        'weights': tf.Variable(tf.random_normal([n2, n3])),
        'biases': tf.Variable(tf.random_normal([n3]))
    }
    o = {
        'weights': tf.Variable(tf.random_normal([n3, cl])),
        'biases': tf.Variable(tf.random_normal([cl]))
    }

    l1 = tf.add(tf.matmul(data, h1['weights']), h1['biases'])
    l1 = tf.nn.relu(l1)
    l2 = tf.add(tf.matmul(l1, h2['weights']), h2['biases'])
    l2 = tf.nn.relu(l2)
    l3 = tf.add(tf.matmul(l2, h3['weights']), h3['biases'])
    l3 = tf.nn.relu(l3)

    out = tf.add(tf.matmul(l3, o['weights']), o['biases'])

    return out

def train(x):
    prediction = nn(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y))
    opti = tf.train.AdadeltaOptimizer().minimize(cost)
    epochs = 10

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for e in range(epochs):
            e_loss = 0
            for _ in range(int(mnist.train.num_examples/100)):
                ex, ey = mnist.train.next_batch(100)
                _, c = sess.run([opti, cost], feed_dict={x: ex, y: ey})
                print('E:', e, 'L:', e_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accu = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:', accu.eval({x: mnist.test.images, y: mnist.test.labels}))

train(x)