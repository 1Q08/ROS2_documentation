.. redirect-from::

    Rosbag-with-ROS1-Bridge
    Tutorials/Rosbag-with-ROS1-Bridge

使用 ROS 1 桥接的 ``rosbag`` 录制和回放数据
===========================================

本教程是 *ROS 1 和 ROS 2 之间的桥接通信* 演示的后续，该演示可在 `此处 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__ 找到，以下内容假设你已经完成了该教程。

对于这些示例，ros1_bridge 可以从 :doc:`源代码 <../../How-To-Guides/Using-ros1_bridge-Jammy-upstream>` 构建。

接下来是一系列额外的示例，就像上述 *ROS 1 和 ROS 2 之间的桥接通信* 演示末尾的那些一样。

使用 rosbag 和 ROS 1 Bridge 录制话题数据
----------------------------------------

在本示例中，我们将使用 ROS 2 自带的 ``cam2image`` 演示程序，以及一个 Python 脚本来模拟类似 turtlebot 机器人的传感器数据，以便将其桥接到 ROS 1 并用 rosbag 录制。

首先，我们在一个新 shell 中运行 ROS 1 的 ``roscore``：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

         $ . /opt/ros/kinetic/setup.bash
         $ roscore

   .. group-tab:: macOS

      .. code-block:: console

         $ . ~/ros_catkin_ws/install_isolated/setup.bash
         $ rocore

然后在另一个 shell 中运行带 ``--bridge-all-topics`` 选项的 ROS 1 <=> ROS 2 ``dynamic_bridge``（这样我们就可以运行 ``rostopic list`` 并看到它们）：

.. note::

   如果你是从源代码安装 rosbridge 的，请相应调整 setup 文件的路径：
   ``. <带桥接的工作空间>/install/setup.bash``。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ . /opt/ros/kinetic/setup.bash
        $ . /opt/ros/ardent/setup.bash
        $ export ROS_MASTER_URI=http://localhost:11311
        $ ros2 run ros1_bridge dynamic_bridge --bridge-all-topics

   .. group-tab:: macOS

      .. code-block:: console

        $ . ~/ros_catkin_ws/install_isolated/setup.bash
        $ . /opt/ros/ardent/setup.bash
        $ export ROS_MASTER_URI=http://localhost:11311
        $ ros2 run ros1_bridge dynamic_bridge --bridge-all-topics


----

现在我们可以启动 ROS 2 程序来模拟我们的类 turtlebot 机器人。
首先，我们用 ``-b`` 选项运行 ``cam2image`` 程序，这样它就不需要摄像头也能工作。
在另一个 shell 中：

.. code-block:: console

   $ . /opt/ros/ardent/setup.bash
   $ ros2 run image_tools cam2image -- -b

TODO: 使用命名空间话题名称

然后我们运行一个简单的 Python 脚本来模拟 Kobuki 底座的 ``odom`` 和 ``imu_data`` 话题。
我会使用更准确的 ``~sensors/imu_data`` 话题名称来表示 imu 数据，但 ROS 2 目前还没有命名空间支持（它即将到来！）。
将此脚本放在一个名为 ``emulate_kobuki_node.py`` 的文件中：

.. code-block:: python

   #!/usr/bin/env python3

   import sys
   import time

   import rclpy

   from nav_msgs.msg import Odometry
   from sensor_msgs.msg import Imu

   def main():
       rclpy.init(args=sys.argv)

       node = rclpy.create_node('emulate_kobuki_node')

       imu_publisher = node.create_publisher(Imu, 'imu_data')
       odom_publisher = node.create_publisher(Odometry, 'odom')

       imu_msg = Imu()
       odom_msg = Odometry()
       counter = 0
       while True:
           counter += 1
           now = time.time()
           if (counter % 50) == 0:
               odom_msg.header.stamp.sec = int(now)
               odom_msg.header.stamp.nanosec = int(now * 1e9) % 1000000000
               odom_publisher.publish(odom_msg)
           if (counter % 100) == 0:
               imu_msg.header.stamp.sec = int(now)
               imu_msg.header.stamp.nanosec = int(now * 1e9) % 1000000000
               imu_publisher.publish(imu_msg)
               counter = 0
           time.sleep(0.001)


   if __name__ == '__main__':
       sys.exit(main())

你可以在一个新的 ROS 2 shell 中运行这个 Python 脚本：

.. code-block:: console

   $ . /opt/ros/ardent/setup.bash
   $ python3 emulate_kobuki_node.py

.. note::

   如果是从源代码构建 ROS 2，请相应调整 setup 文件的路径：``<带桥接的工作空间>/install/setup.bash``。

----

现在所有数据源和动态桥接都在运行了，我们可以在一个新的 ROS 1 shell 中查看可用的话题：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

       $ . /opt/ros/kinetic/setup.bash
       $ rostopic list
       /image
       /imu_data
       /odom
       /rosout
       /rosout_agg

   .. group-tab:: macOS

      .. code-block:: console

       $ . ~/ros_catkin_ws/install_isolated/setup.bash
       $ rostopic list
       /image
       /imu_data
       /odom
       /rosout
       /rosout_agg

现在我们可以用 ``rosbag record`` 在同一个 shell 中录制这些数据：

.. code-block:: console

   $ rosbag record /image /imu_data /odom

几秒钟后，你可以对 ``rosbag`` 命令执行 ``Ctrl-c``，然后执行 ``ls -lh`` 看看文件有多大，你可能会看到类似这样的结果：

.. code-block:: console

   $ ls -lh
   total 0
   -rw-rw-r-- 1 william william  12M Feb 23 16:59 2017-02-23-16-59-47.bag

不过你的 bag 文件名会不同（因为它是根据日期和时间派生的）。

使用 rosbag 和 ROS 1 Bridge 回放话题数据
----------------------------------------

现在我们有了一个 bag 文件，你可以使用任何 ROS 1 工具来检视这个 bag 文件，比如 ``rosbag info <bag file>``、``rostopic list -b <bag file>`` 或 ``rqt_bag <bag file>``。
不过，我们也可以使用 ``rosbag play`` 和 ROS 1 <=> ROS 2 的 ``dynamic_bridge`` 将 bag 数据回放到 ROS 2 中。

首先，关闭你为上一个教程打开的所有 shell，停止所有正在运行的程序。

然后在一个新 shell 中启动 ``roscore``：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

       $ . /opt/ros/kinetic/setup.bash
       $ roscore

   .. group-tab:: macOS

      .. code-block:: console

        $ . ~/ros_catkin_ws/install_isolated/setup.bash
        $ roscore

然后在另一个 shell 中运行 ``dynamic_bridge``：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

       $ . /opt/ros/kinetic/setup.bash
       $ . /opt/ros/ardent/setup.bash
       $ export ROS_MASTER_URI=http://localhost:11311
       $ ros2 run ros1_bridge dynamic_bridge --bridge-all-topics

   .. group-tab:: macOS

      .. code-block:: console

       $ . ~/ros_catkin_ws/install_isolated/setup.bash
       $ . /opt/ros/ardent/setup.bash
       $ export ROS_MASTER_URI=http://localhost:11311
       $ ros2 run ros1_bridge dynamic_bridge --bridge-all-topics

然后在另一个新 shell 中用 ``rosbag play`` 回放 bag 数据，使用 ``--loop`` 选项，这样对于较短的 bag 我们就不必反复重启它：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ . /opt/ros/kinetic/setup.bash
        $ rosbag play --loop path/to/bag_file

   .. group-tab:: macOS

      .. code-block:: console

        $ . ~/ros_catkin_ws/install_isolated/setup.bash
        $ rosbag play --loop path/to/bag_file

.. note::

   请确保将 ``path/to/bag_file`` 替换为你想要回放的 bag 文件的路径。

----

现在数据正在回放且桥接正在运行，我们可以在 ROS 2 中看到传过来的数据。

.. code-block:: console

   $ . /opt/ros/ardent/setup.bash
   $ ros2 topic list
   /clock
   /image
   /imu_data
   /odom
   /parameter_events
   $ ros2 topic echo /odom

你还可以使用 ``showimage`` 工具看到从 bag 中回放的图像：

.. code-block:: console

   $ ros2 run image_tools showimage
