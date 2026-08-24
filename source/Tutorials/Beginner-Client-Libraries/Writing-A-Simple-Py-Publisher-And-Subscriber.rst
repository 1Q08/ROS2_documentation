.. redirect-from::

    Tutorials/Writing-A-Simple-Py-Publisher-And-Subscriber

.. _PyPubSub:

编写一个简单的发布者和订阅者（Python）
======================================

**目标：** 使用 Python 创建并运行发布者和订阅者节点。

**教程级别：** 初级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在本教程中，你将创建 :doc:`节点 <../Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>`，这些节点通过 :doc:`话题 <../Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics>` 以字符串消息的形式相互传递信息。
这里使用的例子是一个简单的“说者”（talker）和“听者”（listener）系统；
一个节点发布数据，另一个节点订阅话题以接收该数据。

这些例子中使用的代码可以在 `这里 <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclpy/topics>`__ 找到。

前置条件
--------

在前面的教程中，你学习了如何 :doc:`创建工作空间 <./Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <./Creating-Your-First-ROS2-Package>`。

建议你对 Python 有基本的了解，但不是完全必需。

任务
----

1 创建一个包
^^^^^^^^^^^^

打开一个新终端，并 :doc:`source 你的 ROS 2 安装环境 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，这样 ``ros2`` 命令才能正常工作。

进入在 :ref:`之前的教程 <new-directory>` 中创建的 ``ros2_ws`` 目录。

请记住，包应该在 ``src`` 目录中创建，而不是在工作空间的根目录。
因此，进入 ``ros2_ws/src``，然后运行包创建命令：

.. code-block:: console

  $ ros2 pkg create --build-type ament_python --license Apache-2.0 py_pubsub

你的终端将返回一条消息，验证你的包 ``py_pubsub`` 及其所有必要的文件和文件夹已创建。

2 编写发布者节点
^^^^^^^^^^^^^^^^

进入 ``ros2_ws/src/py_pubsub/py_pubsub``。
请记住，这个目录是一个 `Python 包 <https://docs.python.org/3/tutorial/modules.html#packages>`__，与它嵌套所在的 ROS 2 包同名。

通过输入以下命令下载示例 talker 代码：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ wget https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py

   .. group-tab:: macOS

      .. code-block:: console

        $ wget https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py

   .. group-tab:: Windows

      在 Windows 命令行提示符中：

      .. code-block:: console

            $ curl -sk https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py -o publisher_member_function.py

      或在 powershell 中：

      .. code-block:: console

            $ curl https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py -o publisher_member_function.py

现在会有一个名为 ``publisher_member_function.py`` 的新文件，与 ``__init__.py`` 相邻。

使用你喜欢的文本编辑器打开该文件。

.. code-block:: python

  import rclpy
  from rclpy.node import Node

  from std_msgs.msg import String


  class MinimalPublisher(Node):

      def __init__(self):
          super().__init__('minimal_publisher')
          self.publisher_ = self.create_publisher(String, 'topic', 10)
          timer_period = 0.5  # seconds
          self.timer = self.create_timer(timer_period, self.timer_callback)
          self.i = 0

      def timer_callback(self):
          msg = String()
          msg.data = 'Hello World: %d' % self.i
          self.publisher_.publish(msg)
          self.get_logger().info('Publishing: "%s"' % msg.data)
          self.i += 1


  def main(args=None):
      rclpy.init(args=args)

      minimal_publisher = MinimalPublisher()

      rclpy.spin(minimal_publisher)

      # Destroy the node explicitly
      # (optional - otherwise it will be done automatically
      # when the garbage collector destroys the node object)
      minimal_publisher.destroy_node()
      rclpy.shutdown()


  if __name__ == '__main__':
      main()


2.1 检查代码
~~~~~~~~~~~~

注释之后的前几行代码导入了 {package(rclpy)}，这样它的 `Node <{package_link(rclpy)}api/node.html>`__ 类就可以被使用。

.. code-block:: python

  import rclpy
  from rclpy.node import Node

下一条语句导入了内置的 {interface(std_msgs/msg/String)} 消息类型，节点用它在话题上传递的数据的结构。

.. code-block:: python

  from std_msgs.msg import String

这几行代码代表了节点的依赖。
请记住，依赖必须添加到 ``package.xml`` 中，你将在下一节完成这一步。

接下来，创建 ``MinimalPublisher`` 类，它继承自（或者是子类）`Node <{package_link(rclpy)}api/node.html>`__。

.. code-block:: python

  class MinimalPublisher(Node):

下面是类构造函数的定义。
``super().__init__`` 调用 `Node <{package_link(rclpy)}api/node.html>`__ 类的构造函数，并传入你的节点名，在本例中是 ``minimal_publisher``。

`create_publisher <{package_link(rclpy)}api/node.html#rclpy.node.Node.create_publisher>`__ 声明该节点在一个名为 ``topic`` 的话题上发布 {interface(std_msgs/msg/String)} 类型的消息（从 ``std_msgs.msg`` 模块导入），并且“队列大小”为 10。
队列大小是一个必需的 :doc:`服务质量 </Concepts/Intermediate/About-Quality-of-Service-Settings>` （QoS）设置，当订阅者接收消息不够快时，它会限制排队的消息数量。

接下来，使用 `create_timer <{package_link(rclpy)}api/node.html#rclpy.node.Node.create_timer>`__ 创建一个每 0.5 秒执行一次的回调。
``self.i`` 是在回调中使用的计数器。

.. code-block:: python

  def __init__(self):
      super().__init__('minimal_publisher')
      self.publisher_ = self.create_publisher(String, 'topic', 10)
      timer_period = 0.5  # seconds
      self.timer = self.create_timer(timer_period, self.timer_callback)
      self.i = 0

``timer_callback`` 创建一条追加了计数器值的消息，发布它，并用 `get_logger() <{package_link(rclpy)}api/node.html#rclpy.node.Node.get_logger>`__ 的 `info() <{package_link(rclpy)}rclpy.impl.rcutils_logger.html#rclpy.impl.rcutils_logger.RcutilsLogger.info>`__ 函数将其打印到控制台。

.. code-block:: python

  def timer_callback(self):
      msg = String()
      msg.data = 'Hello World: %d' % self.i
      self.publisher_.publish(msg)
      self.get_logger().info('Publishing: "%s"' % msg.data)
      self.i += 1

最后，定义 main 函数。

.. code-block:: python

  def main(args=None):
      rclpy.init(args=args)

      minimal_publisher = MinimalPublisher()

      rclpy.spin(minimal_publisher)

      # Destroy the node explicitly
      # (optional - otherwise it will be done automatically
      # when the garbage collector destroys the node object)
      minimal_publisher.destroy_node()
      rclpy.shutdown()

首先初始化 {package(rclpy)} 库，然后创建节点，再让它“spin”节点（使用 `spin() <{package_link(rclpy)}api/init_shutdown.html#rclpy.spin>`__），这样它的回调才会被调用。

2.2 添加依赖
~~~~~~~~~~~~

返回上一级，进入 ``ros2_ws/src/py_pubsub`` 目录，那里已经为你创建了 ``setup.py``、``setup.cfg`` 和 ``package.xml`` 文件。

用你的文本编辑器打开 ``package.xml``。

如 :doc:`上一个教程 <./Creating-Your-First-ROS2-Package>` 中所述，请确保填写 ``<description>``、``<maintainer>`` 和 ``<license>`` 标签：

.. code-block:: xml

  <description>Examples of minimal publisher/subscriber using rclpy</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

在上述几行之后，添加与节点导入语句对应的以下依赖：

.. code-block:: xml

  <exec_depend>rclpy</exec_depend>
  <exec_depend>std_msgs</exec_depend>

这声明了当包代码被执行时需要 {package(rclpy)} 和 {package(std_msgs)}。

请确保保存文件。

2.3 添加入口点
~~~~~~~~~~~~~~

打开 ``setup.py`` 文件。
同样，将 ``maintainer``、``maintainer_email``、``description`` 和 ``license`` 字段与你的 ``package.xml`` 保持一致：

.. code-block:: python

  maintainer='YourName',
  maintainer_email='you@email.com',
  description='Examples of minimal publisher/subscriber using rclpy',
  license='Apache-2.0',

在 `entry_points <https://setuptools.pypa.io/en/latest/userguide/entry_point.html>`__ 字段的 ``console_scripts`` 方括号内添加以下行：

.. code-block:: python

  entry_points={
          'console_scripts': [
                  'talker = py_pubsub.publisher_member_function:main',
          ],
  },

不要忘记保存。

2.4 检查 setup.cfg
~~~~~~~~~~~~~~~~~~

``setup.cfg`` 文件的内容应该已经自动正确填充，如下所示：

.. code-block:: ini

  [develop]
  script_dir=$base/lib/py_pubsub
  [install]
  install_scripts=$base/lib/py_pubsub

这只是告诉 `setuptools <https://setuptools.pypa.io/en/latest/userguide>`__ 将你的可执行文件放在 ``lib`` 中，因为 ``ros2 run`` 会在那里查找它们。

你现在就可以构建你的包，source 本地安装文件并运行它，但让我们先创建订阅者节点，这样你就能看到整个系统的运行情况。

3 编写订阅者节点
^^^^^^^^^^^^^^^^

返回 ``ros2_ws/src/py_pubsub/py_pubsub`` 以创建下一个节点。
在终端中输入以下代码：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ wget https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py

   .. group-tab:: macOS

      .. code-block:: console

        $ wget https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py

   .. group-tab:: Windows

      在 Windows 命令行提示符中：

      .. code-block:: console

            $ curl -sk https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py -o subscriber_member_function.py

      或在 powershell 中：

      .. code-block:: console

            $ curl https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py -o subscriber_member_function.py

现在这个目录应该有这些文件：

.. code-block:: console

  __init__.py  publisher_member_function.py  subscriber_member_function.py

3.1 检查代码
~~~~~~~~~~~~

用你的文本编辑器打开 ``subscriber_member_function.py``。

.. code-block:: python

  import rclpy
  from rclpy.node import Node

  from std_msgs.msg import String


  class MinimalSubscriber(Node):

      def __init__(self):
          super().__init__('minimal_subscriber')
          self.subscription = self.create_subscription(
              String,
              'topic',
              self.listener_callback,
              10)
          self.subscription  # prevent unused variable warning

      def listener_callback(self, msg):
          self.get_logger().info('I heard: "%s"' % msg.data)


  def main(args=None):
      rclpy.init(args=args)

      minimal_subscriber = MinimalSubscriber()

      rclpy.spin(minimal_subscriber)

      # Destroy the node explicitly
      # (optional - otherwise it will be done automatically
      # when the garbage collector destroys the node object)
      minimal_subscriber.destroy_node()
      rclpy.shutdown()


  if __name__ == '__main__':
      main()

订阅者节点的代码几乎与发布者的相同。
构造函数使用与发布者相同的参数，通过 `create_subscription <{package_link(rclpy)}api/node.html#rclpy.node.Node.create_subscription>`__ 创建了一个订阅者。
回想一下 :doc:`话题教程 <../Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics>`，发布者和订阅者使用的话题名和消息类型必须匹配，才能让它们进行通信。

.. code-block:: python

  self.subscription = self.create_subscription(
      String,
      'topic',
      self.listener_callback,
      10)

订阅者的构造函数和回调不包含任何定时器定义，因为它不需要。
一旦收到消息，它的回调就会被调用。

回调的定义只是向控制台打印一条信息消息，以及它接收到的数据。
回想一下发布者定义的是 ``msg.data = 'Hello World: %d' % self.i``

.. code-block:: python

  def listener_callback(self, msg):
      self.get_logger().info('I heard: "%s"' % msg.data)

``main`` 的定义几乎完全相同，只是将发布者的创建和 spin 替换成了订阅者的。

.. code-block:: python

  minimal_subscriber = MinimalSubscriber()

  rclpy.spin(minimal_subscriber)

由于该节点与发布者具有相同的依赖，所以不需要向 ``package.xml`` 添加任何新内容。
``setup.cfg`` 文件也可以保持不变。


3.2 添加入口点
~~~~~~~~~~~~~~

重新打开 ``setup.py``，在发布者入口点的下方添加订阅者节点的入口点。
`entry_points <https://setuptools.pypa.io/en/latest/userguide/entry_point.html>`__ 字段现在应该看起来像这样：

.. code-block:: python

  entry_points={
          'console_scripts': [
                  'talker = py_pubsub.publisher_member_function:main',
                  'listener = py_pubsub.subscriber_member_function:main',
          ],
  },

请确保保存文件，然后你的发布/订阅系统就应该准备好了。

4 构建并运行
^^^^^^^^^^^^
你可能已经在 ROS 2 系统中安装了 {package(rclpy)} 和 {package(std_msgs)} 包。
在构建之前，最好在工作空间的根目录（``ros2_ws``）运行 `rosdep <https://docs.ros.org/en/independent/api/rosdep/html/>`__\ （查看 :doc:`rosdep 教程 </Tutorials/Intermediate/Rosdep>`\ ）来检查缺失的依赖：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

   .. group-tab:: Windows

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。


仍然在工作空间的根目录 ``ros2_ws``，构建你的新包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select py_pubsub

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select py_pubsub

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select py_pubsub

打开一个新终端，进入 ``ros2_ws``，然后 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在运行 talker 节点。
终端应该每 0.5 秒开始发布一条 info 消息，如下所示：

.. code-block:: console

  $ ros2 run py_pubsub talker
  [info] [minimal_publisher]: publishing: "hello world: 0"
  [info] [minimal_publisher]: publishing: "hello world: 1"
  [info] [minimal_publisher]: publishing: "hello world: 2"
  [info] [minimal_publisher]: publishing: "hello world: 3"
  [info] [minimal_publisher]: publishing: "hello world: 4"
  ...

打开另一个终端，再次从 ``ros2_ws`` 内 source 安装文件，然后启动 listener 节点。
listener 将开始向控制台打印消息，从发布者当时所在的任意消息计数开始，如下所示：

.. code-block:: console

  $ ros2 run py_pubsub listener
  [INFO] [minimal_subscriber]: I heard: "Hello World: 10"
  [INFO] [minimal_subscriber]: I heard: "Hello World: 11"
  [INFO] [minimal_subscriber]: I heard: "Hello World: 12"
  [INFO] [minimal_subscriber]: I heard: "Hello World: 13"
  [INFO] [minimal_subscriber]: I heard: "Hello World: 14"

在每个终端中输入 ``Ctrl+C`` 来停止节点的 spin。

总结
----

你创建了两个节点，通过话题发布和订阅数据。
在运行它们之前，你将它们的依赖和入口点添加到了包配置文件中。

后续步骤
--------

接下来，你将使用服务/客户端模型创建另一个简单的 ROS 2 包。
同样，你可以选择用 :doc:`C++ <./Writing-A-Simple-Cpp-Service-And-Client>` 或 :doc:`Python <./Writing-A-Simple-Py-Service-And-Client>` 来编写它。

相关内容
--------

在 Python 中有多种方式可以编写发布者和订阅者；请查看 `ros2/examples <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclpy/topics>`_ 仓库中的 ``minimal_publisher`` 和 ``minimal_subscriber`` 包。
