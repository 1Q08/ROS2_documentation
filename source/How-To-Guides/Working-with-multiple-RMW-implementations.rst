.. redirect-from::

    Working-with-multiple-RMW-implementations
    Guides/Working-with-multiple-RMW-implementations
    Tutorials/Working-with-multiple-RMW-implementations

使用多种 ROS 2 中间件实现
=========================

.. contents:: 目录
   :depth: 2
   :local:

本页解释默认的 RMW 实现，以及如何指定一个替代实现。

前提条件
--------

你应该已经阅读过 :doc:`DDS 和 ROS 中间件实现页面 <../Concepts/Intermediate/About-Different-Middleware-Vendors>`。

指定 RMW 实现
-------------

要使用多种可用的 RMW 实现，你必须已经安装 ROS 2 二进制文件
以及特定 RMW 实现所需的任何额外依赖，
或者从源码构建 ROS 2 并在工作空间中包含多种 RMW 实现
（如果编译时依赖得到满足，RMW 实现默认会被包含在构建中）。
参见 :doc:`安装 RMW 实现 <../Installation/RMW-Implementations>`。

----

C++ 和 Python 节点都支持一个环境变量 ``RMW_IMPLEMENTATION``，
它允许用户在运行 ROS 2 应用程序时选择要使用的 RMW 实现。

用户可以将此变量设置为特定的实现标识符，
例如 ``rmw_cyclonedds_cpp``、``rmw_fastrtps_cpp``、``rmw_connextdds`` 或 ``rmw_gurumdds_cpp``。

例如，要使用 Connext RMW 实现运行 C++ talker 和 Python listener 的演示：

.. tabs::

  .. group-tab:: Linux


    在一个终端中运行：

    .. code-block:: console

       $ RMW_IMPLEMENTATION=rmw_connextdds ros2 run demo_nodes_cpp talker

    在另一个终端中运行：

    .. code-block:: console

       $ RMW_IMPLEMENTATION=rmw_connextdds ros2 run demo_nodes_py listener

  .. group-tab:: macOS

    在一个终端中运行：

    .. code-block:: console

       $ RMW_IMPLEMENTATION=rmw_connextdds ros2 run demo_nodes_cpp talker

    在另一个终端中运行：

    .. code-block:: console

       $ RMW_IMPLEMENTATION=rmw_connextdds ros2 run demo_nodes_py listener

  .. group-tab:: Windows

    在一个终端中运行：

    .. code-block:: console

       $ set RMW_IMPLEMENTATION=rmw_connextdds
       $ ros2 run demo_nodes_cpp talker

    在另一个终端中运行：

    .. code-block:: console

       $ set RMW_IMPLEMENTATION=rmw_connextdds
       $ ros2 run demo_nodes_py listener

向工作空间添加 RMW 实现
-----------------------

可以通过安装必要的依赖并重新构建工作空间，
将额外的 DDS 和 RMW 实现添加到你的工作空间中。
有关安装可用 DDS 选项的更多信息，请参见
:doc:`RMW 实现 <../Installation/RMW-Implementations>` 页面。

假设你在构建 ROS 2 工作空间时只安装了 Fast DDS，
因此只构建了 Fast DDS RMW 实现。
在你上次构建工作空间时，任何其他 RMW 实现包
（例如 ``rmw_connextdds``）很可能无法找到相关 DDS 实现的安装位置。
如果你随后安装了额外的 DDS 实现（例如 Connext），
你需要重新触发在构建 Connext RMW 实现时发生的 Connext 安装检查。
你可以通过在下次构建工作空间时指定 ``--cmake-clean-cache`` 标志来实现，
然后你应该会看到该 RMW 实现包为
新安装的 DDS 实现进行了构建。

使用 ``--cmake-clean-cache`` 选项在添加了额外 RMW 实现的情况下
"重新构建"工作空间时，可能会遇到构建
抱怨默认 RMW 实现发生变化的问题。
要解决这个问题，你可以使用 ``RMW_IMPLEMENTATION`` CMake 参数
将默认实现设置回之前的值，
或者删除那些抱怨的包的构建文件夹，
并使用 ``--packages-start <package name>`` 继续构建。

故障排查
--------

检查当前的 RMW
^^^^^^^^^^^^^^

要检查当前正在使用的 RMW，只需检查 ``RMW_IMPLEMENTATION`` 环境变量。
在 Linux 系统上，``printenv`` 会打印完整的环境变量列表。
其他操作系统查看环境变量的方式会有所不同。
如果环境变量中没有 ``RMW_IMPLEMENTATION``，
可以放心地假设你正在使用 ROS 发行版的默认值，
否则当前的 RMW 就是所列出的值。
每个 ROS 发行版的默认 RMW 可以在
`REP-2000 <https://reps.openrobotics.org/rep-2000/#platforms-by-distribution>`_ 中找到。

确保使用特定的 RMW 实现
^^^^^^^^^^^^^^^^^^^^^^^

如果 ``RMW_IMPLEMENTATION`` 环境变量被设置为一个未安装支持的 RMW 实现，
且你只安装了一种实现，你会看到类似以下的错误消息：

.. code-block:: bash

   Expected RMW implementation identifier of 'rmw_connextdds' but instead found 'rmw_fastrtps_cpp', exiting with 102.

如果你安装了多种 RMW 实现的支持，
而请求使用一种未安装的实现，你会看到类似以下的内容：

.. code-block:: bash

   Error getting RMW implementation identifier / RMW implementation not installed (expected identifier of 'rmw_connextdds'), exiting with 1.

如果出现这种情况，请仔细检查你的 ROS 2 安装是否包含
你在 ``RMW_IMPLEMENTATION`` 环境变量中指定的 RMW 实现的支持。

如果你想在 RMW 实现之间切换，请确认 ROS 2 守护进程
没有使用之前的 RMW 实现运行，
以避免节点与 ``ros2 node`` 等命令行工具之间出现任何问题。
例如，如果你运行：

.. code-block:: bash

   RMW_IMPLEMENTATION=rmw_connextdds ros2 run demo_nodes_cpp talker

以及

.. code-block:: console

   $ ros2 node list

它将生成一个使用 Fast DDS 实现的守护进程：

.. code-block:: bash

   21318 22.0  0.6 535896 55044 pts/8    Sl   16:14   0:00 /usr/bin/python3 /opt/ros/{DISTRO}/bin/_ros2_daemon --rmw-implementation rmw_fastrtps_cpp --ros-domain-id 0

即使你再次使用正确的 RMW 实现运行命令行工具，
守护进程的 RMW 实现也不会改变，并且 ROS 2 命令行工具会失败。

要解决这个问题，只需停止守护进程：

.. code-block:: console

   $ ros2 daemon stop

然后使用正确的 RMW 实现重新运行 ROS 2 命令行工具。

OSX 上的 RTI Connext：由于共享内存内核设置不足而失败
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你在 OSX 上运行 RTI Connext 时收到类似以下的错误消息：

.. code-block:: console

   [D0062|ENABLE]DDS_DomainParticipantPresentation_reserve_participant_index_entryports:!enable reserve participant index
   [D0062|ENABLE]DDS_DomainParticipant_reserve_participant_index_entryports:Unusable shared memory transport. For a more in-   depth explanation of the possible problem and solution, please visit https://community.rti.com/kb/osx510.

此错误是由于操作系统允许的共享内存段数量或大小不足引起的。
结果是 ``DomainParticipant`` 无法分配足够的资源并计算其参与者索引，
从而导致该错误。

你可以临时或永久地增加机器的共享内存资源。

要临时增加这些设置，你可以以 root 用户身份运行以下命令：

.. code-block:: console

   $ /usr/sbin/sysctl -w kern.sysv.shmmax=419430400
   $ /usr/sbin/sysctl -w kern.sysv.shmmin=1
   $ /usr/sbin/sysctl -w kern.sysv.shmmni=128
   $ /usr/sbin/sysctl -w kern.sysv.shmseg=1024
   $ /usr/sbin/sysctl -w kern.sysv.shmall=262144

要永久增加这些设置，你需要编辑或创建文件 ``/etc/sysctl.conf``。
创建或编辑此文件需要 root 权限。
你可以将以下行添加到现有的 ``etc/sysctl.conf`` 文件中，
或者创建包含以下行的 ``/etc/sysctl.conf``：

.. code-block:: bash

   kern.sysv.shmmax=419430400
   kern.sysv.shmmin=1
   kern.sysv.shmmni=128
   kern.sysv.shmseg=1024
   kern.sysv.shmall=262144

修改此文件后，你需要重启机器才能使更改生效。

此解决方案改编自 RTI Connext 社区论坛。
请参见 `原始帖子 <https://community.rti.com/kb/osx510>`__ 获取更详细的解释。
