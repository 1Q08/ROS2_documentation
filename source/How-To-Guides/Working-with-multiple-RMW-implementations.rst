.. redirect-from::

    Working-with-multiple-RMW-implementations
    Guides/Working-with-multiple-RMW-implementations
    Tutorials/Working-with-multiple-RMW-implementations

使用多个 ROS 2 中间件实现
=========================

.. contents:: 目录
   :depth: 2
   :local:

本页说明默认的 RMW 实现，以及如何指定另一种实现。

前提条件
--------

你应该已经阅读过 :doc:`DDS 与 ROS 中间件实现页面 <../Concepts/Intermediate/About-Different-Middleware-Vendors>`。

指定 RMW 实现
-------------

要能够使用多个 RMW 实现，你必须已安装 ROS 2 二进制文件以及特定 RMW 实现所需的任何额外依赖项，或者在工作空间中从源码构建 ROS 2 并包含多个 RMW 实现（如果满足其编译期依赖项，RMW 实现默认会包含在构建中）。
参见 :doc:`安装 RMW 实现 <../Installation/RMW-Implementations>`。

----

C++ 和 Python 节点都支持环境变量 ``RMW_IMPLEMENTATION``，它允许用户在选择运行 ROS 2 应用程序时使用哪个 RMW 实现。

用户可以把该变量设置为某个具体的实现标识符，例如 ``rmw_cyclonedds_cpp``、``rmw_fastrtps_cpp``、``rmw_connextdds`` 或 ``rmw_gurumdds_cpp``。

例如，要使用 Connext RMW 实现来运行由 C++ talker 和 Python listener 组成的 talker 演示：

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

向你的工作空间中添加 RMW 实现
-----------------------------

通过安装必要的依赖项并重新构建工作空间，可以向你的工作空间中添加额外的 DDS 与 RMW 实现。
关于安装可用 DDS 选项的更多信息，请参见 :doc:`RMW 实现 <../Installation/RMW-Implementations>` 页面。

假设你构建 ROS 2 工作空间时只安装了 Fast DDS，因此只构建了 Fast DDS RMW 实现。
上次构建工作空间时，任何其他 RMW 实现软件包（例如 ``rmw_connextdds``）很可能都找不到相关 DDS 实现的安装。
如果你之后又安装了额外的 DDS 实现（例如 Connext），就需要重新触发在构建 Connext RMW 实现时执行的 Connext 安装检查。
你可以在下次构建工作空间时指定 ``--cmake-clean-cache`` 标志来做到这一点，随后你应该会看到 RMW 实现软件包针对新安装的 DDS 实现进行了构建。

在使用 ``--cmake-clean-cache`` 选项并加入额外的 RMW 实现来“重新构建”工作空间时，可能会遇到构建报错称默认 RMW 实现发生了变化的情况。
要解决此问题，你可以用 ``RMW_IMPLEMENTATION`` CMake 参数把默认实现设置回原来的值，也可以删除报错的那些软件包的 build 文件夹，然后用 ``--packages-start <package name>`` 继续构建。

故障排查
--------

检查当前使用的 RMW
^^^^^^^^^^^^^^^^^^

要检查当前正在使用哪个 RMW，只需查看 ``RMW_IMPLEMENTATION`` 环境变量。
在 Linux 系统上，``printenv`` 会打印完整的环境变量列表。
其他操作系统会有各自查看环境变量的方式。
如果环境中没有 ``RMW_IMPLEMENTATION``，那么可以安全地假定你使用的是你的 ROS 发行版的默认值，否则当前 RMW 就是所列出的该值。
每个 ROS 发行版的默认 RMW 可以在 `REP-2000 <https://reps.openrobotics.org/rep-2000/#platforms-by-distribution>`_ 中找到。

确保使用特定的 RMW 实现
^^^^^^^^^^^^^^^^^^^^^^^

如果 ``RMW_IMPLEMENTATION`` 环境变量被设置为一个尚未安装其支持的 RMW 实现，并且你只安装了一个实现，你会看到类似下面的错误消息：

.. code-block:: bash

   Expected RMW implementation identifier of 'rmw_connextdds' but instead found 'rmw_fastrtps_cpp', exiting with 102.

如果你安装了多个 RMW 实现的支持，但请求使用其中一个未安装的实现，你会看到类似这样的内容：

.. code-block:: bash

   Error getting RMW implementation identifier / RMW implementation not installed (expected identifier of 'rmw_connextdds'), exiting with 1.

如果出现这种情况，请再次确认你的 ROS 2 安装包含你在 ``RMW_IMPLEMENTATION`` 环境变量中指定的 RMW 实现的支持。

如果你想在不同的 RMW 实现之间切换，请确认 ROS 2 守护进程没有以之前的 RMW 实现运行，以避免节点与诸如 ``ros2 node`` 之类的命令行工具之间出现问题。
例如，如果你运行：

.. code-block:: bash

   RMW_IMPLEMENTATION=rmw_connextdds ros2 run demo_nodes_cpp talker

以及

.. code-block:: console

   $ ros2 node list

它将会生成一个使用 Fast DDS 实现的守护进程：

.. code-block:: bash

   21318 22.0  0.6 535896 55044 pts/8    Sl   16:14   0:00 /usr/bin/python3 /opt/ros/{DISTRO}/bin/_ros2_daemon --rmw-implementation rmw_fastrtps_cpp --ros-domain-id 0

即使你再次用正确的 RMW 实现运行该命令行工具，守护进程的 RMW 实现也不会改变，ROS 2 命令行工具将会失败。

要解决此问题，只需停止守护进程：

.. code-block:: console

   $ ros2 daemon stop

然后用正确的 RMW 实现重新运行 ROS 2 命令行工具。

OSX 上的 RTI Connext：因共享内存内核设置不足而失败
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果在 OSX 上运行 RTI Connext 时收到类似下面的错误消息：

.. code-block:: console

   [D0062|ENABLE]DDS_DomainParticipantPresentation_reserve_participant_index_entryports:!enable reserve participant index
   [D0062|ENABLE]DDS_DomainParticipant_reserve_participant_index_entryports:Unusable shared memory transport. For a more in-   depth explanation of the possible problem and solution, please visit https://community.rti.com/kb/osx510.

该错误是由于操作系统允许的共享内存段数量或大小不足导致的。
因此，``DomainParticipant`` 无法分配足够的资源并计算其参与者索引，从而引发了该错误。

你可以临时或永久地增加机器的共享内存资源。

要临时增大这些设置，可以以 root 用户运行以下命令：

.. code-block:: console

   $ /usr/sbin/sysctl -w kern.sysv.shmmax=419430400
   $ /usr/sbin/sysctl -w kern.sysv.shmmin=1
   $ /usr/sbin/sysctl -w kern.sysv.shmmni=128
   $ /usr/sbin/sysctl -w kern.sysv.shmseg=1024
   $ /usr/sbin/sysctl -w kern.sysv.shmall=262144

要永久增大这些设置，你需要编辑或创建 ``/etc/sysctl.conf`` 文件。
创建或编辑该文件需要 root 权限。
可以把你现有的 ``etc/sysctl.conf`` 文件中加入这些行，或者创建 ``/etc/sysctl.conf`` 文件并写入以下内容：

.. code-block:: bash

   kern.sysv.shmmax=419430400
   kern.sysv.shmmin=1
   kern.sysv.shmmni=128
   kern.sysv.shmseg=1024
   kern.sysv.shmall=262144

修改该文件后，你需要重启机器才能使更改生效。

该解决方案改编自 RTI Connext 社区论坛。
更详细的说明请参见 `原帖 <https://community.rti.com/kb/osx510>`__。
