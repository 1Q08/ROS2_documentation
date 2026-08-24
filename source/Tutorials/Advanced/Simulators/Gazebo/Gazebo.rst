.. redirect-from::

    Tutorials/Simulators/Ignition/Setting-up-a-Robot-Simulation-Ignition
    Tutorials/Advanced/Simulators/Ignition
    Tutorials/Advanced/Simulators/Gazebo

设置机器人仿真（Gazebo）
========================

**目标：** 使用 Gazebo 和 ROS 2 启动仿真

**教程级别：** 高级

**用时：** 5 分钟

.. contents:: 目录
   :depth: 2
   :local:


.. note::

   这些说明针对的是当前的 `Gazebo <https://gazebosim.org/>`__（以前称为 Ignition），而不是 `Gazebo Classic <https://classic.gazebosim.org/>`__。

前置条件
--------

你需要同时安装 ROS 2 和 Gazebo。

ROS 2
^^^^^

对于 ROS 2，你应该遵循 :doc:`ROS 2 安装说明 <../../../../Installation>`。

Gazebo
^^^^^^

Gazebo 和 ROS 支持不同的版本组合。

所有受支持的组合都可以在 `这里 <https://gazebosim.org/docs/harmonic/ros_installation#summary-of-compatible-ros-and-gazebo-combinations>`__ 查看。

`ROS REP-2000 <https://reps.openrobotics.org/rep-2000/>`__ 标准化了每个 ROS 发行版所对应的默认 Gazebo 版本。

如果你还没有在系统上安装某个版本的 Gazebo，可以按照 `安装说明 <https://gazebosim.org/docs/harmonic/ros_installation>`__ 来安装 Gazebo。

快速检查
--------

要验证你的 Gazebo 安装是否正确，请检查你是否能运行它：

.. code-block:: console

   $ gz sim

更多资源
--------

一旦 Gazebo 安装完成，并且通过上面的快速测试，你就可以转到 `Gazebo 教程 <https://gazebosim.org/docs/harmonic/tutorials>`__，尝试构建你自己的机器人了！

如果你使用的 Gazebo 版本与推荐版本不同，请务必使用下拉菜单选择正确的文档版本。

总结
----

在本教程中，你已经安装了 Gazebo 并设置好了工作空间，可以开始 `Gazebo 教程 <https://gazebosim.org/docs/harmonic/tutorials>`__。
