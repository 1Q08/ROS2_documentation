MVSim 入门
==========

**目标：** 以独立模式和 ROS 2 模式启动 MVSim 演示世界，并学习如何与仿真机器人交互。

**教程级别：** 高级

**时长：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

MVSim 自带一系列演示世界，用于展示多机器人仿真、传感器配置、地形类型、
人类角色、可选车辆和环境布局等不同功能。
你可以使用 ``mvsim`` CLI 将这些演示作为独立应用运行，
也可以作为 ROS 2 节点运行，通过标准 ROS 2 话题发布传感器数据并接收速度命令。

.. image:: Image/mvsim_demos_screenshot.png
   :alt: MVSim 演示截图

前提条件
--------

你应当已按照 :doc:`Installation-Ubuntu` 教程安装好 MVSim。

任务
----

1 使用独立 CLI 启动演示世界
^^^^^^^^^^^^^^^^^^^^^^^^^^^

MVSim 包含一个不需要 ROS 2 的独立启动器。
这对于快速测试世界文件或非 ROS 使用场景很有用。

启动 warehouse 演示：

.. code-block:: console

    $ mvsim launch ~/ros2_ws/src/mvsim/mvsim_tutorial/demo_warehouse.world.xml

如果你是从二进制软件包安装的，演示文件通常位于
``/opt/ros/{DISTRO}/share/mvsim/mvsim_tutorial/`` 下。

其他一些可以尝试的演示世界：

- ``demo_turtlebot_world.world.xml`` —— 带障碍物的经典 ROS 风格环境中的 TurtleBot3。
- ``demo_2robots.world.xml`` —— 两台机器人在家具块之间导航。
- ``demo_elevation_map.world.xml`` —— Jackal 机器人在带有高程数据的地形上行驶。
- ``demo_greenhouse.world.xml`` —— 复杂的温室环境，演示用于程序化内容的 XML 循环。

2 控制机器人
^^^^^^^^^^^^

世界启动后，你可以通过以下方式控制机器人：

- **键盘：** 按 W/S 前进/后退，A/D 向左/向右转向，按空格键停止。
  如果世界中有多个机器人，请先在 GUI 中点击某个机器人将其选中，然后再使用键盘控制。
- **游戏手柄：** 如果连接了游戏手柄，它会被自动检测到。

.. image:: Image/mvsim_gui_controls.jpg
   :alt: MVSim GUI 控制参考

GUI 还提供相机视角、仿真速度和可视化选项的控制。
你可以在 3D 窗口中切换正交/透视视图，并启用传感器数据的可视化。

3 使用 ROS 2 启动
^^^^^^^^^^^^^^^^^

要将 MVSim 作为 ROS 2 节点启动，请使用提供的 launch 文件：

.. code-block:: console

    $ source /opt/ros/{DISTRO}/setup.bash
    $ ros2 launch mvsim demo_warehouse.launch.py

这会启动仿真器，并为每辆车和每个传感器创建 ROS 2 话题。

4 查看 ROS 2 话题
^^^^^^^^^^^^^^^^^

在演示运行的情况下，打开一个新的终端并列出可用的话题：

.. code-block:: console

    $ ros2 topic list

你应该会看到类似下面这样的话题：

- ``/robot1/cmd_vel`` —— 发送 ``geometry_msgs/msg/Twist`` 命令来控制机器人。
- ``/robot1/odom`` —— 来自轮式编码器的里程计（``nav_msgs/msg/Odometry``）。
- ``/robot1/base_pose_ground_truth`` —— 完美的真值位姿。
- ``/robot1/<sensor_name>`` —— 各个传感器专用话题（例如，3D LiDAR 点云使用 ``/robot1/lidar1_points``，2D 扫描使用 ``/robot1/laser1``）。
- ``/tf`` 和 ``/tf_static`` —— 遵循 `REP-105 <https://www.ros.org/reps/rep-0105.html>`__ 的 TF2 变换（``map`` → ``odom`` → ``base_link``）。

你可以从命令行发送速度命令：

.. code-block:: console

    $ ros2 topic pub /robot1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 0.3}}"

或者使用 ``teleop_twist_keyboard`` 进行交互式控制：

.. code-block:: console

    $ ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/robot1/cmd_vel

5 在 RViz2 中可视化
^^^^^^^^^^^^^^^^^^^

你可以在 RViz2 中可视化 MVSim 的传感器数据。
某些 launch 文件包含 ``use_rviz`` 选项：

.. code-block:: console

    $ ros2 launch mvsim demo_warehouse.launch.py use_rviz:=True

或者，手动打开 RViz2，并为感兴趣的话题添加显示项（例如 ``LaserScan``、``PointCloud2``、``Image``、``Odometry``）。

.. image:: Image/mvsim_depth_camera_demo.png
   :alt: MVSim 深度相机可视化

6 无头模式
^^^^^^^^^^

对于没有显示器的 CI 流水线或远程服务器，MVSim 支持无头运行：

.. code-block:: console

    $ ros2 launch mvsim demo_warehouse.launch.py headless:=True

这会在不打开 GUI 窗口的情况下运行完整仿真。

概述
----

在本教程中，你以独立模式和 ROS 2 模式启动了 MVSim 演示世界。
你学习了如何使用键盘和 ROS 2 话题控制机器人、查看已发布的话题，以及在 RViz2 中可视化数据。
下一个教程将介绍如何自定义机器人和传感器来定义你自己的世界。
