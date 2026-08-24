.. _ImprovedDynamicDiscovery:

改进的动态发现
==============

**目标：** 本教程将展示如何使用改进的动态发现配置。

**教程级别：** 高级

**预计用时：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

概述
----

默认情况下，ROS 2 会尝试自动在同一子网上的所有主机上找到所有节点。
然而，可以使用以下选项来控制 ROS 2 的发现范围。

.. warning::

   ``rmw_zenoh`` **不支持** 这些环境变量（``ROS_AUTOMATIC_DISCOVERY_RANGE`` 和 ``ROS_STATIC_PEERS``）。
   如果你使用 ``rmw_zenoh`` 作为 RMW 实现，请参阅 `rmw_zenoh 配置文档 <https://github.com/ros2/rmw_zenoh?tab=readme-ov-file#configuration>`_，了解如何配置发现和通信行为。


配置参数
--------

* ``ROS_AUTOMATIC_DISCOVERY_RANGE``：控制 ROS 节点尝试发现彼此的范围。

   有效选项有：

   * ``SUBNET`` 是默认值，对于基于 DDS 的中间件，它意味着将发现任何通过组播可达的节点。
   * ``LOCALHOST`` 意味着节点只会尝试发现同一台机器上的其他节点。
   * ``OFF`` 意味着节点不会发现任何其他节点，即使是在同一台机器上。
   * ``SYSTEM_DEFAULT`` 意味着“不更改任何发现设置”。

* ``ROS_STATIC_PEERS``：一个以分号（``;``）分隔的地址列表，ROS 应尝试在这些地址上发现节点。
  这允许连接到特定机器上的节点（只要它们的发现范围未设置为 ``OFF``）。

这两个环境变量对于本地和远程节点的组合将启用并控制 ROS 2 通信发现范围。
以下表格展示了各种可能组合下的发现范围行为。

``X`` 表示节点 A 和 B 将不会互相发现并通信。
``O`` 表示节点 A 和 B 将互相发现并通信。

.. list-table:: 在同一主机上运行的节点 A 和 B
   :widths: 20 20 20 20 20 20 20 20 20
   :header-rows: 1

   * - 同一主机
     -
     -
     - 节点 B 设置
     -
     -
     -
     -
     -
   * -
     -
     -
     - 无静态对等节点
     -
     -
     - 有静态对等节点
     -
     -
   * -
     -
     -
     - Off
     - Localhost
     - Subnet
     - Off
     - Localhost
     - Subnet
   * - 节点 A 设置
     - 无静态对等节点
     - Off
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
   * -
     -
     - Localhost
     - ``X``
     - ``O``
     - ``O``
     - ``X``
     - ``O``
     - ``O``
   * -
     -
     - Subnet
     - ``X``
     - ``O``
     - ``O``
     - ``X``
     - ``O``
     - ``O``
   * -
     - 有静态对等节点
     - Off
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
   * -
     -
     - Localhost
     - ``X``
     - ``O``
     - ``O``
     - ``X``
     - ``O``
     - ``O``
   * -
     -
     - Subnet
     - ``X``
     - ``O``
     - ``O``
     - ``X``
     - ``O``
     - ``O``


.. list-table:: 在不同主机上运行的节点 A 和 B
   :widths: 20 20 20 20 20 20 20 20 20
   :header-rows: 1

   * - 不同主机
     -
     -
     - 节点 B 设置
     -
     -
     -
     -
     -
   * -
     -
     -
     - 无静态对等节点
     -
     -
     - 有静态对等节点
     -
     -
   * -
     -
     -
     - Off
     - Localhost
     - Subnet
     - Off
     - Localhost
     - Subnet
   * - 节点 A 设置
     - 无静态对等节点
     - Off
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
   * -
     -
     - Localhost
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``O``
     - ``O``
   * -
     -
     - Subnet
     - ``X``
     - ``X``
     - ``O``
     - ``X``
     - ``O``
     - ``O``
   * -
     - 有静态对等节点
     - Off
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
     - ``X``
   * -
     -
     - Localhost
     - ``X``
     - ``O``
     - ``O``
     - ``X``
     - ``O``
     - ``O``
   * -
     -
     - Subnet
     - ``X``
     - ``O``
     - ``O``
     - ``X``
     - ``O``
     - ``O``


示例
----

例如，以下命令将把 ROS 2 通信限制为仅与 localhost 和特定对等节点通信：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
        $ export ROS_STATIC_PEERS='192.168.0.1;remote.com'

      要在 shell 会话之间保持此设置，你可以将命令添加到 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST" >> ~/.bashrc
        $ echo "export ROS_STATIC_PEERS='192.168.0.1;remote.com'" >> ~/.bashrc

   .. group-tab:: macOS

      .. code-block:: console

        $ export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
        $ export ROS_STATIC_PEERS='192.168.0.1;remote.com'

      要在 shell 会话之间保持此设置，你可以将命令添加到 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST" >> ~/.bash_profile
        $ echo "export ROS_STATIC_PEERS='192.168.0.1;remote.com'" >> ~/.bash_profile

   .. group-tab:: Windows

      .. code-block:: console

        $ set ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
        $ set ROS_STATIC_PEERS=192.168.0.1;remote.com

      如果你想让此设置在 shell 会话之间永久生效，还要运行：

      .. code-block:: console

        $ setx ROS_AUTOMATIC_DISCOVERY_RANGE LOCALHOST
        $ setx ROS_STATIC_PEERS 192.168.0.1;remote.com
