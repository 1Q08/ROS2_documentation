.. redirect-from::

    Tutorials/Tf2/Writing-A-Tf2-Listener-Py

编写监听器（Python）
====================

**目标：** 学习如何使用 tf2 获取帧变换。

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在之前的教程中，我们创建了一个 tf2 广播器，将 turtle 的位姿发布到 tf2。

在本教程中，我们将创建一个 tf2 监听器来开始使用 tf2。

先决条件
--------

本教程假设你已经完成 :doc:`tf2 静态广播器教程（Python） <./Writing-A-Tf2-Static-Broadcaster-Py>` 和 :doc:`tf2 广播器教程（Python） <./Writing-A-Tf2-Broadcaster-Py>`。
在上一教程中，我们创建了一个 ``learning_tf2_py`` 包，我们将继续在该包的基础上工作。

任务
----

1 编写监听器节点
^^^^^^^^^^^^^^^^

让我们先创建源文件。
转到我们在上一个教程中创建的 ``learning_tf2_py`` 包。
在 ``src/learning_tf2_py/learning_tf2_py`` 目录中，通过输入以下命令下载示例监听器代码：

.. tabs::

    .. group-tab:: Linux

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_listener.py

    .. group-tab:: macOS

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_listener.py

    .. group-tab:: Windows

        在 Windows 命令行提示符中：

        .. code-block:: console

            $ curl -sk https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_listener.py -o turtle_tf2_listener.py

        或者在 powershell 中：

        .. code-block:: console

           $ curl https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_listener.py -o turtle_tf2_listener.py

现在使用你喜欢的文本编辑器打开名为 ``turtle_tf2_listener.py`` 的文件。

.. code-block:: python

    import math

    from geometry_msgs.msg import Twist

    import rclpy
    from rclpy.node import Node

    from tf2_ros import TransformException
    from tf2_ros.buffer import Buffer
    from tf2_ros.transform_listener import TransformListener

    from turtlesim.srv import Spawn


    class FrameListener(Node):

        def __init__(self):
            super().__init__('turtle_tf2_frame_listener')

            # Declare and acquire `target_frame` parameter
            self.target_frame = self.declare_parameter(
              'target_frame', 'turtle1').get_parameter_value().string_value

            self.tf_buffer = Buffer()
            self.tf_listener = TransformListener(self.tf_buffer, self)

            # Create a client to spawn a turtle
            self.spawner = self.create_client(Spawn, 'spawn')
            # Boolean values to store the information
            # if the service for spawning turtle is available
            self.turtle_spawning_service_ready = False
            # if the turtle was successfully spawned
            self.turtle_spawned = False

            # Create turtle2 velocity publisher
            self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)

            # Call on_timer function every second
            self.timer = self.create_timer(1.0, self.on_timer)

        def on_timer(self):
            # Store frame names in variables that will be used to
            # compute transformations
            from_frame_rel = self.target_frame
            to_frame_rel = 'turtle2'

            if self.turtle_spawning_service_ready:
                if self.turtle_spawned:
                    # Look up for the transformation between target_frame and turtle2 frames
                    # and send velocity commands for turtle2 to reach target_frame
                    try:
                        t = self.tf_buffer.lookup_transform(
                            to_frame_rel,
                            from_frame_rel,
                            rclpy.time.Time())
                    except TransformException as ex:
                        self.get_logger().info(
                            f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
                        return

                    msg = Twist()
                    scale_rotation_rate = 1.0
                    msg.angular.z = scale_rotation_rate * math.atan2(
                        t.transform.translation.y,
                        t.transform.translation.x)

                    scale_forward_speed = 0.5
                    msg.linear.x = scale_forward_speed * math.sqrt(
                        t.transform.translation.x ** 2 +
                        t.transform.translation.y ** 2)

                    self.publisher.publish(msg)
                else:
                    if self.result.done():
                        self.get_logger().info(
                            f'Successfully spawned {self.result.result().name}')
                        self.turtle_spawned = True
                    else:
                        self.get_logger().info('Spawn is not finished')
            else:
                if self.spawner.service_is_ready():
                    # Initialize request with turtle name and coordinates
                    # Note that x, y and theta are defined as floats in turtlesim/srv/Spawn
                    request = Spawn.Request()
                    request.name = 'turtle2'
                    request.x = float(4)
                    request.y = float(2)
                    request.theta = float(0)
                    # Call request
                    self.result = self.spawner.call_async(request)
                    self.turtle_spawning_service_ready = True
                else:
                    # Check if the service is ready
                    self.get_logger().info('Service is not ready')


    def main():
        rclpy.init()
        node = FrameListener()
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass

        rclpy.shutdown()

1.1 检查代码
~~~~~~~~~~~~

要了解生成 turtle 背后的服务如何工作，请参考 :doc:`编写简单的服务与客户端（Python） <../../Beginner-Client-Libraries/Writing-A-Simple-Py-Service-And-Client>` 教程。

现在，让我们看看与获取帧变换相关的代码。
``tf2_ros`` 包提供了 ``TransformListener`` 的实现，以帮助简化接收变换的任务。

.. code-block:: python

    from tf2_ros.transform_listener import TransformListener

这里，我们创建一个 ``TransformListener`` 对象。
监听器创建后，它开始通过网络接收 tf2 变换，并缓冲它们最多 10 秒。

.. code-block:: python

    self.tf_listener = TransformListener(self.tf_buffer, self)

最后，我们向监听器查询特定的变换。
我们使用以下参数调用 ``lookup_transform`` 方法：

#. 目标帧

#. 源帧

#. 我们想要变换的时间

提供 ``rclpy.time.Time()`` 只会给我们最新的可用变换。
所有这些都包在 try-except 块中，以处理可能的异常。

.. code-block:: python

    t = self.tf_buffer.lookup_transform(
        to_frame_rel,
        from_frame_rel,
        rclpy.time.Time())

1.2 添加入口点
~~~~~~~~~~~~~~

为了让 ``ros2 run`` 命令能运行你的节点，你必须将入口点添加到 ``setup.py``\ （位于 ``src/learning_tf2_py`` 目录）。

在 ``'console_scripts':`` 括号之间添加以下行：

.. code-block:: python

    'turtle_tf2_listener = learning_tf2_py.turtle_tf2_listener:main',

2 更新启动文件
^^^^^^^^^^^^^^

用文本编辑器打开 ``src/learning_tf2_py/launch`` 目录中名为 ``turtle_tf2_demo_launch`` 的启动文件（扩展名为 ``.py``、``.xml`` 或 ``.yaml``），向启动描述添加两个新节点，添加一个启动参数，并添加导入。
最终文件应如下所示：

.. tabs::

  .. group-tab:: XML

    .. literalinclude:: launch/listener_py_launch.xml
        :language: xml
        :name: turtle_tf2_demo_launch.xml

  .. group-tab:: YAML

    .. literalinclude:: launch/listener_py_launch.yaml
        :language: yaml
        :name: turtle_tf2_demo_launch.yaml

  .. group-tab:: Python

    .. literalinclude:: launch/listener_py_launch.py
        :language: python
        :name: turtle_tf2_demo_launch.py

这将声明一个 ``target_frame`` 启动参数，为我们将要生成的第二只 turtle 启动一个广播器，并启动一个监听器来订阅这些变换。

3 构建
^^^^^^

在工作区根目录运行 ``rosdep`` 以检查缺少的依赖。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

          $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

        rosdep 仅在 Linux 上运行，因此你需要自己安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖

   .. group-tab:: Windows

        rosdep 仅在 Linux 上运行，因此你需要自己安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖

仍然在工作区根目录，构建你的包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ colcon build --packages-select learning_tf2_py

  .. group-tab:: macOS

    .. code-block:: console

        $ colcon build --packages-select learning_tf2_py

  .. group-tab:: Windows

    .. code-block:: console

        $ colcon build --merge-install --packages-select learning_tf2_py

打开一个新终端，导航到工作区根目录，并 source 设置文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ . install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

        $ . install/setup.bash

  .. group-tab:: Windows

    在 Windows 命令行提示符中：

    .. code-block:: console

        $ call install\setup.bat

    或者在 powershell 中：

    .. code-block:: console

        $ .\install\setup.ps1



4 运行
^^^^^^

现在你已准备好启动完整的 turtle 演示：

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_py turtle_tf2_demo_launch.xml

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_py turtle_tf2_demo_launch.yaml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_py turtle_tf2_demo_launch.py

你应该会看到有两只 turtle 的 turtle sim。
在第二个终端窗口中输入以下命令：

.. code-block:: console

    $ ros2 run turtlesim turtle_teleop_key

要查看是否正常工作，只需使用方向键驾驶第一只 turtle（确保你的终端窗口是活动的，而不是仿真器窗口），你会看到第二只 turtle 跟着第一只！

总结
----

在本教程中，你学习了如何使用 tf2 获取帧变换。
你也完成了自己的 turtlesim 演示，也就是你在 :doc:`tf2 介绍 <./Introduction-To-Tf2>` 教程中首次尝试的那个演示。
