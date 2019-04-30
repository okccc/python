# coding=utf-8
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 关闭warning


# 创建一张图：包含op和tensor,上下文环境
# op：operation(函数)
# tensor：张量(数据)
g = tf.Graph()
# print(type(g))  # <class 'tensorflow.python.framework.ops.Graph'>
with g.as_default():
    t = tf.constant(1)
    # print(t)  # Tensor("Const:0", shape=(), dtype=int32)
a = tf.constant(5)
b = tf.constant(6)
c = tf.add(a, b)
# print(type(a))  # <class 'tensorflow.python.framework.ops.Tensor'>
# print(type(c))  # <class 'tensorflow.python.framework.ops.Tensor'>

# 默认图,相当于给程序分配一段内存
graph = tf.get_default_graph()
# print(type(graph))  # <class 'tensorflow.python.framework.ops.Graph'>

# placeholder是占位符
ph = tf.placeholder(dtype=tf.float32, shape=[None, 3])
# print(ph)  # Tensor("Placeholder:0", shape=(?, 3), dtype=float32)

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    # 在会话当中运行指定的图,feed_dict给占位符ph传入一个字典
    print(sess.run(ph, feed_dict={ph: [[1, 2, 3], [4, 5, 6], [2, 3, 4]]}))
    print(sess.graph)  # <tensorflow.python.framework.ops.Graph object at 0x00000142D2830828>
    print(a.graph)     # <tensorflow.python.framework.ops.Graph object at 0x00000142D2830828>
    print(a.op)
    print(a.shape)  # ()
    print(a.name)  # Const:0

# tensorflow打印出来的形状
# 0维 ()  1维 (5)  2维 (3,4)  3维 (2,3,4)

# 静态形状和动态形状
# 静态形状：张量形状是固定的不能多次修改且不能跨维度修改
# 动态形状：改变形状生成新的张量,可以跨维度转换但是元素个数一定要匹配
# 区别：在于有没有生成新的张量,np.reshape是直接修改原数据,tf.reshape是改变原数据的形状生成新的张量
ph = tf.placeholder(dtype=tf.float32, shape=[None, 2])
print(ph)  # Tensor("Placeholder_1:0", shape=(?, 2), dtype=float32)
ph.set_shape([3, 2])
print(ph)  # Tensor("Placeholder_1:0", shape=(3, 2), dtype=float32)
ph_new = tf.reshape(ph, shape=[2, 3])
print(ph_new)  # Tensor("Reshape:0", shape=(2, 3), dtype=float32)


# 变量op
# 1、变量op可以持久化保存,张量op不可以
# 2、当定义一个变量op的时候,必须在会话当中运行初始化
a = tf.constant([1,2,3,4])
var = tf.Variable(initial_value=tf.random_normal(shape=[2, 3], mean=0, stddev=1))
print(a, var)
# 显式初始化op
init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    # 必须先运行初始化
    sess.run(init_op)
    # 把程序的图结构写入事件文件, graph:把指定的图写进事件文件当中
    filewriter = tf.summary.FileWriter("./test/", graph=sess.graph)
    print(sess.run([a, var]))






