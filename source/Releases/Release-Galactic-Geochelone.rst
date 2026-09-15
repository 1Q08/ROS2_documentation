.. _galactic-release:

Galactic Geochelone（``galactic``）
===================================

.. toctree::
   :hidden:

   Galactic-Geochelone-Complete-Changelog

.. contents:: 目录
   :depth: 2
   :local:

*Galactic Geochelone* 是 ROS 2 的第七个发行版。
以下内容概述了 Galactic Geochelone 自上一个发行版以来的重要变更与特性亮点。
关于自 Foxy 以来的所有变更列表，请参阅 `long form changelog <Galactic-Geochelone-Complete-Changelog>`。

支持的平台
----------

Galactic Geochelone 根据 `the platform support tiers <../The-ROS2-Project/Platform-Support-Tiers>` 支持以下平台：

第 1 层级平台：

* Ubuntu 20.04 (Focal)：``amd64`` 和 ``arm64``
* Windows 10 (Visual Studio 2019)：``amd64``

第 2 层级平台：

* RHEL 8：``amd64``

第 3 层级平台：

* Ubuntu 20.04 (Focal)：``arm32``
* Debian Bullseye (11)：``amd64``、``arm64`` 和 ``arm32``
* OpenEmbedded Thud (2.6) / webOS OSE：``arm32`` 和 ``arm64``
* Mac macOS 10.14 (Mojave)：``amd64``

目标平台：

+--------+-----------------------+----------------------+----------------------+----------------+-----------------------+---------------------------+
|  架构  | Ubuntu Focal (20.04)  | Windows 10 (VS2019)  | RHEL 8               | macOS          | Debian Bullseye (11)  | OpenEmbedded / webOS OSE  |
+========+=======================+======================+======================+================+=======================+===========================+
| amd64  | 第 1 层级 [d][a][s]   | 第 1 层级 [a][s]     | 第 2 层级 [d][a][s]  | 第 3 层级 [s]  | 第 3 层级 [s]         |                           |
+--------+-----------------------+----------------------+----------------------+----------------+-----------------------+---------------------------+
| arm64  | 第 1 层级 [d][a][s]   |                      |                      |                | 第 3 层级 [s]         | 第 3 层级 [s]             |
+--------+-----------------------+----------------------+----------------------+----------------+-----------------------+---------------------------+
| arm32  | 第 3 层级 [s]         |                      |                      |                | 第 3 层级 [s]         | 第 3 层级 [s]             |
+--------+-----------------------+----------------------+----------------------+----------------+-----------------------+---------------------------+


以下指标说明了每个平台可用的交付机制。

\" \[d\] \" 发行版特定的（Debian、RPM 等）软件包将针对提交到 rosdistro 的软件包
为该平台提供。

\" \[a\] \" 二进制发行版以每个平台一个归档文件的形式提供，
其中包含 Galactic ROS 2 repos 文件[^10] 中的所有软件包。

\" \[s\] \" 从源代码编译。

中间件实现支持：

+--------------------------+-------------------------+---------------+----------------------------+------------------------------+
|         中间件库         |       中间件供应商      |    支持层级   |            平台            |             架构             |
+==========================+=========================+===============+============================+==============================+
|    rmw_cyclonedds_cpp*   |   Eclipse Cyclone DDS   |   第 1 层级   |          所有平台          |           所有架构           |
+--------------------------+-------------------------+---------------+----------------------------+------------------------------+
|     rmw_fastrtps_cpp     |    eProsima Fast-DDS    |   第 1 层级   |          所有平台          |           所有架构           |
+--------------------------+-------------------------+---------------+----------------------------+------------------------------+
|      rmw_connextdds      |       RTI Connext       |   第 1 层级   |  Ubuntu、Windows 和 macOS  |     除 arm64 外的所有架构    |
+--------------------------+-------------------------+---------------+----------------------------+------------------------------+
| rmw_fastrtps_dynamic_cpp |    eProsima Fast-DDS    |   第 2 层级   |          所有平台          |           所有架构           |
+--------------------------+-------------------------+---------------+----------------------------+------------------------------+
|     rmw_gurumdds_cpp     |  GurumNetworks GurumDDS |   第 3 层级   |      Ubuntu 和 Windows     |     除 arm32 外的所有架构    |
+--------------------------+-------------------------+---------------+----------------------------+------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持层级。例如，运行在第 2 层级平台上的
第 1 层级中间件实现只能获得第 2 层级支持。

最低语言要求：

- C++17
- Python 3.6

依赖项要求：

+------------+----------------------------+--------------------------------------------------------------------------------+
|            | 必需支持                   | 推荐支持                                                                       |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| 软件包     | Ubuntu Focal| Windows 10** | RHEL 8   | macOS**  | Debian Bullseye | OpenEmbedded**                         |
+============+=============+==============+==========+==========+=================+========================================+
| CMake      | 3.16.3      | 3.19.1       | 3.18.2   | 3.14.4   | 3.18.4          | 3.16.1 / 3.12.2****                    |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| EmPY       | 3.3.2                                                                                                       |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Gazebo     | 11.0.0*     | N/A          | N/A      | 11.0.0   | 11.0.0*         | N/A                                    |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Ignition   | Edifice*    | N/A          | N/A      | Edifice* | Edifice*        | N/A                                    |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Ogre       | 1.10*                                                              | N/A                                    |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| OpenCV     | 4.2.0       | 3.4.6*       | 3.4.6    | 4.2.0    | 4.5.1           | 4.1.0 / 3.2.0****                      |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| OpenSSL    | 1.1.1d      | 1.1.1i       | 1.1.1g   | 1.1.1f   | 1.1.1i          | 1.1.1d / 1.1.1b****                    |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Python     | 3.8.0       | 3.8.3        | 3.6.8    | 3.8.2    | 3.9.1           | 3.8.2 / 3.7.5****                      |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Qt         | 5.12.5      | 5.12.10      | 5.12.5   | 5.12.3   | 5.15.2          | 5.14.1 / 5.12.5****                    |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
|                                         | **仅 Linux 平台**                                                              |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| PCL        | 1.10.0      | N/A          | 1.11.1   | N/A      | 1.11.1          | 1.10.0                                 |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| **RMW DDS 中间件供应商**                                                                                                 |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Cyclone DDS| 0.8.x (Réplique)                                                                                            |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Fast-DDS   | 2.3.x                                                                                                       |
+------------+-------------+--------------+----------+----------+-----------------+----------------------------------------+
| Connext DDS| 5.3.1                      | N/A      | 5.3.1    | N/A                                                      |
+------------+----------------------------+----------+----------+----------------------------------------------------------+
| Gurum DDS  | 2.7.x                      | N/A                                                                            |
+------------+----------------------------+--------------------------------------------------------------------------------+

\" \* \" 表示这不是上游版本（即官方操作系统仓库中可用的版本），
而是由 OSRF 或社区分发的软件包（在自定义仓库中构建并分发的软件包）。

\" \*\* \" 滚动发行版在其生命周期内会看到这些依赖项的多个版本变更。
此处显示的 OpenEmbedded 版本是 3.1 Dunfell 发行系列提供的版本；
其他受支持的发行系列提供的版本在此列出：
<https://github.com/ros/meta-ros/wiki/Package-Version-Differences> 。
请注意，某个 ROS 发行版所支持的 OpenEmbedded 发行系列会在其支持时间范围内
发生变化，这遵循此处所示的 OpenEmbedded 支持政策：
<https://github.com/ros/meta-ros/wiki/Policies#openembedded-release-series-support>
。但它始终会由至少一个稳定的 OpenEmbedded 发行系列支持。

\" \*\*\*\* \" webOS OSE 提供了这一不同的版本。

本文档仅记录某个 ROS 发行版首次发布时的版本，
不会随着依赖项的演进更新。因此这些版本是一个低水位线。

依赖项使用的软件包管理器：

- Ubuntu、Debian：apt
- Windows：Chocolatey、pip
- macOS：Homebrew、pip
- RHEL：dnf
- OpenEmbedded：opkg

构建系统支持：

- ament_cmake
- cmake
- setuptools

安装
----

`安装 Galactic Geochelone <../../galactic/Installation.html>`__

此 ROS 2 发行版中的新特性
-------------------------

能够为每个日志记录器指定日志级别
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

现在可以在命令行上为不同的日志记录器指定不同的日志级别：

.. code-block:: console

   $ ros2 run demo_nodes_cpp talker --ros-args --log-level WARN --log-level talker:=DEBUG

上述命令将全局日志级别设置为 WARN，但将 talker 节点消息的日志级别设置为 DEBUG。
``--log-level`` 命令行选项可以传入任意次数，从而为每个日志记录器设置不同的日志级别。

能够通过环境变量配置日志目录
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

现在可以通过两个环境变量来配置日志目录：``ROS_LOG_DIR`` 和 ``ROS_HOME``。
其逻辑如下：

* 如果设置了 ``ROS_LOG_DIR`` 且不为空，则使用 ``$ROS_LOG_DIR``。
* 否则，使用 ``$ROS_HOME/log``；如果未设置 ``ROS_HOME`` 或它为空，则使用 ``~/.ros``。

因此默认值保持不变：``~/.ros/log``。

相关 PR：`ros2/rcl_logging#53 <https://github.com/ros2/rcl_logging/pull/53>`_ 和 `ros2/launch#460 <https://github.com/ros2/launch/pull/460>`_。

例如：

.. code-block:: bash

  ROS_LOG_DIR=/tmp/foo ros2 run demo_nodes_cpp talker

会将所有日志放在 ``/tmp/foo`` 中。

.. code-block:: bash

  ROS_HOME=/path/to/home ros2 run demo_nodes_cpp talker

会将所有日志放在 ``/path/to/home/log`` 中。

能够在 CMake 之外调用 ``rosidl`` 管道
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

现在可以直接在 CMake 之外调用 ``rosidl`` 接口生成管道。
源代码生成器和接口定义转换器可以通过统一的命令行接口访问。

例如，给定某个 ``demo`` 软件包中的 ``Demo`` 消息如下：

.. code-block:: console

  $ mkdir -p demo/msg
  $ cd demo
  $ cat << EOF > msg/Demo.msg
  std_msgs/Header header
  geometry_msgs/Twist twist
  geometry_msgs/Accel accel
  EOF

就可以轻松生成 C、C++ 和 Python 支持源代码：

.. code-block:: console

  $ rosidl generate -o gen -t c -t cpp -t py -I$(ros2 pkg prefix --share std_msgs)/.. \
    -I$(ros2 pkg prefix --share geometry_msgs)/.. demo msg/Demo.msg

生成的源代码将放在 ``gen`` 目录中。

也可以将消息定义转换为其他格式，以便第三方代码生成工具使用：

.. code-block:: console

  $ rosidl translate -o gen --to idl -I$(ros2 pkg prefix --share std_msgs)/.. \
    -I$(ros2 pkg prefix --share geometry_msgs)/.. demo msg/Demo.msg

转换后的消息定义将放在 ``gen`` 目录中。

请注意，这些工具只生成源代码，并不负责构建 —— 构建仍由调用方负责。
这是朝着在 CMake 之外的构建系统中启用 ``rosidl`` 接口生成迈出的第一步。
有关更多参考和后续步骤，请参阅 `设计文档 <https://github.com/ros2/design/pull/310>`_。

在启动时从外部配置 QoS
^^^^^^^^^^^^^^^^^^^^^^

现在可以在启动时从外部配置节点的 QoS 设置。
QoS 设置 **不能** 在运行时配置；它们只能在启动时配置。
节点作者必须显式选择加入，才能启用启动时修改 QoS 设置的功能。
如果节点启用了该特性，那么在节点首次启动时就可以通过 ROS 参数设置 QoS 设置。

`此处可以找到 C++ 和 Python 的示例。 <https://github.com/ros2/demos/tree/a66f0e894841a5d751bce6ded4983acb780448cf/quality_of_service_demo#qos-overrides>`_

有关更多详情，请参阅 `设计文档获取更多详情 <http://design.ros2.org/articles/qos_configurability.html>`_。

请注意，通过注册回调来处理参数变更的用户代码应避免拒绝未知参数的更新。
在 Galactic 之前这被视为不良实践，但在启用了可外部配置的 QoS 之后，这样做会导致硬失败。

相关 PR：`ros2/rclcpp#1408 <https://github.com/ros2/rclcpp/pull/1408>`_ 和 `ros2/rclpy#635 <https://github.com/ros2/rclpy/pull/635>`_

可用的 Python point_cloud2 工具
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

用于在 Python 中操作 `PointCloud2 消息 <https://github.com/ros2/common_interfaces/blob/galactic/sensor_msgs/msg/PointCloud2.msg>`__ 的若干实用工具已被 `移植到 ROS 2 <https://github.com/ros2/common_interfaces/pull/128>`__。
这些工具允许从 PointCloud2 消息中获取点列表（``read_points`` 和 ``read_points_list``），以及从点列表创建 PointCloud2 消息（``create_cloud`` 和 ``create_cloud_xyz32``）。

下面是一个创建 PointCloud2 消息再将其读回的示例：

.. code-block:: python

  import sensor_msgs_py.point_cloud2
  from std_msgs.msg import Header

  pointlist = [[0.0, 0.1, 0.2]]

  pointcloud = sensor_msgs_py.point_cloud2.create_cloud_xyz32(Header(frame_id='frame'), pointlist)

  for point in sensor_msgs_py.point_cloud2.read_points(pointcloud):
      print(point)

RViz2 时间面板
^^^^^^^^^^^^^^

Rviz2 时间面板会显示当前的真实时间（Wall time）和 ROS 时间，以及已经流逝的真实时间和 ROS 时间，它已被 `移植到 RViz2 <https://github.com/ros2/rviz/pull/599>`__。
要启用时间面板，请点击 Panels -> Add New Panel，然后选择 "Time"。
将会出现如下所示的面板：

.. image:: rviz2-time-panel-2021-05-17.png

ros2 topic echo 可打印序列化数据
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在调试中间件问题时，查看 RMW 发送的原始序列化数据会很有帮助。
``ros2 topic echo`` 中添加了 `--raw 命令行标志 <https://github.com/ros2/ros2cli/pull/470>`__ 来显示这些数据。
要实际查看效果，请运行以下命令。

终端 1：

.. code-block:: console

  $ ros2 topic pub /chatter std_msgs/msg/String "data: 'hello'"

终端 2：

.. code-block:: console

  $ ros2 topic echo --raw /chatter
  b'\x00\x01\x00\x00\x06\x00\x00\x00hello\x00\x00\x00'
  ---

获取消息的 YAML 表示
^^^^^^^^^^^^^^^^^^^^

现在可以在 C++ 中使用 `to_yaml <https://github.com/ros2/rosidl/issues/523>`__ 函数获取所有消息的 YAML 表示。
下面是一个打印 YAML 表示的代码示例：

.. code-block:: c++

  #include <cstdio>

  #include <std_msgs/msg/string.hpp>

  int main()
  {
    std_msgs::msg::String msg;
    msg.data = "hello world";
    printf("%s", rosidl_generator_traits::to_yaml(msg).c_str());
    return 0;
  }

能够在运行时通过 ros2 命令加载参数文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 长期以来一直支持在启动时（通过命令行参数或 YAML 文件）指定参数值，并支持将当前参数导出到文件（通过 ``ros2 param dump``）。
Galactic 新增了使用 ``ros2 param load`` 动词从 YAML 文件 `在运行时加载参数值 <https://github.com/ros2/ros2cli/pull/590>`__ 的能力。
例如：

终端 1：

.. code-block:: console

  $ ros2 run demo_nodes_cpp parameter_blackboard

终端 2：

.. code-block:: console

  $ ros2 param set /parameter_blackboard foo bar  # 将 'foo' 参数设置为值 'bar'
  $ ros2 param dump /parameter_blackboard  # 将参数的当前值导出到 ./parameter_blackboard.yaml
  $ ros2 param set /parameter_blackboard foo different  # 将 'foo' 参数设置为值 'different'
  $ ros2 param load /parameter_blackboard ./parameter_blackboard.yaml  # 重新加载参数的先前状态，'foo' 恢复为 'bar'

检查 QoS 不兼容性的工具
^^^^^^^^^^^^^^^^^^^^^^^

基于新的 QoS 兼容性检查 API，``ros2doctor`` 和 ``rqt_graph`` 现在可以检测并报告发布者与订阅之间的 QoS 不兼容性。

给定一个发布者和一个具有 `不兼容 QoS 设置 <../../Concepts/Intermediate/About-Quality-of-Service-Settings>` 的订阅：

终端 1：

.. code-block:: console

  $ ros2 run demo_nodes_py talker_qos -n 1000  # 即 best_effort 发布者

终端 2：

.. code-block:: console

  $ ros2 run demo_nodes_py listener_qos --reliable -n 1000  # 即 reliable 订阅

``ros2doctor`` 报告：

.. code-block:: console

  $ ros2 doctor --report
  ~ ...
     QOS COMPATIBILITY LIST
  topic [type]            : /chatter [std_msgs/msg/String]
  publisher node          : talker_qos
  subscriber node         : listener_qos
  compatibility status    : ERROR: Best effort publisher and reliable subscription;
  ~ ...

而 ``rqt_graph`` 显示：

.. image:: images/rqt_graph-qos-incompatibility-2021-05-17.png

相关 PR：`ros2/ros2cli#621 <https://github.com/ros2/ros2cli/pull/621>`_、`ros-visualization/rqt_graph#61 <https://github.com/ros-visualization/rqt_graph/pull/61>`_

在参数文件中使用 launch 替换
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

就像 ROS 1 ``roslaunch`` 中的 ``rosparam`` 标签一样，``launch_ros`` 现在可以求值参数文件中的替换。

例如，给定如下所示的 ``parameter_file_with_substitutions.yaml``：

.. code-block:: yaml

  /**:
    ros__parameters:
      launch_date: $(command date)

将 ``allow_substs`` 设置为 ``True``，即可在 ``Node`` 启动时对替换进行求值：

.. code-block:: python

  import launch
  import launch_ros.parameter_descriptions
  import launch_ros.actions

  def generate_launch_description():
      return launch.LaunchDescription([
          launch_ros.actions.Node(
              package='demo_nodes_cpp',
              executable='parameter_blackboard',
              parameters=[
                  launch_ros.parameter_descriptions.ParameterFile(
                      param_file='parameter_file_with_substitutions.yaml',
                      allow_substs=True)
              ]
          )
      ])

XML launch 文件也支持这一功能。

.. code-block:: xml

  <launch>
    <node pkg="demo_nodes_cpp" exec="parameter_blackboard">
      <param from="parameter_file_with_substitutions.yaml" allow_substs="true"/>
    </node>
  </launch>

相关 PR：`ros2/launch_ros#168 <https://github.com/ros2/launch_ros/pull/168>`_

支持唯一网络流
^^^^^^^^^^^^^^

应用程序现在可以要求基于 UDP/TCP 和 IP 的 RMW 实现为发布者和订阅提供唯一的 *网络流* （即唯一的 `区分服务代码点 <https://tools.ietf.org/html/rfc2474>`_ 和/或唯一的 `IPv6 流标签 <https://tools.ietf.org/html/rfc6437>`_ 和/或 IP 包头部中的唯一端口），从而在支持该特性的网络架构（例如 5G 网络）中为这些 IP 流指定 QoS。

要查看实际效果，可以运行以下 C++ 示例（位于 `ros2/examples <https://github.com/ros2/examples>`__ 仓库中）：

终端 1：

.. code-block:: console

  $ ros2 run examples_rclcpp_minimal_publisher publisher_member_function_with_unique_network_flow_endpoints


终端 2：

.. code-block:: console

  $ ros2 run examples_rclcpp_minimal_subscriber subscriber_member_function_with_unique_network_flow_endpoints


更多参考请参阅 `唯一网络流设计文档 <https://github.com/ros2/design/pull/304>`_。

Rosbag2 新特性
^^^^^^^^^^^^^^

按时间分割录制
""""""""""""""

在 Foxy 中，录制时只能按照包的大小对包进行分割，现在还可以按照经过的时间进行分割。
以下命令会将包文件分割为 100 秒的块。

.. code-block:: console

  $ ros2 bag record --all --max-bag-duration 100

ros2 bag list
"""""""""""""

这个新命令会列出 rosbag2 所使用的各类已安装插件。

.. code-block:: console

  $ ros2 bag list storage
  rosbag2_v2
  sqlite3

  $ ros2 bag list converter
  rosbag_v2_converter


压缩实现是一个插件
""""""""""""""""""

在 Foxy 中，rosbag2 的压缩是硬编码为使用 Zstd 库实现的。
现在已重新设计，使压缩实现成为一个插件，无需修改 rosbag2 核心代码库即可替换。
``ros-galactic-rosbag2`` 自带的默认插件仍然是 Zstd 插件 —— 但现在可以发布并使用更多插件，而且通过有选择地安装软件包，可以将 Zstd 排除在安装之外。


按消息压缩
""""""""""

在 Foxy 中，可以在文件分割时自动压缩每个 rosbag 文件（按文件压缩），但现在还可以指定按消息压缩。

.. code-block:: console

  $ ros2 bag record --all --compression-format zstd --compression-mode message


Rosbag2 的 Python API
"""""""""""""""""""""

Galactic 中发布了新软件包 ``rosbag2_py``，它提供了 Python API。
该软件包是对 C++ API 的 ``pybind11`` 绑定。
在 Galactic 的初始发行版中，它尚未公开 ``rosbag2_cpp`` API 中可用的全部功能，但它是 ``ros2 bag`` 命令行工具唯一的连接方式，因此已经可以使用相当多的功能。


性能测试软件包与性能改进
""""""""""""""""""""""""

自 Foxy 发行版以来，我们对 rosbag2 开展了一次全面的性能分析项目。
完整的初始报告见 https://github.com/ros2/rosbag2/blob/galactic/rosbag2_performance/rosbag2_performance_benchmarking/docs/rosbag2_performance_improvements.pdf 。
软件包 ``rosbag2_performance_benchmarking`` 提供了运行性能分析的工具，尤其是针对录制的分析，这有助于我们维护并改进 rosbag2 的性能。

根据这份报告，我们开展了关键工作，将性能提升到更适用于实际机器人工作流的状态。
举一个关键指标 —— 在高带宽压力测试（200Mbps）中，Foxy 发行版最多会丢弃 70% 的消息，而 Galactic 版本的消息保留率约为 100%。
更多详情请参阅所链接的报告。

用于筛选话题的 ``--regex`` 和 ``--exclude`` 选项
""""""""""""""""""""""""""""""""""""""""""""""""

新的录制选项 ``--regex`` 和 ``--exclude`` 可以对包中录制的话题进行精细控制，而无需显式列出所有话题。
这些选项可以一起使用，也可以分开使用，还可以与 ``--all`` 结合使用。

以下命令只会录制名称中包含 "scan" 的话题。

.. code-block:: console

  $ ros2 bag record --regex "*scan*"

以下命令会录制除 ``/my_namespace/`` 中的话题之外的所有话题。

.. code-block:: console

  $ ros2 bag record --all --exclude "/my_namespace/*"


``ros2 bag reindex``
""""""""""""""""""""

ROS 2 的包由一个目录表示，而不是单个文件。
该目录包含一个 ``metadata.yaml`` 文件以及一个或多个包文件。
当 ``metadata.yaml`` 文件丢失或缺失时，``ros2 bag reindex $bag_dir`` 会尝试通过读取该目录中的所有包文件来重建它。

回放时间控制
""""""""""""

rosbag2 回放新增了控制功能 —— 暂停与恢复、更改速率以及播放下一跳。
截至 Galactic 发行版，这些控制仅以服务的形式在 rosbag2 播放器节点上提供。
我们正在开发将这些控制也以键盘操作的形式公开到 ``ros2 bag play`` 中，但在那之前，可以很容易地实现一个带按钮或键盘控制的用户应用程序来调用这些服务。

在一个终端中：

.. code-block:: console

  $ ros2 bag play my_bag

在另一个终端中：

.. code-block:: console

  $ ros2 service list -t
  /rosbag2_player/get_rate [rosbag2_interfaces/srv/GetRate]
  /rosbag2_player/is_paused [rosbag2_interfaces/srv/IsPaused]
  /rosbag2_player/pause [rosbag2_interfaces/srv/Pause]
  /rosbag2_player/play_next [rosbag2_interfaces/srv/PlayNext]
  /rosbag2_player/resume [rosbag2_interfaces/srv/Resume]
  /rosbag2_player/set_rate [rosbag2_interfaces/srv/SetRate]
  /rosbag2_player/toggle_paused [rosbag2_interfaces/srv/TogglePaused]

  $ ros2 service call /rosbag2_player/is_paused rosbag2_interfaces/IsPaused

暂停回放：

.. code-block:: console

  $ ros2 service call /rosbag2_player/pause rosbag2_interfaces/Pause

恢复回放：

.. code-block:: console

  $ ros2 service call /rosbag2_player/resume rosbag2_interfaces/Resume

将回放的暂停状态切换为其相反状态。
如果正在播放，则暂停。
如果已暂停，则恢复。

.. code-block:: console

  $ ros2 service call /rosbag2_player/toggle_paused rosbag2_interfaces/TogglePaused

获取当前回放速率：

.. code-block:: console

  $ ros2 service call /rosbag2_player/get_rate

设置当前回放速率（必须大于 0）：

.. code-block:: console

  $ ros2 service call /rosbag2_player/set_rate rosbag2_interfaces/SetRate "rate: 0.1"

播放接下来的单条消息（仅在暂停时有效）：

.. code-block:: console

  $ ros2 service call /rosbag2_player/play_next rosbag2_interfaces/PlayNext


回放会发布 /clock
"""""""""""""""""

Rosbag2 还可以在回放期间向 ``/clock`` 话题发布消息，从而控制“仿真时间”。
以下命令会以固定间隔发布时钟消息。

以默认的 40Hz 速率发布：

.. code-block:: console

  $ ros2 bag play my_bag --clock


以指定速率发布，例如 100Hz：

.. code-block:: console

  $ ros2 bag play my_bag --clock 100

自 Foxy 发行版以来的变更
------------------------

默认 RMW 更改为 Eclipse Cyclone DDS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 Galactic 开发过程中，ROS 2 技术指导委员会（TSC） `投票决定 <https://discourse.ros.org/t/ros-2-galactic-default-middleware-announced/18064>`__ 将默认的 ROS 中间件（RMW）改为 `Eclipse Foundation <https://www.eclipse.org>`__ 的 `Eclipse Cyclone DDS <https://github.com/eclipse-cyclonedds/cyclonedds>`__ 项目。
在没有任何配置更改的情况下，用户将默认获得 Eclipse Cyclone DDS。
Fast DDS 和 Connext 仍然是 Tier-1 支持的 RMW 厂商，用户可以通过 ``RMW_IMPLEMENTATION`` 环境变量自行选择使用其中之一。
更多信息请参阅 `使用多个 RMW 实现指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

Connext RMW 更改为 rmw_connextdds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Galactic 合并了一个新的 Connext RMW，名为 `rmw_connextdds <https://github.com/ros2/rmw_connextdds>`_。
该 RMW 具有更好的性能，并修复了旧 RMW ``rmw_connext_cpp`` 的许多问题。

测试与整体质量的大幅改进
^^^^^^^^^^^^^^^^^^^^^^^^

Galactic 包含许多修复竞态条件、填补内存泄漏以及修复用户所报告问题的更改。
除了这些更改之外，在 Galactic 开发期间我们还通过实施 `REP 2004 <https://reps.openrobotics.org/rep-2004/>`__ 共同努力提升了系统的整体质量。
``rclcpp`` 软件包及其所有依赖项（包括大多数 ROS 2 非 Python 核心软件包）通过以下方式提升到了 `质量等级 1 <https://reps.openrobotics.org/rep-2004/#quality-level-1>`__：

* 具有版本策略（QL1 要求 1）
* 具有文档化的变更控制流程（QL1 要求 2）
* 记录所有功能和公共 API（QL1 要求 3）
* 增加大量额外的测试（QL1 要求 4）：

  * 所有功能的系统测试
  * 所有公共 API 的单元测试
  * 每晚性能测试
  * 代码覆盖率达到 95%

* 使软件包的所有运行时依赖项的等级至少与软件包本身相同（QL1 要求 5）
* 支持所有 REP-2000 平台（QL1 要求 6）
* 具有漏洞披露政策（QL1 要求 7）

rmw
^^^

用于检查 QoS 配置文件兼容性的新 API
"""""""""""""""""""""""""""""""""""

``rmw_qos_profile_check_compatible`` 是一个用于检查两个 QoS 配置文件兼容性的新函数。

RMW 厂商应实现此 API，以便 ``rqt_graph`` 等工具中的 QoS 调试和自省功能正常工作。

相关 PR：`ros2/rmw#299 <https://github.com/ros2/rmw/pull/299>`_

ament_cmake
^^^^^^^^^^^

``ament_install_python_package()`` 现在会安装 Python egg
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

通过安装扁平的 Python egg，使用 ``ament_install_python_package()`` 安装的 Python 包可以通过 ``pkg_resources`` 和 ```importlib.metadata`` 等模块被发现。此外，还可以在 ``setup.cfg`` 文件中提供额外的元数据（包括入口点）。

相关 PR：`ament/ament_cmake#326 <https://github.com/ament/ament_cmake/pull/326>`_

``ament_target_dependencies()`` 可处理 SYSTEM 依赖项
""""""""""""""""""""""""""""""""""""""""""""""""""""

现在可以将某些软件包依赖项标记为 SYSTEM 依赖项，以应对外部代码中的警告。通常，SYSTEM 依赖项也会被排除在依赖项计算之外 —— 请谨慎使用。

相关 PR：`ament/ament_cmake#297 <https://github.com/ament/ament_cmake/pull/297>`_

nav2
^^^^

变更包括但不限于若干稳定性改进、新插件、接口变更以及代价地图过滤器。
完整列表请参阅 `迁移指南 <https://navigation.ros.org/migration/Foxy.html>`_

tf2_ros 中的 Python 代码拆分出来
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

过去位于 tf2_ros 中的 Python 代码已移至名为 tf2_ros_py 的独立软件包中。
任何依赖 tf2_ros 的现有 Python 代码都将继续正常工作，但这些软件包的 package.xml 应修改为对 tf2_ros_py 使用 ``exec_depend``。

tf2_ros 的 Python TransformListener 使用全局命名空间
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 的 ``TransformListener`` 现在会在全局命名空间中订阅 ``/tf`` 和 ``/tf_static``。
此前，它是在节点的命名空间中进行订阅的。
这意味着节点的命名空间将不再影响 ``/tf`` 和 ``/tf_static`` 的订阅。

例如：

.. code-block:: console

  $ ros2 run tf2_ros tf2_echo --ros-args -r __ns:=/test -- odom base_link

将订阅 ``/tf`` 和 ``/tf_static``，如 ``ros2 topic list`` 所示。

相关 PR：`ros2/geometry2#390 <https://github.com/ros2/geometry2/pull/390>`_

rclcpp
^^^^^^

spin_until_future_complete 模板参数的变更
"""""""""""""""""""""""""""""""""""""""""

``Executor::spin_until_future_complete`` 的第一个模板参数是 future 结果类型 ``ResultT``，并且该方法只接受 ``std::shared_future<ResultT>``。
为了接受其他类型的 future（例如 ``std::future``），该参数已改为 future 类型本身。

如果 ``spin_until_future_complete`` 调用依赖模板参数推导，则无需更改。
如果不是，以下是一个示例 diff：

.. code-block:: dpatch

   std::shared_future<MyResultT> future;
   ...
   -executor.spin_until_future_complete<MyResultT>(future);
   +executor.spin_until_future_complete<std::shared_future<MyResultT>>(future);


更多详情请参阅 `ros2/rclcpp#1160 <https://github.com/ros2/rclcpp/pull/1160>`_。
关于用户代码中所需更改的示例，请参阅 `ros-visualization/interactive_markers#72 <https://github.com/ros-visualization/interactive_markers/pull/72>`_。

默认 ``/clock`` 订阅 QoS 配置文件的变更
"""""""""""""""""""""""""""""""""""""""

默认值已从历史深度为 10 的可靠通信更改为历史深度为 1 的最佳努力通信。
参见 `ros2/rclcpp#1312 <https://github.com/ros2/rclcpp/pull/1312>`_。

Waitable API
""""""""""""

Waitable API 已修改，以避免与 ``MultiThreadedExecutor`` 相关的问题。
这只会影响实现自定义 waitable 的用户。
更多详情请参阅 `ros2/rclcpp#1241 <https://github.com/ros2/rclcpp/pull/1241>`_。

``rclcpp`` 日志宏的变更
"""""""""""""""""""""""
此前，日志宏容易受到 `格式化字符串攻击 <https://owasp.org/www-community/attacks/Format_string_attack>`_ 的影响，攻击者可以利用被求值的格式化字符串执行代码、读取栈内容或导致运行中的程序发生段错误。
为解决此安全问题，日志宏现在只接受字符串字面量作为其格式化字符串参数。

如果你之前有这样的代码：

.. code-block::

  const char *my_const_char_string format = "Foo";
  RCLCPP_DEBUG(get_logger(), my_const_char_string);

你现在应将其替换为：

.. code-block::

  const char *my_const_char_string format = "Foo";
  RCLCPP_DEBUG(get_logger(), "%s", my_const_char_string);

或：

.. code-block::

  RCLCPP_DEBUG(get_logger(), "Foo");


此更改去除了日志宏的一些便利性，因为不再接受 ``std::string``\s 作为格式参数。


如果你之前的代码没有任何格式参数，例如：

.. code-block::

  std::string my_std_string = "Foo";
  RCLCPP_DEBUG(get_logger(), my_std_string);

你现在应将其替换为：

.. code-block::

    std::string my_std_string = "Foo";
    RCLCPP_DEBUG(get_logger(), "%s", my_std_string.c_str());

.. note::
    如果你将 ``std::string`` 用作带格式参数的格式化字符串，那么将该字符串转换为 ``char *`` 并用作格式化字符串会产生格式化安全警告。这是因为编译器在编译时无法深入检查 ``std::string`` 来验证参数。为避免该安全警告，我们建议像上一个示例那样手动构建字符串，并在不传入任何格式参数的情况下使用它。

``std::stringstream`` 类型仍然可以作为流日志宏的参数使用。
更多详情请参阅 `ros2/rclcpp#1442 <https://github.com/ros2/rclcpp/pull/1442>`_。

参数类型现在默认是静态的
""""""""""""""""""""""""

此前，参数在被设置时可以更改其类型。
例如，如果某个参数被声明为整数，随后设置该参数的调用可能会将其类型改为字符串。
这种行为可能导致 bug，而且很少是用户想要的效果。
从 Galactic 开始，参数类型默认是静态的，尝试更改类型将会失败。
如果需要此前的动态行为，可以通过某种机制选择启用（见下方代码）。

.. code-block:: cpp

    // declare integer parameter with default value, trying to set it to a different type will fail.
    node->declare_parameter("my_int", 5);
    // declare string parameter with no default and mandatory user provided override.
    // i.e. the user must pass a parameter file setting it or a command line rule -p <param_name>:=<value>
    node->declare_parameter("string_mandatory_override", rclcpp::PARAMETER_STRING);
    // Conditionally declare a floating point parameter with a mandatory override.
    // Useful when the parameter is only needed depending on other conditions and no default is reasonable.
    if (mode == "modeA") {
        node->declare_parameter("conditionally_declare_double_parameter", rclcpp::PARAMETER_DOUBLE);
    }
    // You can also get the old dynamic typing behavior if you want:
    rcl_interfaces::msg::ParameterDescriptor descriptor;
    descriptor.dynamic_typing = true;
    node->declare_parameter("dynamically_typed_param", rclcpp::ParameterValue{}, descriptor);

更多详情请参见 https://github.com/ros2/rclcpp/blob/galactic/rclcpp/doc/notes_on_statically_typed_parameters.md 。

用于检查 QoS 配置文件兼容性的新 API
"""""""""""""""""""""""""""""""""""

``qos_check_compatible`` 是一个用于检查两个 QoS 配置文件兼容性的新函数。

相关 PR：`ros2/rclcpp#1554 <https://github.com/ros2/rclcpp/pull/1554>`_

rclpy
^^^^^

移除已弃用的 Node.set_parameters_callback
"""""""""""""""""""""""""""""""""""""""""

方法 ``Node.set_parameters_callback`` 在 `ROS Foxy 中已被弃用 <https://github.com/ros2/rclpy/pull/504>`_，并已在 `ROS Galactic 中移除 <https://github.com/ros2/rclpy/pull/633>`_。
请改用 ``Node.add_on_set_parameters_callback()``。
下面是一些使用它的示例代码。

.. code-block:: python

    import rclpy
    import rclpy.node
    from rcl_interfaces.msg import ParameterType
    from rcl_interfaces.msg import SetParametersResult


    rclpy.init()
    node = rclpy.node.Node('callback_example')
    node.declare_parameter('my_param', 'initial value')


    def on_parameter_event(parameter_list):
        for parameter in parameter_list:
            node.get_logger().info(f'Got {parameter.name}={parameter.value}')
        return SetParametersResult(successful=True)


    node.add_on_set_parameters_callback(on_parameter_event)
    rclpy.spin(node)

运行以下命令以查看参数回调的实际效果。

.. code-block::

    ros2 param set /callback_example my_param "Hello World"

参数类型现在默认是静态的
""""""""""""""""""""""""

在 Foxy 及更早版本中，设置参数的调用可能会更改其类型。
从 Galactic 开始，参数类型是静态的，默认情况下无法更改。
如果需要此前的行为，请在参数描述符中将 ``dynamic_typing`` 设为 true。
下面是一个示例。

.. code-block:: python

  import rclpy
  import rclpy.node
  from rcl_interfaces.msg import ParameterDescriptor

  rclpy.init()
  node = rclpy.node.Node('static_param_example')
  node.declare_parameter('static_param', 'initial value')
  node.declare_parameter('dynamic_param', 'initial value', descriptor=ParameterDescriptor(dynamic_typing=True))
  rclpy.spin(node)

运行以下命令以查看静态类型参数与动态类型参数的区别。

.. code-block:: console

    $ ros2 param set /static_param_example dynamic_param 42
    Set parameter successful
    $ ros2 param set /static_param_example static_param 42
    Setting parameter failed: Wrong parameter type, expected 'Type.STRING' got 'Type.INTEGER'

更多详情请参见 https://github.com/ros2/rclcpp/blob/galactic/rclcpp/doc/notes_on_statically_typed_parameters.md 。

用于检查 QoS 配置文件兼容性的新 API
"""""""""""""""""""""""""""""""""""

``rclpy.qos.qos_check_compatible`` 是一个 `新函数 <https://github.com/ros2/rclpy/pull/708>`_，用于检查两个 QoS 配置文件的兼容性。
如果两个配置文件兼容，则使用它们的发布者和订阅者将能够相互通信。

.. code-block:: python

    import rclpy.qos

    publisher_profile = rclpy.qos.qos_profile_sensor_data
    subscription_profile = rclpy.qos.qos_profile_parameter_events

    print(rclpy.qos.qos_check_compatible(publisher_profile, subscription_profile))

.. code-block:: console

    $ python3 qos_check_compatible_example.py
    (QoSCompatibility.ERROR, 'ERROR: Best effort publisher and reliable subscription;')

rclcpp_action
^^^^^^^^^^^^^

动作客户端目标响应回调签名的变更
""""""""""""""""""""""""""""""""

目标响应回调现在应接受指向目标句柄的共享指针，而不是 future。

例如 `example <https://github.com/ros2/examples/pull/291>`_，旧签名为：

.. code-block:: c++

   void goal_response_callback(std::shared_future<GoalHandleFibonacci::SharedPtr> future)

新签名：

.. code-block:: c++

   void goal_response_callback(GoalHandleFibonacci::SharedPtr goal_handle)

相关 PR：`ros2/rclcpp#1311 <https://github.com/ros2/rclcpp/pull/1311>`_

rosidl_typesupport_introspection_c
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从数组中获取元素的函数存在 API 破坏性变更
"""""""""""""""""""""""""""""""""""""""""

该函数的签名被更改，因为它在语义上与其他所有用于从数组或序列中获取元素的函数不一致。
这只会影响使用 introspection 类型支持的 rmw 实现作者。

更多详情请参阅 `ros2/rosidl#531 <https://github.com/ros2/rosidl/pull/531>`_。

rcl_lifecycle 与 rclcpp_lifecycle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RCL 的生命周期状态机新增 init API
"""""""""""""""""""""""""""""""""

``rcl_lifecycle`` 中的生命周期状态机经过修改，现在期望一个新引入的选项结构体，用于合并状态机的通用配置。
该选项结构体允许指示状态机是否应使用默认值初始化、其附带的服务是否处于活动状态，以及使用哪个分配器。

.. code-block:: c

  rcl_ret_t
  rcl_lifecycle_state_machine_init(
    rcl_lifecycle_state_machine_t * state_machine,
    rcl_node_t * node_handle,
    const rosidl_message_type_support_t * ts_pub_notify,
    const rosidl_service_type_support_t * ts_srv_change_state,
    const rosidl_service_type_support_t * ts_srv_get_state,
    const rosidl_service_type_support_t * ts_srv_get_available_states,
    const rosidl_service_type_support_t * ts_srv_get_available_transitions,
    const rosidl_service_type_support_t * ts_srv_get_transition_graph,
    const rcl_lifecycle_state_machine_options_t * state_machine_options);

RCL 的生命周期状态机存储分配器实例
""""""""""""""""""""""""""""""""""

上述选项结构体包含了用于初始化状态机的分配器实例。
该选项结构体以及其中包含的分配器都被存储在生命周期状态机内部。
作为直接结果，``rcl_lifecycle_fini function`` 不再在其 fini 函数中期望传入分配器，而是使用选项结构体中设置的分配器来释放其内部数据结构。

.. code-block:: c

  rcl_ret_t
  rcl_lifecycle_state_machine_fini(
    rcl_lifecycle_state_machine_t * state_machine,
    rcl_node_t * node_handle);

RCLCPP 的生命周期节点提供不实例化服务的选项
"""""""""""""""""""""""""""""""""""""""""""

为了在不暴露 ``change_state``、``get_state`` 等内部服务的情况下使用 rclcpp 的生命周期节点，生命周期节点的构造函数新增了一个参数，用于指示这些服务是否可用。
该布尔标志默认为 true，如果不需要，无需对现有 API 做任何改动。

.. code-block:: c++

  explicit LifecycleNode(
    const std::string & node_name,
    const rclcpp::NodeOptions & options = rclcpp::NodeOptions(),
    bool enable_communication_interface = true);

相关 PR：`ros2/rcl#882 <https://github.com/ros2/rcl/pull/882>`_ 和 `ros2/rclcpp#1507 <https://github.com/ros2/rclcpp/pull/1507>`_

rcl_lifecycle 与 rclcpp_lifecycle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

录制 - 按时间分割
"""""""""""""""""



已知问题
--------

ros2cli
^^^^^^^

在 Windows 上守护进程会拖慢 CLI
"""""""""""""""""""""""""""""""

作为变通方法，可以在不使用守护进程的情况下运行 CLI 命令，例如：

.. code-block:: console

  $ ros2 topic list --no-daemon


该问题由 `ros2/ros2cli#637 <https://github.com/ros2/ros2cli/issues/637>`_ 跟踪。

rqt
^^^

部分 rqt_bag 图标缺失
"""""""""""""""""""""

``rqt_bag`` 中缺少 “Zoom In”（放大）、“Zoom Out”（缩小）、“Zoom Home”（回到初始视图）和 “Toggle Thumbnails”（切换缩略图）的图标。
该问题在 `ros-visualization/rqt_bag#102 <https://github.com/ros-visualization/rqt_bag/issues/102>`_ 中被跟踪

大多数 rqt 工具在 Windows 上无法独立运行
""""""""""""""""""""""""""""""""""""""""

在 Windows 上“独立”启动 rqt 工具（例如 ``ros2 run rqt_graph rqt_graph``）通常无法正常工作。
变通方法是启动 rqt 容器进程（``rqt``），然后插入要使用的插件。

rviz2
^^^^^

RViz2 面板的关闭按钮为空白
""""""""""""""""""""""""""

每个 RViz2 面板的右上角都应包含一个 “X”，以便关闭该面板。
这些按钮确实存在，但在所有平台上它们内部的 “X” 都缺失了。
该问题正在 `ros2/rviz2#692 <https://github.com/ros2/rviz/issues/692>`__ 中被跟踪。

发行前的时间线
--------------

    Mon. 2021年3月22日 - Alpha
        对 ROS Core [1]_ 软件包进行初步测试与稳定化。

    Mon. 2021年4月5日 - Freeze
        对 Rolling Ridley 中的 ROS Core [1]_ 软件包进行 API 与功能冻结。
        注意这包括 ``rmw``，它是 ``ros_core`` 的递归依赖项。
        此时间点之后只应发布 bug 修复版本。
        新软件包可以独立发布。

    Mon. 2021年4月19日 - Branch
        从 Rolling Ridley 分支。
        ``rosdistro`` 重新开放接受 ROS Core [1]_ 软件包的 Rolling PR。
        Galactic 的开发从 ``ros-rolling-*`` 软件包转向 ``ros-galactic-*`` 软件包。

    Mon. 2021年4月26日 - Beta
        提供 ROS Desktop [2]_ 软件包的更新版本。
        呼吁进行广泛测试。

    Mon. 2021年5月17日 - RC
      发布候选（RC）软件包已构建。
        提供 ROS Desktop [2]_ 软件包的更新版本。

    Thu. 2021年5月20日 - Distro Freeze
        冻结 rosdistro。
        ``rosdistro`` 仓库上针对 Galactic 的 PR 将不会被合并（在发行公告后重新开放）。

    Sun. 2021年5月23日 - General Availability
      发布公告。
        ``rosdistro`` 重新开放接受 Galactic 的 PR。

.. [1] ``ros_core`` 变体在 `REP 2001 (ros-core) <https://reps.openrobotics.org/rep-2001/#ros-core>`_ 中有描述。
.. [2] ``desktop`` 变体在 `REP 2001 (desktop-variants) <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中有描述。
