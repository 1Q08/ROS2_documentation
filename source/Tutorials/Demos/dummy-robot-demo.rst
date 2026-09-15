.. redirect-from::

    dummy-robot-demo
    Tutorials/dummy-robot-demo

使用虚拟机器人进行试验
======================

在本演示中，我们展示一个简单的演示机器人，涵盖从发布关节状态、发布模拟激光数据，直到在 RViz 中的地图上可视化机器人模型的所有组件。

启动演示
--------

我们假设你的 ROS 2 安装目录为 ``~/ros2_ws``。
请根据你的平台更改相应目录。

为了启动该演示，我们执行 demo bringup 启动文件；我们将在下一节中更详细地解释它。
你应该会在终端中看到类似以下内容的输出：

.. code-block:: console

   $ source ~/ros2_ws/install/setup.bash
   $ ros2 launch dummy_robot_bringup dummy_robot_bringup.launch.py
   [INFO] [launch]: process[dummy_map_server-1]: started with pid [25812]
   [INFO] [launch]: process[robot_state_publisher-2]: started with pid [25813]
   [INFO] [launch]: process[dummy_joint_states-3]: started with pid [25814]
   [INFO] [launch]: process[dummy_laser-4]: started with pid [25815]
   Initialize urdf model from file: /home/mikael/work/ros2/bouncy_ws/install_debug_isolated/dummy_robot_bringup/share/dummy_robot_bringup/launch/single_rrbot.urdf
   Parsing robot urdf xml string.
   Link single_rrbot_link1 had 1 children
   Link single_rrbot_link2 had 1 children
   Link single_rrbot_link3 had 2 children
   Link single_rrbot_camera_link had 0 children
   Link single_rrbot_hokuyo_link had 0 children
   got segment single_rrbot_camera_link
   got segment single_rrbot_hokuyo_link
   got segment single_rrbot_link1
   got segment single_rrbot_link2
   got segment single_rrbot_link3
   got segment world
   Adding fixed segment from world to single_rrbot_link1
   Adding moving segment from single_rrbot_link1 to single_rrbot_link2
   [INFO] [dummy_laser]: angle inc:    0.004363
   [INFO] [dummy_laser]: scan size:    1081
   [INFO] [dummy_laser]: scan time increment:  0.000028
   Adding moving segment from single_rrbot_link2 to single_rrbot_link3
   Adding fixed segment from single_rrbot_link3 to single_rrbot_camera_link
   Adding fixed segment from single_rrbot_link3 to single_rrbot_hokuyo_link

如果你现在在新终端中打开 RViz2，就会看到你的机器人。
🎉

.. code-block:: console

   $ source <ROS2_INSTALL_FOLDER>/setup.bash
   $ rviz2

这会启动 RViz2。
假设你的 dummy_robot_bringup 仍处于启动状态，现在你可以添加 TF 显示插件，并将全局坐标系配置为 ``world``。
完成之后，你应该会看到类似的画面：


.. image:: images/rviz-dummy-robot.png


发生了什么？
^^^^^^^^^^^^

如果你仔细查看该启动文件，会发现我们同时启动了若干节点。


* dummy_map_server
* dummy_laser
* dummy_joint_states
* robot_state_publisher

前两个软件包相对简单。
``dummy_map_server`` 会以周期性更新不断发布空地图。
``dummy_laser`` 基本上做同样的事：发布模拟的激光扫描数据。

``dummy_joint_states`` 节点会发布模拟的关节状态数据。
由于我们发布的是一个只有两个关节的简单 RRbot，该节点会为这两个关节发布关节状态值。

``robot_state_publisher`` 承担了真正有趣的工作。
它解析给定的 URDF 文件，提取机器人模型，并监听传入的关节状态。
借助这些信息，它会为我们的机器人发布 TF 值，我们则在 RViz 中将这些值可视化。

太棒了！
