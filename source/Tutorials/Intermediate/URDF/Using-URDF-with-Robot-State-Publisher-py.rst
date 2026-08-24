.. redirect-from::

    Tutorials/URDF/Using-URDF-with-Robot-State-Publisher

.. _URDFPlusRSPPYTHON:

将 URDF 与 ``robot_state_publisher`` 结合使用（Python）
=======================================================

**目标：** 模拟一个在 URDF 中建模的行走机器人，并在 Rviz 中查看它。

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

本教程将展示如何建模一个行走机器人，将状态发布为 `tf2 <https://wiki.ros.org/tf2>`__ 消息，并在 Rviz 中查看仿真。
首先，我们创建描述机器人装配的 URDF 模型。
接下来，我们编写一个节点来模拟运动并发布 JointState 和变换。
然后我们使用 ``robot_state_publisher`` 将整个机器人状态发布到 ``/tf2``。

.. image:: images/r2d2_rviz_demo.gif

先决条件
--------

- `rviz2 <https://index.ros.org/p/rviz2/>`__

和往常一样，别忘了在 :doc:`你打开的每个新终端 <../../Beginner-CLI-Tools/Configuring-ROS2-Environment>` 中 source ROS 2。

任务
----

1 创建一个包
^^^^^^^^^^^^
创建目录：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ mkdir -p second_ros2_ws/src

  .. group-tab:: macOS

    .. code-block:: console

      $ mkdir -p second_ros2_ws/src

  .. group-tab:: Windows

    .. code-block:: console

      $ md second_ros2_ws/src

然后创建包：

.. code-block:: console

    $ cd second_ros2_ws/src
    $ ros2 pkg create --build-type ament_python --license Apache-2.0 urdf_tutorial_r2d2 --dependencies rclpy
    $ cd urdf_tutorial_r2d2

你现在应该看到一个 ``urdf_tutorial_r2d2`` 文件夹。
接下来你将对它进行几处修改。

2 创建 URDF 文件
^^^^^^^^^^^^^^^^

创建我们将存放一些资源文件的目录：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ mkdir -p urdf

  .. group-tab:: macOS

    .. code-block:: console

      $ mkdir -p urdf

  .. group-tab:: Windows

    .. code-block:: console

      $ md urdf

下载 :download:`URDF 文件 <documents/r2d2.urdf.xml>` 并将其保存为 ``second_ros2_ws/src/urdf_tutorial_r2d2/urdf/r2d2.urdf.xml``。
下载 :download:`Rviz 配置文件 <documents/r2d2.rviz>` 并将其保存为 ``second_ros2_ws/src/urdf_tutorial_r2d2/urdf/r2d2.rviz``。

3 发布状态
^^^^^^^^^^

现在我们需要一种方法来指定机器人处于什么状态。
为此，我们必须指定所有三个关节和整体里程计。

打开你喜欢的编辑器，将以下代码粘贴到 ``second_ros2_ws/src/urdf_tutorial_r2d2/urdf_tutorial_r2d2/state_publisher.py``

.. code-block:: python

  from math import sin, cos, pi
  import rclpy
  from rclpy.node import Node
  from rclpy.qos import QoSProfile
  from geometry_msgs.msg import Quaternion
  from sensor_msgs.msg import JointState
  from tf2_ros import TransformBroadcaster, TransformStamped

  class StatePublisher(Node):

      def __init__(self):
          rclpy.init()
          super().__init__('state_publisher')

          qos_profile = QoSProfile(depth=10)
          self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
          self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
          self.nodeName = self.get_name()
          self.get_logger().info("{0} started".format(self.nodeName))

          degree = pi / 180.0
          loop_rate = self.create_rate(30)

          # robot state
          tilt = 0.
          tinc = degree
          swivel = 0.
          angle = 0.
          height = 0.
          hinc = 0.005

          # message declarations
          odom_trans = TransformStamped()
          odom_trans.header.frame_id = 'odom'
          odom_trans.child_frame_id = 'axis'
          joint_state = JointState()

          try:
              while rclpy.ok():
                  rclpy.spin_once(self)

                  # update joint_state
                  now = self.get_clock().now()
                  joint_state.header.stamp = now.to_msg()
                  joint_state.name = ['swivel', 'tilt', 'periscope']
                  joint_state.position = [swivel, tilt, height]

                  # update transform
                  # (moving in a circle with radius=2)
                  odom_trans.header.stamp = now.to_msg()
                  odom_trans.transform.translation.x = cos(angle)*2
                  odom_trans.transform.translation.y = sin(angle)*2
                  odom_trans.transform.translation.z = 0.7
                  odom_trans.transform.rotation = \
                      euler_to_quaternion(0, 0, angle + pi/2) # roll,pitch,yaw

                  # send the joint state and transform
                  self.joint_pub.publish(joint_state)
                  self.broadcaster.sendTransform(odom_trans)

                  # Create new robot state
                  tilt += tinc
                  if tilt < -0.5 or tilt > 0.0:
                      tinc *= -1
                  height += hinc
                  if height > 0.2 or height < 0.0:
                      hinc *= -1
                  swivel += degree
                  angle += degree/4

                  # This will adjust as needed per iteration
                  loop_rate.sleep()

          except KeyboardInterrupt:
              pass

  def euler_to_quaternion(roll, pitch, yaw):
      qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
      qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
      qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
      qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
      return Quaternion(x=qx, y=qy, z=qz, w=qw)

  def main():
      node = StatePublisher()

  if __name__ == '__main__':
      main()

4 创建一个 launch 文件
^^^^^^^^^^^^^^^^^^^^^^

创建一个新的 ``second_ros2_ws/src/urdf_tutorial_r2d2/launch`` 文件夹。
打开你的编辑器，粘贴以下代码，并将其保存为 ``second_ros2_ws/src/urdf_tutorial_r2d2/launch/demo_launch.py``

.. literalinclude:: launch/demo_launch.py
  :language: python


5 编辑 setup.py 文件
^^^^^^^^^^^^^^^^^^^^

你必须告诉 **colcon** 构建工具如何安装你的 Python 包。
如下编辑 ``second_ros2_ws/src/urdf_tutorial_r2d2/setup.py`` 文件：

- 包含这些 import 语句

.. code-block:: python

  import os
  from glob import glob
  from setuptools import setup
  from setuptools import find_packages

- 在 ``data_files`` 中追加这两行

.. code-block:: python

  data_files=[
    ...
    (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    (os.path.join('share', package_name), glob('urdf/*')),
  ],

- 修改 ``entry_points`` 表，这样你以后可以从控制台运行 'state_publisher'

.. code-block:: python

        'console_scripts': [
            'state_publisher = urdf_tutorial_r2d2.state_publisher:main'
        ],

用你的修改保存 ``setup.py`` 文件。

6 安装包
^^^^^^^^

.. code-block:: console

    $ cd second_ros2_ws
    $ colcon build --symlink-install --packages-select urdf_tutorial_r2d2

Source 安装文件：

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


7 查看结果
^^^^^^^^^^

启动包

.. code-block:: console

  $ ros2 launch urdf_tutorial_r2d2 demo_launch.py

打开一个新终端，然后用以下命令运行 Rviz

.. code-block:: console

  $ rviz2 -d `ros2 pkg prefix urdf_tutorial_r2d2 --share`/r2d2.rviz

有关如何使用 Rviz 的详细信息，请参阅 `用户指南 <http://wiki.ros.org/rviz/UserGuide>`__。

总结
----

你创建了一个 ``JointState`` 发布器节点，并将其与 ``robot_state_publisher`` 结合使用，以模拟一个行走的机器人。
这些示例中使用的代码最初来自 `这里 <https://github.com/benbongalon/ros2-migration/tree/master/urdf_tutorial>`__。

此内容的致谢归于本
`ROS 1 教程 <http://wiki.ros.org/urdf/Tutorials/Using%20urdf%20with%20robot_state_publisher>`__ 的作者，
其中部分内容被重用。
