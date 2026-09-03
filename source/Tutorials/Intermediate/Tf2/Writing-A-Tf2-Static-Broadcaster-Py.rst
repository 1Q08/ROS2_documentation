.. redirect-from::

    Tutorials/Tf2/Writing-A-Tf2-Static-Broadcaster-Py

编写静态广播器（Python）
========================

**目标：** 学习如何将静态坐标帧广播到 tf2。

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

发布静态变换对于定义机器人基座与其传感器或非移动部件之间的关系很有用。
例如，在位于激光扫描仪中心的帧中推理激光扫描测量是最容易的。

这是一个独立的教程，涵盖静态变换的基础知识，由两部分组成。
在第一部分中，我们将编写代码将静态变换发布到 tf2。
在第二部分中，我们将解释如何使用 ``tf2_ros`` 中的命令行 ``static_transform_publisher`` 可执行工具。

在接下来的两个教程中，我们将编写代码来重现 :doc:`tf2 介绍 <./Introduction-To-Tf2>` 教程中的演示。
之后，后续教程将重点用更高级的 tf2 功能扩展演示。

先决条件
--------

在前面的教程中，你学习了如何 :doc:`创建工作区 <../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>`。

任务
----

1 创建包
^^^^^^^^

首先，我们将创建一个用于本教程和后续教程的包。
名为 ``learning_tf2_py`` 的包将依赖 ``geometry_msgs``、``python3-numpy``、``rclpy``、``tf2_ros_py`` 和 ``turtlesim``。
本教程的代码存储 `在这里 <https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/static_turtle_tf2_broadcaster.py>`_。

打开一个新终端并 :doc:`source 你的 ROS 2 安装 <../../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，以便 ``ros2`` 命令可以正常工作。
导航到工作区的 ``src`` 文件夹并创建一个新包：

.. code-block:: console

   $ ros2 pkg create --build-type ament_python --license Apache-2.0 -- learning_tf2_py

你的终端将返回一条消息，验证你的包 ``learning_tf2_py`` 及其所有必要文件和文件夹的创建。

2 编写静态广播器节点
^^^^^^^^^^^^^^^^^^^^

让我们先创建源文件。
在 ``src/learning_tf2_py/learning_tf2_py`` 目录中，通过输入以下命令下载示例静态广播器代码：

.. tabs::

    .. group-tab:: Linux

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/static_turtle_tf2_broadcaster.py

    .. group-tab:: macOS

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/static_turtle_tf2_broadcaster.py

    .. group-tab:: Windows

        在 Windows 命令行提示符中：

        .. code-block:: console

                $ curl -sk https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/static_turtle_tf2_broadcaster.py -o static_turtle_tf2_broadcaster.py

        或者在 powershell 中：

        .. code-block:: console

                $ curl https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_py/turtle_tf2_py/static_turtle_tf2_broadcaster.py -o static_turtle_tf2_broadcaster.py

现在使用你喜欢的文本编辑器打开名为 ``static_turtle_tf2_broadcaster.py`` 的文件。

.. code-block:: python

    import math
    import sys

    from geometry_msgs.msg import TransformStamped

    import numpy as np

    import rclpy
    from rclpy.node import Node

    from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


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


    class StaticFramePublisher(Node):
        """
        Broadcast transforms that never change.

        This example publishes transforms from `world` to a static turtle frame.
        The transforms are only published once at startup, and are constant for all
        time.
        """

        def __init__(self, transformation):
            super().__init__('static_turtle_tf2_broadcaster')

            self.tf_static_broadcaster = StaticTransformBroadcaster(self)

            # Publish static transforms once at startup
            self.make_transforms(transformation)

        def make_transforms(self, transformation):
            t = TransformStamped()

            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'world'
            t.child_frame_id = transformation[1]

            t.transform.translation.x = float(transformation[2])
            t.transform.translation.y = float(transformation[3])
            t.transform.translation.z = float(transformation[4])
            quat = quaternion_from_euler(
                float(transformation[5]), float(transformation[6]), float(transformation[7]))
            t.transform.rotation.x = quat[0]
            t.transform.rotation.y = quat[1]
            t.transform.rotation.z = quat[2]
            t.transform.rotation.w = quat[3]

            self.tf_static_broadcaster.sendTransform(t)


    def main():
        logger = rclpy.logging.get_logger('logger')

        # obtain parameters from command line arguments
        if len(sys.argv) != 8:
            logger.info('Invalid number of parameters. Usage: \n'
                        '$ ros2 run learning_tf2_py static_turtle_tf2_broadcaster'
                        'child_frame_name x y z roll pitch yaw')
            sys.exit(1)

        if sys.argv[1] == 'world':
            logger.info('Your static turtle name cannot be "world"')
            sys.exit(2)

        # pass parameters and initialize node
        rclpy.init()
        node = StaticFramePublisher(sys.argv)
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass

        rclpy.shutdown()

2.1 检查代码
~~~~~~~~~~~~

现在让我们看看与将静态 turtle 位姿发布到 tf2 相关的代码。
第一行导入所需的包。
首先我们从 ``geometry_msgs`` 导入 ``TransformStamped``，它为我们提供了一个消息模板，我们将把这个消息发布到变换树。

.. code-block:: python

    from geometry_msgs.msg import TransformStamped

随后，导入 ``rclpy``，以便使用它的 ``Node`` 类。

.. code-block:: python

    import rclpy
    from rclpy.node import Node

``tf2_ros`` 包提供了一个 ``StaticTransformBroadcaster``，使静态变换的发布变得容易。
要使用 ``StaticTransformBroadcaster``，我们需要从 ``tf2_ros`` 模块导入它。

.. code-block:: python

    from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

``StaticFramePublisher`` 类构造函数用名称 ``static_turtle_tf2_broadcaster`` 初始化节点。
然后，创建 ``StaticTransformBroadcaster``，它将在启动时发送一个静态变换。

.. code-block:: python

    self.tf_static_broadcaster = StaticTransformBroadcaster(self)
    self.make_transforms(transformation)

这里我们创建一个 ``TransformStamped`` 对象，它将是填充后我们要发送的消息。
在传入实际变换值之前，我们需要给它适当的元数据。

#. 我们需要给要发布的变换一个时间戳，我们只用当前时间 ``self.get_clock().now()`` 来标记它。

#. 然后我们需要设置我们正在创建的链接的父帧名称，在本例中是 ``world``。

#. 最后，我们需要设置我们正在创建的链接的子帧名称。

.. code-block:: python

    t = TransformStamped()

    t.header.stamp = self.get_clock().now().to_msg()
    t.header.frame_id = 'world'
    t.child_frame_id = transformation[1]

这里我们填充 turtle 的 6D 位姿（平移和旋转）。

.. code-block:: python

    t.transform.translation.x = float(transformation[2])
    t.transform.translation.y = float(transformation[3])
    t.transform.translation.z = float(transformation[4])
    quat = quaternion_from_euler(
        float(transformation[5]), float(transformation[6]), float(transformation[7]))
    t.transform.rotation.x = quat[0]
    t.transform.rotation.y = quat[1]
    t.transform.rotation.z = quat[2]
    t.transform.rotation.w = quat[3]

最后，我们使用 ``sendTransform()`` 函数广播静态变换。

.. code-block:: python

    self.tf_static_broadcaster.sendTransform(t)

2.2 更新 package.xml
~~~~~~~~~~~~~~~~~~~~

向上导航一级到 ``src/learning_tf2_py`` 目录，那里已经为你创建了 ``setup.py``、``setup.cfg`` 和 ``package.xml`` 文件。

用你的文本编辑器打开 ``package.xml``。

如 :doc:`创建包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>` 教程所述，确保填写 ``<description>``、``<maintainer>`` 和 ``<license>`` 标签：

.. code-block:: xml

    <description>Learning tf2 with rclpy</description>
    <maintainer email="you@email.com">Your Name</maintainer>
    <license>Apache-2.0</license>

在上面几行之后，添加与你节点的 import 语句对应的以下依赖：

.. code-block:: xml

    <exec_depend>geometry_msgs</exec_depend>
    <exec_depend>python3-numpy</exec_depend>
    <exec_depend>rclpy</exec_depend>
    <exec_depend>tf2_ros_py</exec_depend>
    <exec_depend>turtlesim</exec_depend>

这声明了代码执行时所需的 ``geometry_msgs``、``python3-numpy``、``rclpy``、``tf2_ros_py`` 和 ``turtlesim`` 依赖。

确保保存文件。

2.3 添加入口点
~~~~~~~~~~~~~~

为了让 ``ros2 run`` 命令能运行你的节点，你必须将入口点添加到 ``setup.py``\ （位于 ``src/learning_tf2_py`` 目录）。

在 ``'console_scripts':`` 括号之间添加以下行：

.. code-block:: python

    'static_turtle_tf2_broadcaster = learning_tf2_py.static_turtle_tf2_broadcaster:main',

3 构建
^^^^^^

在构建之前，最好在工作空间根目录运行 ``rosdep`` 来检查是否缺少依赖：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

          $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

      rosdep 仅在 Linux 上运行，因此你需要自行安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖。

   .. group-tab:: Windows

      rosdep 仅在 Linux 上运行，因此你需要自行安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖。

仍然在工作空间根目录中，构建你的新包：

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

打开一个新终端，导航到工作空间根目录，并 source 设置文件：

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

现在运行 ``static_turtle_tf2_broadcaster`` 节点：

.. code-block:: console

    $ ros2 run learning_tf2_py static_turtle_tf2_broadcaster mystaticturtle 0 0 1 0 0 0

这将为 ``mystaticturtle`` 设置一个海龟位姿广播，使其悬浮在地面上方 1 米处。

现在我们可以通过 echo ``tf_static`` 话题来检查静态变换是否已发布。
如果一切正常，你应该会看到单个静态变换：

.. code-block:: console

    $ ros2 topic echo /tf_static
    transforms:
    - header:
       stamp:
          sec: 1622908754
          nanosec: 208515730
       frame_id: world
    child_frame_id: mystaticturtle
    transform:
       translation:
          x: 0.0
          y: 0.0
          z: 1.0
       rotation:
          x: 0.0
          y: 0.0
          z: 0.0
          w: 1.0

发布静态变换的正确方法
----------------------

本教程旨在展示如何使用 ``StaticTransformBroadcaster`` 发布静态变换。
在实际开发过程中，你不必自己编写这些代码，而应该使用专门的 ``tf2_ros`` 工具来完成。
``tf2_ros`` 提供了一个名为 ``static_transform_publisher`` 的可执行文件，既可以用作命令行工具，也可以作为可添加到 launch 文件中的节点。

以下命令向 tf2 发布一个静态坐标变换，在 ``world`` 和 ``mystaticturtle`` 坐标系之间产生 z 方向 1 米的偏移，且无旋转。
在 ROS 2 中，roll/pitch/yaw 分别指绕 x/y/z 轴的旋转（以弧度为单位）。

.. code-block:: console

    $ ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --yaw 0 --pitch 0 --roll 0 --frame-id world --child-frame-id mystaticturtle

以下命令向 tf2 发布相同的静态坐标变换，但旋转使用四元数表示。

.. code-block:: console

    $ ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --qx 0 --qy 0 --qz 0 --qw 1 --frame-id world --child-frame-id mystaticturtle

``static_transform_publisher`` 既被设计为手动使用的命令行工具，也可在 ``launch`` 文件中用于设置静态变换。
例如：

.. tabs::

   .. group-tab:: XML

      .. literalinclude:: launch/static_transform_publisher_launch.xml
         :language: xml

   .. group-tab:: YAML

      .. literalinclude:: launch/static_transform_publisher_launch.yaml
         :language: yaml

   .. group-tab:: Python

      .. literalinclude:: launch/static_transform_publisher_launch.py
         :language: python

请注意，除了 ``--frame-id`` 和 ``--child-frame-id`` 之外的所有参数都是可选的；如果未指定某个选项，则假定为恒等变换。

总结
----

在本教程中，你学习了静态变换如何用于定义坐标系之间的静态关系，例如 ``mystaticturtle`` 与 ``world`` 坐标系的关系。
此外，你还学习了静态变换如何通过将数据关联到一个公共坐标系来帮助理解传感器数据（例如来自激光扫描仪的数据）。
最后，你编写了自己的节点向 tf2 发布静态变换，并学习了如何使用 ``static_transform_publisher`` 可执行文件和 launch 文件发布所需的静态变换。
