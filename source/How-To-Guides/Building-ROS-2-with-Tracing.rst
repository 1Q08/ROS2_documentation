.. redirect-from::

    How-To-Guides/Building-ROS-2-with-Tracing-Instrumentation

使用 tracing 构建 ROS 2
=======================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 源代码中包含追踪插桩（tracing instrumentation），而且 ROS 2 的 Linux 安装将 LTTng 追踪器作为依赖项包含在内。
因此，在 Linux 上 ROS 2 可以开箱即用地被追踪。

不过，也可以从源代码构建 ROS 2 以移除追踪点或完全移除插桩。
本指南演示如何做到这一点。
更多信息请参见 `该仓库 <https://github.com/ros2/ros2_tracing>`__。

.. note::

   本指南仅适用于 Linux 系统。

先决条件
--------

设置你的系统以从源代码构建 ROS 2。
更多信息请参见 :doc:`源代码安装页面 <../Installation/Alternatives/Ubuntu-Development-Setup>`。

构建配置
--------

ROS 2 追踪插桩分为两个组件：函数插桩和追踪点。
首先，ROS 2 核心包（例如 ``rclcpp``）调用 ``tracetools`` 包提供的函数。
然后，该函数触发一个追踪点，如果该追踪点在运行期被启用，它就会记录数据。

默认情况下，如果追踪器没有被\ `配置为追踪，或者追踪点未被启用 <https://github.com/ros2/ros2_tracing#tracing>`__，它们实际上对执行几乎没有影响。
不过，追踪点仍然可以通过 CMake 选项移除。
此外，函数可以通过 CMake 选项被完全移除，这意味着追踪点也会被移除。

在无追踪点的情况下构建
^^^^^^^^^^^^^^^^^^^^^^

此步骤取决于你是 :doc:`从源代码构建 ROS 2 <../Installation/Alternatives/Ubuntu-Development-Setup>` 还是使用 ROS 2 二进制文件（:doc:`deb 包 <../Installation/Ubuntu-Install-Debs>` 或 :doc:`二进制归档 <../Installation/Alternatives/Ubuntu-Install-Binary>`）。
要移除追踪点，请（重新）构建 ``tracetools`` 并将 ``TRACETOOLS_TRACEPOINTS_EXCLUDED`` CMake 选项设置为 ``ON``：

.. tabs::

  .. group-tab:: 源代码安装

    .. code-block:: console

       $ cd ~/ros2_{DISTRO}
       $ colcon build --packages-select tracetools --cmake-clean-cache --cmake-args -DTRACETOOLS_TRACEPOINTS_EXCLUDED=ON

  .. group-tab:: 二进制安装

    将 ``ros2_tracing`` 仓库克隆到你的工作空间并构建：

    .. code-block:: console

       $ cd ~/ws
       $ git clone https://github.com/ros2/ros2_tracing.git -b {DISTRO} src/ros2_tracing
       $ colcon build --packages-select tracetools --cmake-args -DTRACETOOLS_TRACEPOINTS_EXCLUDED=ON

在无插桩的情况下构建
^^^^^^^^^^^^^^^^^^^^

要完全移除追踪点和函数调用，请 :doc:`从源代码构建 ROS 2 <../Installation/Alternatives/Ubuntu-Development-Setup>` 并将 ``TRACETOOLS_DISABLED`` CMake 选项设置为 ``ON``：

.. code-block:: console

   $ cd ~/ros2_{DISTRO}
   $ colcon build --cmake-args -DTRACETOOLS_DISABLED=ON --no-warn-unused-cli

验证
----

验证追踪已被禁用：

.. code-block:: console

   $ cd ~/ws
   $ source install/setup.bash
   $ ros2 run tracetools status

它应该打印出：

.. tabs::

  .. group-tab:: 无追踪点

    .. code-block:: bash

       Tracing disabled

  .. group-tab:: 无插桩

    .. code-block:: bash

       Tracing disabled through configuration

如果打印出其他内容，那么说明出了问题。
