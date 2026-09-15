.. redirect-from::

    Tutorials/Simulators/Ignition/Setting-up-a-Robot-Simulation-Ignition
    Tutorials/Advanced/Simulators/Ignition
    Tutorials/Advanced/Simulators/Gazebo

设置机器人仿真（Gazebo）
========================

**目标：** 使用 Gazebo 和 ROS 2 启动仿真

**教程级别：** 高级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

前置条件
--------

首先你需要安装 ROS 2 和 Gazebo。
你有两种选择：

 - 从 deb 软件包安装。
   要查看 deb 软件包中提供哪些版本，请查看这个 `表格 <https://github.com/gazebosim/ros_ign>`__。
 - 从源码编译：

   - :doc:`ROS 2 安装说明 <../../../../Installation>`
   - `Gazebo 安装说明 <https://gazebosim.org/docs>`__

任务
----

1 启动仿真
^^^^^^^^^^

在这个演示中，你将在 Gazebo 中仿真一个简单的差速驱动机器人。
你将使用 Gazebo 示例中定义的某个 world，名为
`visualize_lidar.sdf <https://github.com/gazebosim/gz-sim/blob/main/examples/worlds/visualize_lidar.sdf>`__。
要运行这个示例，你应该在终端中执行以下命令：

`ROS REP-2000 <https://reps.openrobotics.org/rep-2000/>`__ 标准化了每个 ROS 发行版默认使用哪个版本的 Gazebo。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ ign gazebo -v 4 -r visualize_lidar.sdf

.. image:: Image/gazebo_diff_drive.png

仿真运行后，你可以使用 ``ign`` 命令行工具查看 Gazebo 提供的话题：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ ign topic -l
        /clock
        /gazebo/resource_paths
        /gui/camera/pose
        /gui/record_video/stats
        /model/vehicle_blue/odometry
        /model/vehicle_blue/tf
        /stats
        /world/visualize_lidar_world/clock
        /world/visualize_lidar_world/dynamic_pose/info
        /world/visualize_lidar_world/pose/info
        /world/visualize_lidar_world/scene/deletion
        /world/visualize_lidar_world/scene/info
        /world/visualize_lidar_world/state
        /world/visualize_lidar_world/stats

由于你还没有启动任何 ROS 2 节点，``ros2 topic list`` 的输出中
应该没有任何机器人话题：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ ros2 topic list
        /parameter_events
        /rosout

2 配置 ROS 2
^^^^^^^^^^^^

要让我们仿真的内容与 ROS 2 通信，你需要使用一个名为 ``ros_gz_bridge`` 的软件包。
该软件包提供了一个网络桥接，可以在 ROS 2 和 Gazebo Transport 之间交换消息。
你可以通过输入以下命令来安装这个软件包：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ sudo apt-get install ros-{DISTRO}-ros-ign-bridge

此时你已经可以从 ROS 桥接到 Gazebo 了。
具体来说，你将为话题 ``/model/vehicle_blue/cmd_vel`` 创建一个桥接：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash
        $ ros2 run ros_gz_bridge parameter_bridge /model/vehicle_blue/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist

有关 ``ros_gz_bridge`` 的更多细节，请查看这个 `README <https://github.com/gazebosim/ros_gz/tree/ros2/ros_gz_bridge>`__ 。

桥接运行后，机器人就能够跟随你的电机指令运动了。
有两种选择：

* 使用 ``ros2 topic pub`` 向该话题发送命令

 .. tabs::

    .. group-tab:: Linux

       .. code-block:: console

        $ ros2 topic pub /model/vehicle_blue/cmd_vel geometry_msgs/Twist "linear: { x: 0.1 }"

* ``teleop_twist_keyboard`` 软件包。
  该节点从键盘获取按键，并将它们作为 Twist 消息发布。
  你可以通过输入以下命令来安装它：

 .. tabs::

    .. group-tab:: Linux

       .. code-block:: console

         $ sudo apt-get install ros-{DISTRO}-teleop-twist-keyboard

 ``teleop_twist_keyboard`` 发布 Twist 消息的默认话题是 ``/cmd_vel``，但你可以重映射该
 话题，以便使用桥接中使用的话题：

 .. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash
        $ ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/model/vehicle_blue/cmd_vel
        This node takes keypresses from the keyboard and publishes them
        as Twist messages. It works best with a US keyboard layout.
        ---------------------------
        Moving around:
           u    i    o
           j    k    l
           m    ,    .

        For Holonomic mode (strafing), hold down the shift key:
        ---------------------------
           U    I    O
           J    K    L
           M    <    >

        t : up (+z)
        b : down (-z)

        anything else : stop

        q/z : increase/decrease max speeds by 10%
        w/x : increase/decrease only linear speed by 10%
        e/c : increase/decrease only angular speed by 10%

        CTRL-C to quit

        currently:      speed 0.5       turn 1.0

3 在 ROS 2 中可视化激光雷达数据
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

这个差速驱动机器人带有一个激光雷达。
要把 Gazebo 生成的数据发送到 ROS 2，你需要启动另一个桥接。
这里激光雷达的数据由 Gazebo Transport 话题 ``/lidar2`` 提供，你将在桥接中重映射它。
该话题将以 ``/lidar_scan`` 的名字提供：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash
        $ ros2 run ros_gz_bridge parameter_bridge /lidar2@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan --ros-args -r /lidar2:=/laser_scan

要在 ROS 2 中可视化激光雷达的数据，你可以使用 Rviz2：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash
        $ rviz2

然后你需要配置 ``fixed frame``：

.. image:: Image/fixed_frame.png

接着点击“Add”按钮，添加一个显示项来可视化激光雷达：

.. image:: Image/add_lidar.png

现在你应该能在 Rviz2 中看到激光雷达的数据了：

.. image:: Image/rviz2.png

小结
----

在本教程中，你使用 Gazebo 启动了一个机器人仿真，启动了
与执行器和传感器相关的桥接，可视化了来自传感器的数据，并让一个差速驱动机器人运动起来。
