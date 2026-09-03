.. redirect-from::

    Tutorials/Writing-A-Simple-Py-Service-And-Client

.. _PySrvCli:

编写一个简单的服务和客户端（Python）
====================================

**目标：** 使用 Python 创建并运行服务和客户端节点。

**教程级别：** 初级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

当 :doc:`节点 <../Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>` 使用 :doc:`服务 <../Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services>` 进行通信时，发送数据请求的节点称为客户端节点，响应请求的节点称为服务节点。
请求和响应的结构由 ``.srv`` 文件确定。

这里使用的例子是一个简单的整数加法系统；一个节点请求两个整数之和，另一个节点以结果作为响应。

前置条件
--------

在前面的教程中，你学习了如何 :doc:`创建工作空间 <./Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <./Creating-Your-First-ROS2-Package>`。

任务
----

1 创建一个包
^^^^^^^^^^^^

打开一个新终端，并 :doc:`source 你的 ROS 2 安装环境 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，这样 ``ros2`` 命令才能正常工作。

进入在 :ref:`之前的教程 <new-directory>` 中创建的 ``ros2_ws`` 目录。

请记住，包应该在 ``src`` 目录中创建，而不是在工作空间的根目录。
进入 ``ros2_ws/src`` 并创建一个新包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_python --license Apache-2.0 py_srvcli --dependencies rclpy example_interfaces

你的终端将返回一条消息，验证你的包 ``py_srvcli`` 及其所有必要的文件和文件夹已创建。

``--dependencies`` 参数会自动将必要的依赖行添加到 ``package.xml``。
``example_interfaces`` 是包含 `你构建请求和响应所需的 .srv 文件 <https://github.com/ros2/example_interfaces/blob/{REPOS_FILE_BRANCH}/srv/AddTwoInts.srv>`__ 的包：

.. code-block:: bash

    int64 a
    int64 b
    ---
    int64 sum

前两行是请求的参数，横线下方是响应。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

因为你在创建包时使用了 ``--dependencies`` 选项，所以不需要手动向 ``package.xml`` 添加依赖。

不过，一如既往地，请确保将描述、维护者邮箱和姓名以及许可证信息添加到 ``package.xml``。

.. code-block:: xml

  <description>Python client server tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

1.2 更新 ``setup.py``
~~~~~~~~~~~~~~~~~~~~~

将相同的信息添加到 ``setup.py`` 文件的 ``maintainer``、``maintainer_email``、``description`` 和 ``license`` 字段中：

.. code-block:: python

    maintainer='Your Name',
    maintainer_email='you@email.com',
    description='Python client server tutorial',
    license='Apache-2.0',

2 编写服务节点
^^^^^^^^^^^^^^

在 ``ros2_ws/src/py_srvcli/py_srvcli`` 目录中，创建一个名为 ``service_member_function.py`` 的新文件，并在其中粘贴以下代码：

.. code-block:: python

  from example_interfaces.srv import AddTwoInts

  import rclpy
  from rclpy.node import Node


  class MinimalService(Node):

      def __init__(self):
          super().__init__('minimal_service')
          self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

      def add_two_ints_callback(self, request, response):
          response.sum = request.a + request.b
          self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

          return response


  def main():
      rclpy.init()

      minimal_service = MinimalService()

      rclpy.spin(minimal_service)

      rclpy.shutdown()


  if __name__ == '__main__':
      main()

2.1 检查代码
~~~~~~~~~~~~

第一条 ``import`` 语句从 ``example_interfaces`` 包中导入了 ``AddTwoInts`` 服务类型。
后面的 ``import`` 语句导入了 ROS 2 Python 客户端库，特别是 ``Node`` 类。

.. code-block:: python

  from example_interfaces.srv import AddTwoInts

  import rclpy
  from rclpy.node import Node

``MinimalService`` 类的构造函数用名称 ``minimal_service`` 初始化节点。
然后，它创建一个服务并定义类型、名称和回调。

.. code-block:: python

  def __init__(self):
      super().__init__('minimal_service')
      self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

服务回调的定义接收请求数据，对它求和，并将结果作为响应返回。

.. code-block:: python

  def add_two_ints_callback(self, request, response):
      response.sum = request.a + request.b
      self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

      return response

最后，主类初始化 ROS 2 Python 客户端库，实例化 ``MinimalService`` 类来创建服务节点，并 spin 节点以处理回调。

2.2 添加入口点
~~~~~~~~~~~~~~

为了让 ``ros2 run`` 命令能够运行你的节点，你必须将入口点添加到 ``setup.py``\ （位于 ``ros2_ws/src/py_srvcli`` 目录中）。

在 ``'console_scripts':`` 方括号之间添加以下行：

.. code-block:: python

  'service = py_srvcli.service_member_function:main',

3 编写客户端节点
^^^^^^^^^^^^^^^^

在 ``ros2_ws/src/py_srvcli/py_srvcli`` 目录中，创建一个名为 ``client_member_function.py`` 的新文件，并在其中粘贴以下代码：

.. code-block:: python

  import sys

  from example_interfaces.srv import AddTwoInts
  import rclpy
  from rclpy.node import Node


  class MinimalClientAsync(Node):

      def __init__(self):
          super().__init__('minimal_client_async')
          self.cli = self.create_client(AddTwoInts, 'add_two_ints')
          while not self.cli.wait_for_service(timeout_sec=1.0):
              self.get_logger().info('service not available, waiting again...')
          self.req = AddTwoInts.Request()

      def send_request(self, a, b):
          self.req.a = a
          self.req.b = b
          return self.cli.call_async(self.req)


  def main():
      rclpy.init()

      minimal_client = MinimalClientAsync()
      future = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
      rclpy.spin_until_future_complete(minimal_client, future)
      response = future.result()
      minimal_client.get_logger().info(
          'Result of add_two_ints: for %d + %d = %d' %
          (int(sys.argv[1]), int(sys.argv[2]), response.sum))

      minimal_client.destroy_node()
      rclpy.shutdown()


  if __name__ == '__main__':
      main()


3.1 检查代码
~~~~~~~~~~~~

与服务代码一样，我们首先 ``import`` 必要的库。

.. code-block:: python

  import sys

  from example_interfaces.srv import AddTwoInts
  import rclpy
  from rclpy.node import Node

``MinimalClientAsync`` 类的构造函数用名称 ``minimal_client_async`` 初始化节点。
构造函数的定义创建了一个与服务节点类型和名称相同的客户端。
客户端和服务要能够通信，类型和名称必须匹配。
构造函数中的 ``while`` 循环每秒检查一次是否有与客户端类型和名称匹配的服务可用。
最后它创建一个新的 ``AddTwoInts`` 请求对象。

.. code-block:: python

  def __init__(self):
      super().__init__('minimal_client_async')
      self.cli = self.create_client(AddTwoInts, 'add_two_ints')
      while not self.cli.wait_for_service(timeout_sec=1.0):
          self.get_logger().info('service not available, waiting again...')
      self.req = AddTwoInts.Request()

构造函数下面是 ``send_request`` 方法，它发送请求并 spin，直到收到响应或失败。

.. code-block:: python

  def send_request(self, a, b):
      self.req.a = a
      self.req.b = b
      return self.cli.call_async(self.req)

最后是 ``main`` 方法，它构造一个 ``MinimalClientAsync`` 对象，使用传入的命令行参数发送请求，调用 ``rclpy.spin_until_future_complete`` 等待结果，并记录结果。

.. code-block:: python

  def main():
      rclpy.init()

      minimal_client = MinimalClientAsync()
      future = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
      rclpy.spin_until_future_complete(minimal_client, future)
      response = future.result()
      minimal_client.get_logger().info(
          'Result of add_two_ints: for %d + %d = %d' %
          (int(sys.argv[1]), int(sys.argv[2]), response.sum))

      minimal_client.destroy_node()
      rclpy.shutdown()

.. warning::

  不要在 ROS 2 回调中使用 ``rclpy.spin_until_future_complete``。
  更多细节请参阅 :doc:`同步死锁文章 <../../../How-To-Guides/Sync-Vs-Async>`。

3.2 添加入口点
~~~~~~~~~~~~~~

与服务节点一样，你还必须添加入口点才能运行客户端节点。

你的 ``setup.py`` 文件的 ``entry_points`` 字段应该看起来像这样：

.. code-block:: python

  entry_points={
      'console_scripts': [
          'service = py_srvcli.service_member_function:main',
          'client = py_srvcli.client_member_function:main',
      ],
  },

4 构建并运行
^^^^^^^^^^^^

在构建之前，最好在工作空间的根目录（``ros2_ws``）运行 ``rosdep`` 来检查缺失的依赖：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

            $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

   .. group-tab:: Windows

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。


返回到工作空间的根目录 ``ros2_ws``，并构建你的新包：

.. code-block:: console

  $ colcon build --packages-select py_srvcli

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

现在运行服务节点：

.. code-block:: console

  $ ros2 run py_srvcli service

节点将等待客户端的请求。

打开另一个终端，再次从 ``ros2_ws`` 内 source 安装文件。
启动客户端节点，后面跟上任意两个以空格分隔的整数。
例如，如果你选择 ``2`` 和 ``3``，客户端会收到这样的响应：

.. code-block:: console

  $ ros2 run py_srvcli client 2 3
  [INFO] [minimal_client_async]: Result of add_two_ints: for 2 + 3 = 5

返回到服务节点正在运行的终端。
你会看到它在收到请求时发布了日志消息：

.. code-block:: console

  [INFO] [minimal_service]: Incoming request
  a: 2 b: 3

在服务终端中输入 ``Ctrl+C`` 来停止节点的 spin。


总结
----

你创建了两个节点，通过服务请求和响应数据。
你将它们的依赖和可执行文件添加到了包配置文件中，这样你就可以构建并运行它们，看到服务/客户端系统的实际运行。

后续步骤
--------

在最后几个教程中，你一直在利用接口通过话题和服务传递数据。
接下来，你将学习如何 :doc:`创建自定义接口 <./Custom-ROS2-Interfaces>`。

相关内容
--------

* 在 Python 中有多种方式可以编写服务和客户端；请查看 `ros2/examples <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclpy/services>`_ 仓库中的 ``minimal_client`` 和 ``minimal_service`` 包。

* 在本教程中，你在客户端节点中使用了 ``call_async()`` API 来调用服务。
  还有一种可用于 Python 的服务调用 API，称为同步调用。
  我们不建议使用同步调用，但如果你想了解更多，请阅读 :doc:`同步 vs 异步客户端 <../../How-To-Guides/Sync-Vs-Async>` 指南。
