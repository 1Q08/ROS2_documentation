.. redirect-from::

    Tutorials/Ros2bag/Recording-A-Bag-From-Your-Own-Node-Python

.. _ROS2BagOwnNodePython:

从节点录制 bag（Python）
========================

**目标：** 将你自己 Python 节点的数据录制到 bag 中。

**教程级别：** 高级

**预计用时：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``rosbag2`` 不仅仅提供 ``ros2 bag`` 命令行工具。
它还提供了一个 Python API，用于从你自己的源代码中读取和写入 bag。
这允许你订阅一个主题，并在对该数据执行任何其他处理的同时，将接收到的数据保存到 bag 中。
例如，你可以这样做，以保存来自某个主题的数据以及处理该数据的结果，而无需仅仅为了录制而通过主题发送处理后的数据。
因为任何数据都可以录制到 bag 中，所以也可以保存来自主题以外其他数据源的数据，例如用于训练集的合成数据。
例如，这对于快速生成一个包含大量样本、播放时间跨度很长的 bag 很有用。

前置条件
--------

你应该已经在常规的 ROS 2 安装中安装了 ``rosbag2`` 包。

如果你是在 Linux 上通过 deb 包安装的，它可能已默认安装。
如果没有，你可以使用以下命令安装它。

.. code-block:: console

  $ sudo apt install ros-{DISTRO}-rosbag2

本教程讨论如何使用 ROS 2 bag，包括从终端使用。
你应该已经完成了 :doc:`基础的 ROS 2 bag 教程 <../Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data>`。

任务
----

1 创建包
^^^^^^^^

打开一个新终端，并 :doc:`source 你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，使 ``ros2`` 命令能够正常工作。

按照 :ref:`这些说明 <new-directory>` 创建一个名为 ``ros2_ws`` 的新工作空间。

导航到 ``ros2_ws/src`` 目录，并创建一个新包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_python --license Apache-2.0 bag_recorder_nodes_py --dependencies rclpy rosbag2_py example_interfaces std_msgs

你的终端将返回一条消息，确认包 ``bag_recorder_nodes_py`` 及其所有必要文件和文件夹已创建。
``--dependencies`` 参数会自动将必要的依赖行添加到 ``package.xml``。
在这种情况下，该包将使用 ``rosbag2_py`` 包和 ``rclpy`` 包。
对于消息定义，还需要依赖 ``example_interfaces`` 包。

1.1 更新 ``package.xml`` 和 ``setup.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

由于你在创建包时使用了 ``--dependencies`` 选项，因此无需手动向 ``package.xml`` 添加依赖。
不过，和往常一样，请确保向 ``package.xml`` 添加描述、维护者邮箱和姓名以及许可证信息。

.. code-block:: xml

  <description>Python bag writing tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

也请确保将相同信息添加到 ``setup.py`` 文件。

.. code-block:: Python

   maintainer='Your Name',
   maintainer_email='you@email.com',
   description='Python bag writing tutorial',
   license='Apache-2.0',

2 编写 Python 节点
^^^^^^^^^^^^^^^^^^

在 ``ros2_ws/src/bag_recorder_nodes_py/bag_recorder_nodes_py`` 目录中，创建一个名为 ``simple_bag_recorder.py`` 的新文件，并将以下代码粘贴进去。

.. code-block:: Python

   import rclpy
   from rclpy.node import Node
   from rclpy.serialization import serialize_message
   from std_msgs.msg import String

   import rosbag2_py

   class SimpleBagRecorder(Node):
       def __init__(self):
           super().__init__('simple_bag_recorder')
           self.writer = rosbag2_py.SequentialWriter()

           storage_options = rosbag2_py.StorageOptions(
               uri='my_bag',
               storage_id='mcap')
           converter_options = rosbag2_py.ConverterOptions('', '')
           self.writer.open(storage_options, converter_options)

           topic_info = rosbag2_py.TopicMetadata(
               id=0,
               name='chatter',
               type='std_msgs/msg/String',
               serialization_format='cdr')
           self.writer.create_topic(topic_info)

           self.subscription = self.create_subscription(
               String,
               'chatter',
               self.topic_callback,
               10)
           self.subscription

       def topic_callback(self, msg):
           self.writer.write(
               'chatter',
               serialize_message(msg),
               self.get_clock().now().nanoseconds)


   def main(args=None):
       rclpy.init(args=args)
       sbr = SimpleBagRecorder()
       rclpy.spin(sbr)
       rclpy.shutdown()


   if __name__ == '__main__':
       main()

2.1 分析代码
~~~~~~~~~~~~

顶部的 ``import`` 语句是包依赖。
注意导入了 ``rosbag2_py`` 包，以获取处理 bag 文件所需的函数和结构。

在类构造函数中，我们首先创建将用于写入 bag 的 writer 对象。
我们正在创建一个 ``SequentialWriter``，它按消息接收的顺序将消息写入 bag。
`rosbag2 <https://github.com/ros2/rosbag2/tree/{REPOS_FILE_BRANCH}/rosbag2_cpp/include/rosbag2_cpp/writers>`__ 中可能还有其他具有不同行为的 writer。

.. code-block:: Python

   self.writer = rosbag2_py.SequentialWriter()

现在我们有了一个 writer 对象，可以用它打开 bag。
我们指定要创建的 bag 的 URI 和格式（``mcap``），其他选项保持默认值。
使用默认的转换选项，这将不执行任何转换，并以接收到的序列化格式存储消息。

.. code-block:: Python

   storage_options = rosbag2_py.StorageOptions(
       uri='my_bag',
       storage_id='mcap')
   converter_options = rosbag2_py.ConverterOptions('', '')
   self.writer.open(storage_options, converter_options)

接下来，我们需要告诉 writer 我们想要存储的主题。
这是通过创建一个 ``TopicMetadata`` 对象并将其注册到 writer 来完成的。
该对象指定主题名、主题数据类型和使用的序列化格式。

.. code-block:: Python

   topic_info = rosbag2_py.TopicMetadata(
       id=0,
       name='chatter',
       type='std_msgs/msg/String',
       serialization_format='cdr')
   self.writer.create_topic(topic_info)

现在 writer 已设置为录制我们传给它的数据，我们创建一个订阅并为其指定一个回调。
我们将在回调中将数据写入 bag。

.. code-block:: Python

   self.subscription = self.create_subscription(
       String,
       'chatter',
       self.topic_callback,
       10)
   self.subscription

回调以未序列化的形式接收消息（这是 ``rclpy`` API 的标准做法），并将消息传给 writer，同时指定该数据对应的主题以及随消息一起记录的时间戳。
然而，writer 需要序列化的消息才能存储到 bag 中。
这意味着我们需要在将数据传给 writer 之前先序列化数据。
因此，我们调用 ``serialize_message()`` 并将其结果传给 writer，而不是直接传入消息。

.. code-block:: Python

   def topic_callback(self, msg):
       self.writer.write(
           'chatter',
           serialize_message(msg),
           self.get_clock().now().nanoseconds)

文件以 ``main`` 函数结束，该函数用于创建节点的实例并启动 ROS 对其进行处理。

.. code-block:: Python

   def main(args=None):
       rclpy.init(args=args)
       sbr = SimpleBagRecorder()
       rclpy.spin(sbr)
       rclpy.shutdown()

2.2 添加入口点
~~~~~~~~~~~~~~

打开 ``bag_recorder_nodes_py`` 包中的 ``setup.py`` 文件，并为你的节点添加入口点。

.. code-block:: Python

   entry_points={
       'console_scripts': [
           'simple_bag_recorder = bag_recorder_nodes_py.simple_bag_recorder:main',
       ],
   },


3 构建并运行
^^^^^^^^^^^^

导航回工作空间的根目录 ``ros2_ws``，并构建你的新包。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes_py

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes_py

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select bag_recorder_nodes_py

打开一个新终端，导航到 ``ros2_ws``，并 source 安装文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在运行该节点：

.. code-block:: console

   $ ros2 run bag_recorder_nodes_py simple_bag_recorder

打开第二个终端，运行 ``talker`` 示例节点。

.. code-block:: console

   $ ros2 run demo_nodes_py talker

这将开始在 ``chatter`` 主题上发布数据。
当 bag 写入节点接收到这些数据时，它会将数据写入 ``my_bag`` bag。
如果 ``my_bag`` 目录已经存在，你必须先删除它，然后再运行 ``simple_bag_recorder`` 节点。
这是因为 ``rosbag2`` 默认不会覆盖已有的 bag，因此目标目录不能存在。

终止两个节点。
然后，在一个终端中启动 ``listener`` 示例节点。

.. code-block:: console

   $ ros2 run demo_nodes_py listener

在另一个终端中，使用 ``ros2 bag`` 播放你的节点录制的 bag。

.. code-block:: console

   $ ros2 bag play my_bag

你将看到来自 bag 的消息被 ``listener`` 节点接收。

如果你想再次运行 bag 写入节点，你需要先删除 ``my_bag`` 目录。

4 从节点录制合成数据
^^^^^^^^^^^^^^^^^^^^

任何数据都可以录制到 bag 中，而不仅仅是通过主题接收到的数据。
从自己的节点写入 bag 的一个常见用例是生成并存储合成数据。
在本节中，你将学习如何编写一个节点，生成一些数据并将其存储在 bag 中。
我们将演示两种实现方法。
第一种使用带定时器的节点；如果你的数据生成在节点外部（例如直接从硬件读取数据，如相机），你可以使用这种方法。
第二种方法不使用节点；当你不需要使用 ROS 基础设施的任何功能时，可以使用这种方法。

4.1 编写 Python 节点
~~~~~~~~~~~~~~~~~~~~

在 ``ros2_ws/src/bag_recorder_nodes_py/bag_recorder_nodes_py`` 目录中，创建一个名为 ``data_generator_node.py`` 的新文件，并将以下代码粘贴进去。

.. code-block:: Python

   import rclpy
   from rclpy.node import Node
   from rclpy.serialization import serialize_message
   from example_interfaces.msg import Int32

   import rosbag2_py

   class DataGeneratorNode(Node):
       def __init__(self):
           super().__init__('data_generator_node')
           self.data = Int32()
           self.data.data = 0
           self.writer = rosbag2_py.SequentialWriter()

           storage_options = rosbag2_py.StorageOptions(
               uri='timed_synthetic_bag',
               storage_id='mcap')
           converter_options = rosbag2_py.ConverterOptions('', '')
           self.writer.open(storage_options, converter_options)

           topic_info = rosbag2_py.TopicMetadata(
               id=0,
               name='synthetic',
               type='example_interfaces/msg/Int32',
               serialization_format='cdr')
           self.writer.create_topic(topic_info)

           self.timer = self.create_timer(1, self.timer_callback)

       def timer_callback(self):
           self.writer.write(
               'synthetic',
               serialize_message(self.data),
               self.get_clock().now().nanoseconds)
           self.data.data += 1


   def main(args=None):
       rclpy.init(args=args)
       dgn = DataGeneratorNode()
       rclpy.spin(dgn)
       rclpy.shutdown()


   if __name__ == '__main__':
       main()

4.2 分析代码
~~~~~~~~~~~~

这段代码的大部分与第一个示例相同。
重要的差异在此处描述。

首先，bag 的名称被更改。

.. code-block:: Python

   storage_options = rosbag2_py.StorageOptions(
       uri='timed_synthetic_bag',
       storage_id='mcap')

主题名也被更改，存储的数据类型也是如此。

.. code-block:: Python

   topic_info = rosbag2_py.TopicMetadata(
       id=0,
       name='synthetic',
       type='example_interfaces/msg/Int32',
       serialization_format='cdr')
   self.writer.create_topic(topic_info)

这个节点没有订阅主题，而是有一个定时器。
定时器以一秒为周期触发，并在触发时调用给定的成员函数。

.. code-block:: Python

   self.timer = self.create_timer(1, self.timer_callback)

在定时器回调中，我们生成（或以其他方式获取，例如从连接到某些硬件的串口读取）我们希望存储在 bag 中的数据。
与上一个示例一样，数据尚未序列化，因此我们必须先将其序列化，然后再传给 writer。

.. code-block:: Python

   self.writer.write(
       'synthetic',
       serialize_message(self.data),
       self.get_clock().now().nanoseconds)

4.3 添加可执行文件
~~~~~~~~~~~~~~~~~~

打开 ``bag_recorder_nodes_py`` 包中的 ``setup.py`` 文件，并为你的节点添加入口点。

.. code-block:: Python

   entry_points={
       'console_scripts': [
           'simple_bag_recorder = bag_recorder_nodes_py.simple_bag_recorder:main',
           'data_generator_node = bag_recorder_nodes_py.data_generator_node:main',
       ],
   },

4.4 构建并运行
~~~~~~~~~~~~~~

导航回工作空间的根目录 ``ros2_ws``，并构建你的包。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes_py

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes_py

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select bag_recorder_nodes_py

打开一个新终端，导航到 ``ros2_ws``，并 source 安装文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

如果 ``timed_synthetic_bag`` 目录已经存在，你必须先删除它，然后再运行节点。

现在运行该节点：

.. code-block:: console

   $ ros2 run bag_recorder_nodes_py data_generator_node

等待大约 30 秒，然后用 :kbd:`ctrl-c` 终止节点。
接下来，播放创建的 bag。

.. code-block:: console

   $ ros2 bag play timed_synthetic_bag

打开第二个终端，回显 ``/synthetic`` 主题。

.. code-block:: console

   $ ros2 topic echo /synthetic

你将看到生成并存储在 bag 中的数据以每秒一条消息的速率打印到控制台。

5 从可执行文件录制合成数据
^^^^^^^^^^^^^^^^^^^^^^^^^^

既然你可以创建一个 bag 来存储来自主题之外的数据源的数据，你将学习如何从一个非节点可执行文件生成和录制合成数据。
这种方法的优点是代码更简单，并且可以快速创建大量数据。

5.1 编写 Python 可执行文件
~~~~~~~~~~~~~~~~~~~~~~~~~~

在 ``ros2_ws/src/bag_recorder_nodes_py/bag_recorder_nodes_py`` 目录中，创建一个名为 ``data_generator_executable.py`` 的新文件，并将以下代码粘贴进去。

.. code-block:: Python

   from rclpy.clock import Clock
   from rclpy.duration import Duration
   from rclpy.serialization import serialize_message
   from example_interfaces.msg import Int32

   import rosbag2_py


   def main(args=None):
       writer = rosbag2_py.SequentialWriter()

       storage_options = rosbag2_py.StorageOptions(
           uri='big_synthetic_bag',
           storage_id='mcap')
       converter_options = rosbag2_py.ConverterOptions('', '')
       writer.open(storage_options, converter_options)

       topic_info = rosbag2_py.TopicMetadata(
           id=0,
           name='synthetic',
           type='example_interfaces/msg/Int32',
           serialization_format='cdr')
       writer.create_topic(topic_info)

       time_stamp = Clock().now()
       for ii in range(0, 100):
           data = Int32()
           data.data = ii
           writer.write(
               'synthetic',
               serialize_message(data),
               time_stamp.nanoseconds)
           time_stamp += Duration(seconds=1)

   if __name__ == '__main__':
       main()

5.2 分析代码
~~~~~~~~~~~~

将本示例与上一个示例进行比较就会发现，它们并没有太大区别。
唯一显著的差异是使用 for 循环而不是定时器来驱动数据生成。

请注意，我们现在还为数据生成时间戳，而不是为每个样本依赖当前系统时间。
时间戳可以是你需要的任何值。
数据将以这些时间戳给出的速率播放，因此这是控制样本默认播放速度的有用方法。
还要注意，虽然每个样本之间的间隔在时间上是完整的一秒，但这个可执行文件不需要在每个样本之间等待一秒。
这使我们能够在比播放所需时间短得多的时间内，生成覆盖大范围时间的大量数据。

.. code-block:: Python

   time_stamp = Clock().now()
   for ii in range(0, 100):
       data = Int32()
       data.data = ii
       writer.write(
           'synthetic',
           serialize_message(data),
           time_stamp.nanoseconds)
       time_stamp += Duration(seconds=1)

5.3 添加可执行文件
~~~~~~~~~~~~~~~~~~

打开 ``bag_recorder_nodes_py`` 包中的 ``setup.py`` 文件，并为你的节点添加入口点。

.. code-block:: Python

   entry_points={
       'console_scripts': [
           'simple_bag_recorder = bag_recorder_nodes_py.simple_bag_recorder:main',
           'data_generator_node = bag_recorder_nodes_py.data_generator_node:main',
           'data_generator_executable = bag_recorder_nodes_py.data_generator_executable:main',
       ],
   },

5.4 构建并运行
~~~~~~~~~~~~~~

导航回工作空间的根目录 ``ros2_ws``，并构建你的包。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes_py

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes_py

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select bag_recorder_nodes_py

打开一个终端，导航到 ``ros2_ws``，并 source 安装文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

如果 ``big_synthetic_bag`` 目录已经存在，你必须先删除它，然后再运行可执行文件。

现在运行该可执行文件：

.. code-block:: console

   $ ros2 run bag_recorder_nodes_py data_generator_executable

请注意，该可执行文件运行并非常快速地完成。

现在播放创建的 bag。

.. code-block:: console

   $ ros2 bag play big_synthetic_bag

打开第二个终端，回显 ``/synthetic`` 主题。

.. code-block:: console

   $ ros2 topic echo /synthetic

你将看到生成并存储在 bag 中的数据以每秒一条消息的速率打印到控制台。
即使 bag 是快速生成的，它仍然以时间戳指示的速率播放。

总结
----

你创建了一个节点，将它在主题上接收到的数据录制到 bag 中。
你测试了使用该节点录制 bag，并通过播放 bag 验证了数据已被录制。
这种方法可以用于录制一个 bag，其中包含比通过主题接收到的更多的数据，例如处理接收到的数据所获得的结果。
然后，你继续创建了一个节点和一个可执行文件来生成合成数据并将其存储在 bag 中。
后一种方法尤其适用于生成合成数据，例如可以作为训练集使用的合成数据。
