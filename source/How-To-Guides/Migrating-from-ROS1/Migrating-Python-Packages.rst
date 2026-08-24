.. redirect-from::

   Migration-Guide-Python
   The-ROS2-Project/Contributing/Migration-Guide-Python

迁移 Python 包参考
==================

本页是关于如何将 Python 包从 ROS 1 迁移到 ROS 2 的参考。
如果这是你第一次迁移 Python 包，请先遵循 :doc:`本指南迁移一个示例 Python 包 <./Migrating-Python-Package-Example>`。

.. contents:: 目录
   :depth: 2
   :local:

构建工具
--------

ROS 2 不再使用 ``catkin_make``、``catkin_make_isolated`` 或 ``catkin build``，而是使用命令行工具 `colcon <https://design.ros2.org/articles/build_tool.html>`__ 来构建和安装一组包。
请参见 :doc:`初学者教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>` 以开始使用 ``colcon``。

构建系统
--------

对于纯 Python 包，ROS 2 使用 Python 开发者所熟悉的标准 ``setup.py`` 安装机制。

更新文件以使用 *setup.py*
^^^^^^^^^^^^^^^^^^^^^^^^^

如果 ROS 1 包仅使用 CMake 来调用 ``setup.py`` 文件，并且除 Python 代码外不包含其他内容（例如没有消息、服务等），则应将其转换为 ROS 2 中的纯 Python 包：

*
  在 ``package.xml`` 文件中更新或添加构建类型：

  .. code-block:: xml

     <export>
       <build_type>ament_python</build_type>
     </export>

*
  删除 ``CMakeLists.txt`` 文件

*
  将 ``setup.py`` 文件更新为标准的 Python 设置脚本

ROS 2 仅支持 Python 3。
虽然每个包都可以选择同时支持 Python 2，但如果它使用了其他 ROS 2 包提供的任何 API，则必须使用 Python 3 来调用可执行文件。

更新源代码
----------

节点初始化
^^^^^^^^^^

在 ROS 1 中：

.. code-block:: python

   rospy.init_node('asdf')

   rospy.loginfo('Created node')

在 ROS 2 中：

.. code-block:: python

   rclpy.init(args=sys.argv)
   node = rclpy.create_node('asdf')

   node.get_logger().info('Created node')

ROS 参数
^^^^^^^^

在 ROS 1 中：

.. code-block:: python

   port = rospy.get_param('port', '/dev/ttyUSB0')
   assert isinstance(port, str), 'port parameter must be a str'

   baudrate = rospy.get_param('baudrate', 115200)
   assert isinstance(baudrate, int), 'baudrate parameter must be an integer'

  rospy.logwarn('port: ' + port)

在 ROS 2 中：

.. code-block:: python

   port = node.declare_parameter('port', '/dev/ttyUSB0').value
   assert isinstance(port, str), 'port parameter must be a str'

   baudrate = node.declare_parameter('baudrate', 115200).value
   assert isinstance(baudrate, int), 'baudrate parameter must be an integer'

   node.get_logger().warn('port: ' + port)

创建发布者
^^^^^^^^^^

在 ROS 1 中：

.. code-block:: python

   pub = rospy.Publisher('chatter', String)
   # 或者
   pub = rospy.Publisher('chatter', String, queue_size=10)

在 ROS 2 中：

.. code-block:: python

   pub = node.create_publisher(String, 'chatter', rclpy.qos.QoSProfile())
   # 或者
   pub = node.create_publisher(String, 'chatter', 10)

创建订阅者
^^^^^^^^^^

在 ROS 1 中：

.. code-block:: python

   sub = rospy.Subscriber('chatter', String, callback)
   # 或者
   sub = rospy.Subscriber('chatter', String, callback, queue_size=10)

在 ROS 2 中：

.. code-block:: python

   sub = node.create_subscription(String, 'chatter', callback, rclpy.qos.QoSProfile())
   # 或者
   sub = node.create_subscription(String, 'chatter', callback, 10)

创建服务
^^^^^^^^

在 ROS 1 中：

.. code-block:: python

   srv = rospy.Service('add_two_ints', AddTwoInts, add_two_ints_callback)

在 ROS 2 中：

.. code-block:: python

   srv = node.create_service(AddTwoInts, 'add_two_ints', add_two_ints_callback)

创建服务客户端
^^^^^^^^^^^^^^

在 ROS 1 中：

.. code-block:: python

   rospy.wait_for_service('add_two_ints')
   add_two_ints = rospy.ServiceProxy('add_two_ints', AddTwoInts)
   resp = add_two_ints(req)

在 ROS 2 中：

.. code-block:: python

   add_two_ints = node.create_client(AddTwoInts, 'add_two_ints')
   while not add_two_ints.wait_for_service(timeout_sec=1.0):
       node.get_logger().info('service not available, waiting again...')
   resp = add_two_ints.call_async(req)
   rclpy.spin_until_future_complete(node, resp)

.. warning::

   不要在 ROS 2 回调中使用 ``rclpy.spin_until_future_complete``。
   更多详细信息请参见 :doc:`同步死锁文章 <../Sync-Vs-Async>`。
