.. redirect-from::

    Tutorials/Tf2/Writing-A-Tf2-Broadcaster-Py

编写广播器（Python）
====================

**目标：** 学习如何将机器人的状态广播到 tf2。

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在接下来的两个教程中，我们将编写代码来重现 :doc:`tf2 介绍 <./Introduction-To-Tf2>` 教程中的演示。
之后，后续教程将重点用更高级的 tf2 功能扩展演示，包括在变换查找中使用超时和时间旅行。

先决条件
--------

本教程假设你具备 ROS 2 的工作知识，并且已经完成 :doc:`tf2 介绍教程 <./Introduction-To-Tf2>` 和 :doc:`tf2 静态广播器教程（Python） <./Writing-A-Tf2-Static-Broadcaster-Py>`。
我们将重用上一个教程中的 ``learning_tf2_py`` 包。

在前面的教程中，你学习了如何 :doc:`创建工作区 <../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>`。

任务
----

1 编写广播器节点
^^^^^^^^^^^^^^^^

让我们先创建源文件。
转到我们在上一个教程中创建的 ``learning_tf2_py`` 包。
在 ``src/learning_tf2_py/learning_tf2_py`` 目录中，通过输入以下命令下载示例广播器代码：

.. tabs::

    .. group-tab:: Linux

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_broadcaster.py

    .. group-tab:: macOS

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_broadcaster.py

    .. group-tab:: Windows

        在 Windows 命令行提示符中：

        .. code-block:: console

            $ curl -sk https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_broadcaster.py -o turtle_tf2_broadcaster.py

        或者在 powershell 中：

        .. code-block:: console

            $ curl https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/turtle_tf2_broadcaster.py -o turtle_tf2_broadcaster.py

现在使用你喜欢的文本编辑器打开名为 ``turtle_tf2_broadcaster.py`` 的文件。

.. code-block:: python

    import math

    from geometry_msgs.msg import TransformStamped

    import numpy as np

    import rclpy
    from rclpy.node import Node

    from tf2_ros import TransformBroadcaster

    from turtlesim.msg import Pose


    def quaternion_from_euler(ai, aj, ak):
        ai /= 2.0
        aj /= 2.0
        ak /= 2.0
        ci = math.cos(ai)
        si = math.sin(ai)
        cj = math.cos(aj)
        sj = math.sin(aj)
        ck = math.cos(ak)
        sk = math.sin(ak)
        cc = ci*ck
        cs = ci*sk
        sc = si*ck
        ss = si*sk

        q = np.empty((4, ))
        q[0] = cj*sc - sj*cs
        q[1] = cj*ss + sj*cc
        q[2] = cj*cs - sj*sc
        q[3] = cj*cc + sj*ss

        return q


    class FramePublisher(Node):

        def __init__(self):
            super().__init__('turtle_tf2_frame_publisher')

            # Declare and acquire `turtlename` parameter
            self.turtlename = self.declare_parameter(
              'turtlename', 'turtle').get_parameter_value().string_value

            # Initialize the transform broadcaster
            self.tf_broadcaster = TransformBroadcaster(self)

            # Subscribe to a turtle{1}{2}/pose topic and call handle_turtle_pose
            # callback function on each message
            self.subscription = self.create_subscription(
                Pose,
                f'/{self.turtlename}/pose',
                self.handle_turtle_pose,
                1)
            self.subscription  # prevent unused variable warning

        def handle_turtle_pose(self, msg):
            t = TransformStamped()

            # Read message content and assign it to
            # corresponding tf variables
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'world'
            t.child_frame_id = self.turtlename

            # Turtle only exists in 2D, thus we get x and y translation
            # coordinates from the message and set the z coordinate to 0
            t.transform.translation.x = msg.x
            t.transform.translation.y = msg.y
            t.transform.translation.z = 0.0

            # For the same reason, turtle can only rotate around one axis
            # and this why we set rotation in x and y to 0 and obtain
            # rotation in z axis from the message
            q = quaternion_from_euler(0, 0, msg.theta)
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]

            # Send the transformation
            self.tf_broadcaster.sendTransform(t)


    def main():
        rclpy.init()
        node = FramePublisher()
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass

        rclpy.shutdown()

1.1 检查代码
~~~~~~~~~~~~

现在，让我们看看与将 turtle 位姿发布到 tf2 相关的代码。
首先，我们定义并获取单个参数 ``turtlename``，它指定 turtle 名称，例如 ``turtle1`` 或 ``turtle2``。

.. code-block:: python

    self.turtlename = self.declare_parameter(
      'turtlename', 'turtle').get_parameter_value().string_value

随后，节点订阅话题 ``{self.turtlename}/pose``，并在每个传入消息上运行函数 ``handle_turtle_pose``。

.. code-block:: python

     self .subscription = self.create_subscription(
         Pose,
         f'/{self.turtlename}/pose',
         self.handle_turtle_pose,
         1)

现在，我们创建一个 ``TransformStamped`` 对象并给它适当的元数据。

#. 我们需要给要发布的变换一个时间戳，我们通过调用 ``self.get_clock().now()`` 用当前时间来标记它。
   这将返回 ``Node`` 使用的当前时间。

#. 然后我们需要设置我们正在创建的链接的父帧名称，在本例中是 ``world``。

#. 最后，我们需要设置我们正在创建的链接的子节点名称，在本例中这是 turtle 本身的名称。

turtle 位姿消息的处理函数广播这只 turtle 的平移和旋转，并将其作为从帧 ``world`` 到帧 ``turtleX`` 的变换发布。

.. code-block:: python

    t = TransformStamped()

    # Read message content and assign it to
    # corresponding tf variables
    t.header.stamp = self.get_clock().now().to_msg()
    t.header.frame_id = 'world'
    t.child_frame_id = self.turtlename

这里我们将 3D turtle 位姿中的信息复制到 3D 变换中。

.. code-block:: python

    # Turtle only exists in 2D, thus we get x and y translation
    # coordinates from the message and set the z coordinate to 0
    t.transform.translation.x = msg.x
    t.transform.translation.y = msg.y
    t.transform.translation.z = 0.0

    # For the same reason, turtle can only rotate around one axis
    # and this why we set rotation in x and y to 0 and obtain
    # rotation in z axis from the message
    q = quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

最后，我们取构造好的变换，并将其传递给 ``TransformBroadcaster`` 的 ``sendTransform`` 方法，该方法将负责广播。

.. code-block:: python

    # Send the transformation
    self.tf_broadcaster.sendTransform(t)

1.2 添加入口点
~~~~~~~~~~~~~~

为了让 ``ros2 run`` 命令能运行你的节点，你必须将入口点添加到
``setup.py``\ （位于 ``src/learning_tf2_py`` 目录）。

在 ``'console_scripts':`` 括号之间添加以下行：

.. code-block:: python

    'turtle_tf2_broadcaster = learning_tf2_py.turtle_tf2_broadcaster:main',

2 编写启动文件
^^^^^^^^^^^^^^

现在为这个演示创建一个启动文件。
在 ``src/learning_tf2_py`` 目录中创建一个 ``launch`` 文件夹。
用文本编辑器在 ``launch`` 文件夹中创建一个名为 ``turtle_tf2_demo_launch`` 的新文件，扩展名为 ``.py``、``.xml`` 或 ``.yaml``，并添加以下行：

.. tabs::

  .. group-tab:: XML

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.xml
        :language: xml
        :name: turtle_tf2_demo_launch.xml

  .. group-tab:: YAML

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.yaml
        :language: yaml
        :name: turtle_tf2_demo_launch.yaml

  .. group-tab:: Python

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.py
        :language: python
        :name: turtle_tf2_demo_launch.py


2.1 检查代码
~~~~~~~~~~~~

让我们检查启动文件的结构。
每种格式都有自己的启动文件设置方式：

.. tabs::

  .. group-tab:: XML

    XML 启动文件以 XML 声明和一个根 ``<launch>`` 元素开头。

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.xml
        :language: xml
        :lines: 1-2

  .. group-tab:: YAML

    YAML 启动文件以 YAML 版本声明和一个 ``launch:`` 键开头。

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.yaml
        :language: yaml
        :lines: 1-3

  .. group-tab:: Python

    在 Python 启动文件中，我们首先从 ``launch`` 和 ``launch_ros`` 包导入所需的模块。
    需要注意的是，``launch`` 是一个通用的启动框架（不是 ROS 2 特定的），而 ``launch_ros`` 有 ROS 2 特定的内容，比如我们在这里导入的节点。

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.py
        :language: python
        :lines: 1-2

现在我们运行节点，启动 turtlesim 仿真，并使用 ``turtle_tf2_broadcaster`` 节点将 ``turtle1`` 状态广播到 tf2。

.. tabs::

  .. group-tab:: XML

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.xml
        :language: xml
        :lines: 3-6

  .. group-tab:: YAML

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.yaml
        :language: yaml
        :lines: 4-9

  .. group-tab:: Python

    .. literalinclude:: launch/py_turtle_tf2_demo_launch.py
        :language: python
        :lines: 5-20

2.2 添加依赖
~~~~~~~~~~~~

返回上一级目录 ``learning_tf2_py``，那里有 ``setup.py``、``setup.cfg`` 和 ``package.xml`` 文件。

用文本编辑器打开 ``package.xml``。
添加与你的启动文件导入语句对应的以下依赖：

.. code-block:: xml

    <exec_depend>launch</exec_depend>
    <exec_depend>launch_ros</exec_depend>

这声明了代码执行时所需的额外的 ``launch`` 和 ``launch_ros`` 依赖。

确保保存文件。

2.3 更新 setup.py
~~~~~~~~~~~~~~~~~

重新打开 ``setup.py`` 并添加这一行，以便 ``launch/`` 文件夹中的启动文件会被安装。
``data_files`` 字段现在应如下所示：

.. code-block:: python

    data_files=[
        ...
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],

同时在文件顶部添加适当的导入：

.. code-block:: python

    import os
    from glob import glob

你可以在 :doc:`本教程 <../Launch/Creating-Launch-Files>` 中了解更多关于创建启动文件的信息。

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

现在运行启动文件，它将启动 turtlesim 仿真节点和 ``turtle_tf2_broadcaster`` 节点：

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

在第二个终端窗口中输入以下命令：

.. code-block:: console

    $ ros2 run turtlesim turtle_teleop_key

现在你会看到 turtlesim 仿真已启动，有一只你可以控制的 turtle。

.. image:: images/turtlesim_broadcast.png

现在，使用 ``tf2_echo`` 工具检查 turtle 位姿是否真的被广播到 tf2：

.. code-block:: console

    $ ros2 run tf2_ros tf2_echo world turtle1

这应该会显示第一只 turtle 的位姿。
使用方向键驾驶 turtle（确保你的 ``turtle_teleop_key`` 终端窗口是活动的，而不是仿真器窗口）。
在你的控制台输出中，你会看到类似这样的内容：

.. code-block:: console

    At time 1714913843.708748879
    - Translation: [4.541, 3.889, 0.000]
    - Rotation: in Quaternion [0.000, 0.000, 0.999, -0.035]
    - Rotation: in RPY (radian) [0.000, -0.000, -3.072]
    - Rotation: in RPY (degree) [0.000, -0.000, -176.013]
    - Matrix:
     -0.998  0.070  0.000  4.541
     -0.070 -0.998  0.000  3.889
      0.000  0.000  1.000  0.000
      0.000  0.000  0.000  1.000

如果你对 ``world`` 和 ``turtle2`` 之间的变换运行 ``tf2_echo``，你不会看到变换，因为第二只 turtle 还不存在。
然而，一旦我们在下一个教程中添加第二只 turtle，``turtle2`` 的位姿就会被广播到 tf2。

总结
----

在本教程中，你学习了如何将机器人的位姿（turtle 的位置和方向）广播到 tf2，以及如何使用 ``tf2_echo`` 工具。
要真正使用广播到 tf2 的变换，你应该继续学习下一个关于创建 :doc:`tf2 监听器 <./Writing-A-Tf2-Listener-Py>` 的教程。
