使用跟踪插桩构建 ROS 2
======================

.. contents:: 目录
   :depth: 2
   :local:

本指南介绍如何使用 ``ros2_tracing`` 提供的跟踪插桩构建 ROS 2。
更多信息请参见 `代码仓库 <https://github.com/ros2/ros2_tracing>`__。

插桩已包含在 ROS 2 源代码中。
然而，如果使用二进制文件或从源代码构建，默认情况下插桩实际上并不会触发跟踪点。
要获得跟踪点，需要安装 LTTng 跟踪器，然后需要从源代码（重新）构建部分 ROS 2。

.. note::

   本指南仅适用于 Linux 系统，并假定使用 Ubuntu。

前提条件
--------

设置好系统以便从源代码构建 ROS 2。
更多信息请参见 :doc:`源代码安装页面 <../Installation/Alternatives/Ubuntu-Development-Setup>`。

安装跟踪器
----------

安装 `LTTng 跟踪器 <https://lttng.org/docs>`__ 以及相关工具和依赖项。

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install -y lttng-tools liblttng-ust-dev python3-lttng python3-babeltrace babeltrace

这只会安装 LTTng 用户空间跟踪器，而不会安装 LTTng 内核跟踪器，因为跟踪 ROS 2 应用程序并不需要后者。

构建
----

此步骤取决于你是从源代码构建 ROS 2 还是使用 ROS 2 二进制文件。

使用源代码安装
^^^^^^^^^^^^^^

如果你在安装 LTTng 之前已经 :doc:`从源代码构建了 ROS 2 <../Installation/Alternatives/Ubuntu-Development-Setup>`，则需要至少重新构建到 ``tracetools`` 软件包：

.. code-block:: bash

   cd ~/ws
   colcon build --packages-up-to tracetools --cmake-force-configure

使用二进制安装
^^^^^^^^^^^^^^

如果你依赖 ROS 2 二进制文件（:doc:`deb 软件包 <../Installation/Ubuntu-Install-Debs>` 或 :doc:`“fat”压缩包 <../Installation/Alternatives/Ubuntu-Install-Binary>`），则需要将 ``ros2_tracing`` 仓库克隆到你的工作空间，并至少构建到 ``tracetools`` 软件包：

.. code-block:: bash

   cd ~/ws/src
   git clone https://github.com/ros2/ros2_tracing.git
   cd ../
   colcon build --packages-up-to tracetools

验证
----

获取并验证跟踪是否已启用：

.. code-block:: bash

   cd ~/ws
   source install/setup.bash
   ros2 run tracetools status

它应该输出：

.. code-block:: bash

   Tracing enabled

如果输出的是其他内容，那就说明出了问题。

禁用跟踪
--------

如果在构建 ``tracetools`` 时安装并找到了 LTTng 用户空间跟踪器，跟踪将自动启用。
或者，要从 ROS 2 中构建并完全移除跟踪点和跟踪插桩，请将 ``TRACETOOLS_DISABLED`` CMake 选项设置为 ``ON``：

.. code-block:: bash

   colcon build --cmake-args -DTRACETOOLS_DISABLED=ON --no-warn-unused-cli
