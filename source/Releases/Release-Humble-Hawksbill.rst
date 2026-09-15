.. _humble-release:

Humble Hawksbill（``humble``）
==============================

.. toctree::
   :hidden:

   Humble-Hawksbill-Complete-Changelog

.. contents:: 目录
   :depth: 2
   :local:

*Humble Hawksbill* 是 ROS 2 的第八个发行版。
以下是自上一个发行版以来 Humble Hawksbill 中重要变更与特性的亮点。
有关自 Galactic 以来的所有变更列表，请参阅 `完整变更日志 <Humble-Hawksbill-Complete-Changelog>`_。

支持的平台
----------

Humble Hawksbill 按照 `平台支持层级 <../The-ROS2-Project/Platform-Support-Tiers>`_ 支持以下平台：

Tier 1 平台：

* Ubuntu 22.04 (Jammy)：``amd64`` 和 ``arm64``
* Windows 10 (Visual Studio 2019)：``amd64``

Tier 2 平台：

* RHEL 8：``amd64``

Tier 3 平台：

* Ubuntu 20.04 (Focal)：``amd64``
* macOS：``amd64``
* Debian Bullseye：``amd64``

目标平台：

+--------------+----------------------+---------------------+------------------+----------------------+------------+----------------------+------------------------------+
| Architecture | Ubuntu Jammy (22.04) | Windows 10 (VS2019) | RHEL 8           | Ubuntu Focal (20.04) | macOS      | Debian Bullseye (11) | OpenEmbedded / Yocto Project |
+==============+======================+=====================+==================+======================+============+======================+==============================+
| amd64        | Tier 1 [d][a][s]     | Tier 1 [a][s]       | Tier 2 [d][a][s] | Tier 3 [s]           | Tier 3 [s] | Tier 3 [s]           | Tier 3 [s]                   |
+--------------+----------------------+---------------------+------------------+----------------------+------------+----------------------+------------------------------+
| arm64        | Tier 1 [d][a][s]     |                     |                  | Tier 3 [s]           |            | Tier 3 [s]           | Tier 3 [s]                   |
+--------------+----------------------+---------------------+------------------+----------------------+------------+----------------------+------------------------------+
| arm32        | Tier 3 [s]           |                     |                  | Tier 3 [s]           |            | Tier 3 [s]           | Tier 3 [s]                   |
+--------------+----------------------+---------------------+------------------+----------------------+------------+----------------------+------------------------------+

以下标识说明了各平台可用的交付机制。

\" \[d\] \" 针对提交到 rosdistro 的软件包，将为其提供发行版专用（Debian、RPM 等）软件包。

\" \[a\] \" 二进制发行版为每个平台提供单个归档文件，其中包含 Humble ROS 2 repos 文件中的所有软件包[^11]。

\" \[s\] \" 从源代码编译。

中间件实现支持：

+--------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| Middleware Library       | Middleware Provider     | Support Level | Platforms                  | Architectures                 |
+==========================+=========================+===============+============================+===============================+
| rmw_fastrtps_cpp*        | eProsima Fast-DDS       | Tier 1        | All Platforms              | All Architectures             |
+--------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_cyclonedds_cpp       | Eclipse Cyclone DDS     | Tier 1        | All Platforms              | All Architectures             |
+--------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_connextdds           | RTI Connext             | Tier 1        | Ubuntu, Windows, and macOS | All Architectures except arm64|
+--------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-DDS       | Tier 2        | All Platforms              | All Architectures             |
+--------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_gurumdds_cpp         | GurumNetworks GurumDDS  | Tier 3        | Ubuntu and Windows         | All Architectures except arm32|
+--------------------------+-------------------------+---------------+----------------------------+-------------------------------+


\" \* \" 表示默认 RMW 实现。

中间件实现支持取决于平台支持层级。
例如，在 Tier 2 平台上的 Tier 1 中间件实现只能获得 Tier 2 级别的支持。

最低语言要求：

- C++17
- Python 3.6

依赖要求：

+------------------+-------------------+-----------------------------------------------------------------------------------------------------------+
|                  | Required Support  | Recommended Support                                                                                       |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Package          | Ubuntu   | Windows| RHEL 8 | Ubuntu Focal | macOS**  | Debian Bullseye  | OpenEmbedded**                                      |
|                  | Jammy    | 10**   |        |              |          |                  |                                                     |
+==================+==========+========+========+==============+==========+==================+=====================================================+
| CMake            | 3.22.1   | 3.22.0 | 3.20.2 | 3.16.3       | 3.14.4   | 3.18.4           | 3.22.3 / 3.16.5***                                  |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| EmPY             | 3.3.4    | 3.3.2                                                                                                              |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Gazebo Classic   | 11.x.x*  | N/A    | N/A    | 11.0.0*      | 11.x.x   | 11.x.x*          | N/A                                                 |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Gazebo (Ignition)| Fortress*| N/A    | N/A    | Fortress*    | Fortress*| Fortress*        | N/A                                                 |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| NumPy            | 1.21.5   | 1.18.4 | 1.14.3 | 1.17.4       | 1.18.4   | 1.19.5           | N/A                                                 |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Ogre             | 1.12.1*                                                                 | N/A                                                 |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| OpenCV           | 4.5.4    | 3.4.6* | 3.4.6  | 4.2.0        | 4.2.0    | 4.5.1            | 4.1.0 / 3.2.0***                                    |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| OpenSSL          | 1.1.1l   | 1.1.1l | 1.1.1k | 1.1.1d       | 1.1.1f   | 1.1.1i           | 1.1.1d / 1.1.1b***                                  |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Python           | 3.10.4   | 3.8.3  | 3.6.8  | 3.8.0        | 3.8.2    | 3.9.1            | 3.8.2 / 3.7.5***                                    |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Qt               | 5.15.3   | 5.12.12| 5.15.2 | 5.12.5       | 5.12.3   | 5.15.2           | 5.14.1 / 5.12.5***                                  |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
|                             | **Linux only**                                                                                                     |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| PCL              | 1.12.1   | N/A    | 1.11.1 | 1.10.0       | N/A      | 1.11.1           | 1.10.0                                              |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| **RMW DDS Middleware Providers**                                                                                                                 |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Cyclone DDS      | 0.9.x (Papillons)                                                                                                             |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Fast-DDS         | 2.6.x                                                                                                                         |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Connext DDS      | 6.0.1             | N/A    | 6.0.1                   | N/A                                                                    |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+
| Gurum DDS        | 2.7.x             | N/A    | 2.7.x        | N/A                                                                               |
+------------------+----------+--------+--------+--------------+----------+------------------+-----------------------------------------------------+

\" \* \" 表示这不是上游版本（可在官方操作系统仓库中获取），而是由 OSRF 或社区分发的软件包（在自定义仓库中构建和分发的软件包）。

\" \*\* \" 表示该依赖可能会有多次版本变更，因为它使用的包管理器会在没有稳定 API 的情况下持续更新该依赖。

\" \*\*\* \" webOS OSE 提供了这一不同的版本。

本文档仅记录 ROS 发行版首次发布时的版本，不会随着依赖的演进更新。
因此这些版本是一个最低水位线。

依赖所使用的包管理器：

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

`安装 Humble Hawksbill <../../humble/Installation.html>`__

补丁版本 1 (2022-11-23) 中的变更
--------------------------------

ros2topic
^^^^^^^^^

``now`` 作为 ``builtin_interfaces.msg.Time`` 的关键字，``auto`` 作为 ``std_msgs.msg.Header`` 的关键字
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
``ros2 topic pub`` 现在允许通过 ``now`` 关键字将 ``builtin_interfaces.msg.Time`` 消息设置为当前时间。
类似地，当传入关键字 ``auto`` 时，将自动生成 ``std_msg.msg.Header`` 消息。
此行为与 ROS 1 的 ``rostopic`` 一致 (http://wiki.ros.org/ROS/YAMLCommandLine#Headers.2Ftimestamps)

相关 PR：`ros2/ros2cli#751 <https://github.com/ros2/ros2cli/pull/751>`_

此 ROS 2 发行版中的新特性
-------------------------

ament_cmake_gen_version_h
^^^^^^^^^^^^^^^^^^^^^^^^^

生成带版本信息的 C/C++ 头文件
"""""""""""""""""""""""""""""
``ament_cmake_gen_version_h`` 中新增了一个 CMake 函数，用于生成包含软件包版本信息的头文件，见 `ament/ament_cmake#377 <https://github.com/ament/ament_cmake/pull/377>`__。
以下是最简单的用例：

.. code-block:: CMake

    project(my_project)
    add_library(my_lib ...)
    ament_generate_version_header(my_lib)

它将根据 ``package.xml`` 生成包含版本信息的头文件，并使其对链接 ``my_lib`` 库的目标可用。

如何包含该头文件：

.. code-block:: C

    #include <my_project/version.h>

头文件安装位置：

.. code-block:: cmake

    set(VERSION_HEADER ${CMAKE_INSTALL_PREFIX}/include/my_project/my_project/version.h)

launch
^^^^^^

在 group action 中限定环境变量的作用域
""""""""""""""""""""""""""""""""""""""

与 launch 配置类似，现在默认情况下，环境变量的状态被限定在 group action 的作用域内。

例如，在以下 launch 文件中，被执行的进程将回显值 ``1`` （在 Humble 之前它会回显 ``2``）：

.. tabs::

   .. group-tab:: XML

    .. code-block:: xml

      <launch>
        <set_env name="FOO" value="1" />
        <group>
          <set_env name="FOO" value="2" />
        </group>
        <executable cmd="echo $FOO" output="screen" shell="true" />
      </launch>

   .. group-tab:: Python

      .. code-block:: python

        import launch
        import launch.actions

        def generate_launch_description():
            return launch.LaunchDescription([
                launch.actions.SetEnvironmentVariable(name='FOO', value='1'),
                launch.actions.GroupAction([
                    launch.actions.SetEnvironmentVariable(name='FOO', value='2'),
                ]),
                launch.actions.ExecuteProcess(cmd=['echo', '$FOO'], output='screen', shell=True),
            ])

如果你希望为 launch 配置和环境变量禁用作用域限定，可以将 ``scoped`` 参数（或属性）设置为 false。

相关 PR：`ros2/launch#601 <https://github.com/ros2/launch/pull/601>`_

launch_pytest
"""""""""""""

我们新增了一个软件包 ``launch_pytest``，它是 ``launch_testing`` 的替代方案。
``launch_pytest`` 是一个简单的 pytest 插件，提供用于管理 launch 服务生命周期的 pytest fixture。

请参阅 `软件包 README 以了解详情与示例 <https://github.com/ros2/launch/tree/humble/launch_pytest>`_。

相关 PR：`ros2/launch#528 <https://github.com/ros2/launch/pull/528>`_

允许用可调用对象匹配目标 action
"""""""""""""""""""""""""""""""

事件处理器原本需要传入目标 action 对象来进行匹配，现在也可以改为传入 callable 来完成匹配。

相关 PR：`ros2/launch#540 <https://github.com/ros2/launch/pull/540>`_

求值 Python 表达式时可访问 math 模块
""""""""""""""""""""""""""""""""""""

在 ``PythonExpression`` 替换（``eval``）内部，我们现在可以使用 Python 的 math 模块中的符号。
例如，

.. code-block:: xml

   <launch>
     <log message="$(eval 'ceil(pi)')" />
   </launch>

相关 PR：`ros2/launch#557 <https://github.com/ros2/launch/pull/557>`_

布尔替换
""""""""

新增的 ``NotSubstitution``、``AndSubstitution`` 和 ``OrSubstitution`` 替换提供了一种便捷的方式来执行逻辑运算，例如

.. code-block:: xml

   <launch>
     <let name="p" value="true" />
     <let name="q" value="false" />
     <group if="$(or $(var p) $(var q))">
       <log message="The first condition is true" />
     </group>
     <group unless="$(and $(var p) $(var q))">
       <log message="The second condition is false" />
     </group>
     <group if="$(not $(var q))">
       <log message="The third condition is true" />
     </group>
   </launch>

相关 PR：`ros2/launch#598 <https://github.com/ros2/launch/pull/598>`_

新增的 action
"""""""""""""

* ``AppendEnvironmentVariable`` 向已有的环境变量追加值。

  * 相关 PR：`ros2/launch#543 <https://github.com/ros2/launch/pull/543>`_

* ``ResetLaunchConfigurations`` 重置应用于 launch 配置的所有配置项。

  * 相关 PR：`ros2/launch#515 <https://github.com/ros2/launch/pull/515>`_

launch_ros
^^^^^^^^^^

向 node action 传递 ROS 参数
""""""""""""""""""""""""""""

现在可以直接提供 `ROS 特有的节点参数 <../../How-To-Guides/Node-arguments>`_，而无需再通过带前导 ``--ros-args`` 标志的 ``args`` 参数来传递：

.. tabs::

   .. group-tab:: XML

    .. code-block:: xml

      <launch>
        <node pkg="demo_nodes_cpp" exec="talker" ros_args="--log-level debug" />
      </launch>

   .. group-tab:: YAML

      .. code-block:: yaml

        launch:
        - node:
            pkg: demo_nodes_cpp
            exec: talker
            ros_args: '--log-level debug'

Python launch 文件中 ``Node`` action 对应的参数是 ``ros_arguments``：

.. code-block:: python

  from launch import LaunchDescription
  import launch_ros.actions

  def generate_launch_description():
      return LaunchDescription([
          launch_ros.actions.Node(
              package='demo_nodes_cpp',
              executable='talker',
              ros_arguments=['--log-level', 'debug'],
          ),
      ])

相关 PR：`ros2/launch_ros#249 <https://github.com/ros2/launch_ros/pull/249>`_ 和 `ros2/launch_ros#253 <https://github.com/ros2/launch_ros/pull/253>`_。

frontend 对可组合节点的支持
"""""""""""""""""""""""""""

现在我们可以从 frontend launch 文件启动 node container 并向其中加载组件，例如：

.. tabs::

   .. group-tab:: XML

    .. code-block:: xml

       <launch>
         <node_container pkg="rclcpp_components" exec="component_container" name="my_container" namespace="">
           <composable_node pkg="composition" plugin="composition::Talker" name="talker" />
         </node_container>
         <load_composable_node target="my_container">
           <composable_node pkg="composition" plugin="composition::Listener" name="listener" />
         </load_composable_node>
       </launch>

   .. group-tab:: YAML

      .. code-block:: yaml

         launch:
           - node_container:
               pkg: rclcpp_components
               exec: component_container
               name: my_container
               namespace: ''
               composable_node:
                 - pkg: composition
                   plugin: composition::Talker
                   name: talker
           - load_composable_node:
               target: my_container
               composable_node:
                 - pkg: composition
                   plugin: composition::Listener
                   name: listener

相关 PR：`ros2/launch_ros#235 <https://github.com/ros2/launch_ros/pull/235>`_

参数替换
""""""""

新增的 ``ParameterSubstitution`` 允许你替换此前在 launch 中通过 ``SetParameter`` action 设置的参数值。
例如，

.. code-block:: xml

   <launch>
     <set_parameter name="foo" value="bar" />
     <log message="Parameter foo has value $(param foo)" />
   </launch>

相关 PR：`ros2/launch_ros#297 <https://github.com/ros2/launch_ros/pull/297>`_

新增的 action
"""""""""""""

* ``RosTimer`` 的作用类似于 launch 的 ``TimerAction``，但使用 ROS 时钟（因此例如可以使用仿真时间）。

  * 相关 PR：`ros2/launch_ros#244 <https://github.com/ros2/launch_ros/pull/244>`_ 和 `ros2/launch_ros#264 <https://github.com/ros2/launch_ros/pull/264>`_

* ``SetParametersFromFile`` 将 ROS 参数文件传递给 launch 文件中的所有节点（包括节点组件）。

  * 相关 PR：`ros2/launch_ros#260 <https://github.com/ros2/launch_ros/pull/260>`_ 和 `ros2/launch_ros#281 <https://github.com/ros2/launch_ros/pull/281>`_

SROS2 安全 enclave 支持证书吊销列表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

证书吊销列表（CRL）是一种机制，允许在证书到期之前将其吊销。
从 Humble 开始，现在可以将 CRL 放入 SROS2 安全 enclave 并使其生效。
有关使用示例，请参阅 `SROS2 教程 <https://github.com/ros2/sros2/blob/humble/SROS2_Linux.md#certificate-revocation-lists>`__。

内容过滤话题
^^^^^^^^^^^^

内容过滤话题支持一种更精细的订阅方式，表示订阅者并不一定希望看到该话题下发布的每个实例的所有取值。
当底层 RMW 实现支持该特性时，可以使用内容过滤话题来请求基于内容的订阅。

.. list-table:: RMW Content Filtered Topics support
   :widths: 25 25

   * - rmw_fastrtps
     - supported
   * - rmw_connextdds
     - supported
   * - rmw_cyclonedds
     - not supported

要了解更多信息，请参阅 `content_filtering <https://github.com/ros2/examples/blob/humble/rclcpp/topics/minimal_subscriber/content_filtering.cpp>`_ 示例。

相关设计 PR：`ros2/design#282 <https://github.com/ros2/design/pull/282>`_。

ros2cli
^^^^^^^

``ros2 launch`` 具有 ``--launch-prefix`` 参数
"""""""""""""""""""""""""""""""""""""""""""""

这样可以为 launch 文件中的所有可执行文件传入一个前缀，这在许多调试场景中很有用。
有关更多信息，请参阅相关的 `pull request <https://github.com/ros2/launch_ros/pull/254>`__，以及 :ref:`教程 <launch-prefix-example>`。

与此相关，还新增了 ``--launch-prefix-filter`` 命令行选项，用于有选择地将 ``--launch-prefix`` 中的前缀添加到可执行文件上。
有关更多信息，请参阅该 `pull request <https://github.com/ros2/launch_ros/pull/261>`__。

``ros2 topic echo`` 具有 ``--flow-style`` 参数
""""""""""""""""""""""""""""""""""""""""""""""

这允许用户强制对话题数据的 YAML 表示使用 ``flow style``。
如果不使用该选项，``ros2 topic echo /tf_static`` 的输出可能类似如下：

.. code-block::

  transforms:
  - header:
      stamp:
        sec: 1651172841
        nanosec: 433705575
      frame_id: single_rrbot_link3
    child_frame_id: single_rrbot_camera_link
    transform:
      translation:
        x: 0.05
        y: 0.0
        z: 0.9
      rotation:
        x: 0.0
        y: 0.0
        z: 0.0
        w: 1.0

使用该选项后，输出将类似如下：

.. code-block::

  transforms: [{header: {stamp: {sec: 1651172841, nanosec: 433705575}, frame_id: single_rrbot_link3}, child_frame_id: single_rrbot_camera_link, transform: {translation: {x: 0.05, y: 0.0, z: 0.9}, rotation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}]

有关更多信息，请参阅 `PyYAML 文档 <https://pyyaml.docsforge.com/master/documentation/#dictionaries-without-nested-collections-are-not-dumped-correctly>`__。

``ros2 topic echo`` 可以根据消息内容过滤数据
""""""""""""""""""""""""""""""""""""""""""""

这允许用户只打印话题中匹配某个 Python 表达式的数据。
例如，使用以下参数将只打印以 'foo' 开头的字符串消息：

.. code-block::

   ros2 topic echo --filter 'm.data.startswith("foo")` /chatter

有关更多信息，请参阅该 `pull request <https://github.com/ros2/ros2cli/pull/654>`__。


rviz2
^^^^^

为任意三角形列表应用纹理
""""""""""""""""""""""""

我们新增了 `使用 UV 坐标向任意三角形列表应用通过 URI 定义的纹理的能力 <https://github.com/ros2/rviz/pull/719>`__。
现在我们可以从纹理贴图生成渐变效果，而不是使用默认的灰度。
这将实现 marker 的复杂着色。
要使用它，你应该使用 ``visualization_msgs/Marker.msg`` 并填充 ``texture_resource``、``texture``、``uv_coordinates`` 和 ``mesh_file`` 字段。
你可以 `在此处 <https://github.com/ros2/common_interfaces/pull/153>`__ 找到更多信息。

.. image:: images/triangle_marker_with_gradient.png

可视化质量属性（包括惯性）
""""""""""""""""""""""""""

我们还新增了可视化惯性的能力。为此，你需要在机器人模型下的 'Mass Properties' 中启用 'Inertia'：

.. image:: images/rviz_mass_inertia.png

你可以在下面看到惯性的图像。

.. image:: images/tb4_inertia.png

在 RViz 中可视化 YUV 图像
"""""""""""""""""""""""""

现在可以直接在 RViz 中可视化 YUV 图像，而无需先转换为 RGB。
详见 `ros2/rviz#701 <https://github.com/ros2/rviz/pull/701>`__。

允许渲染超过 100 米的物体
"""""""""""""""""""""""""

默认情况下，RViz 只渲染距相机 100 米以内的物体。
rviz 相机插件中新增了一个名为 "Far Plane Distance" 的配置属性，可用于配置该渲染距离。

.. image:: images/rviz2-far-plane-distance.png

有关更多信息，请参阅 `ros2/rviz#849 <https://github.com/ros2/rviz/pull/849>`__。

自 Galactic 发行版以来的变更
----------------------------

C++ 头文件安装到子目录中
^^^^^^^^^^^^^^^^^^^^^^^^

在 Humble 之前的 ROS 2 发行版中，所有软件包的 C++ 头文件都安装到同一个 include 目录中。
例如，在 Galactic 中，目录结构如下所示（为简洁起见有所简略）：

.. code::

    /opt/ros/galactic/include/
    ├── rcl
    │   ├── node.h
    ├── rclcpp
    │   ├── node.hpp


在使用 overlay 时，这种结构可能会导致严重问题。
也就是说，由于 include 目录的顺序问题，很可能会获取到错误的头文件集。
有关这些问题的详细说明，请参阅 https://colcon.readthedocs.io/en/released/user/overriding-packages.html。

为帮助解决这一问题，在 Humble（以及今后所有 ROS 2 发行版）中，目录结构已发生变化：

.. code::

    /opt/ros/humble/include
    ├── rcl
    │   └── rcl
    │       ├── node.h
    ├── rclcpp
    │   └── rclcpp
    │       ├── node.hpp

请注意，使用这些头文件的下游软件包 *无需* 变更；使用 ``#include <rclcpp/node.hpp>`` 仍与以前一样有效。
但是，在使用会查找 include 目录的 IDE 时，可能需要将各个 include 目录添加到搜索路径中。

有关更多信息（包括该变更背后的原因），请参阅 https://github.com/ros2/ros2/issues/1150。

common_interfaces
^^^^^^^^^^^^^^^^^

为 Marker 消息支持纹理和内嵌网格
""""""""""""""""""""""""""""""""

这两项新增功能既增强了用标准消息以新方式可视化数据的能力，同时也使得能够在 rosbag 中跟踪这些数据。

**纹理** 为 marker 新增了三个字段：

.. code-block:: bash

   # Texture resource is a special URI that can either reference a texture file in
   # a format acceptable to (resource retriever)[https://index.ros.org/p/resource_retriever/]
   # or an embedded texture via a string matching the format:
   #   "embedded://texture_name"
   string texture_resource
   # An image to be loaded into the rendering engine as the texture for this marker.
   # This will be used iff texture_resource is set to embedded.
   sensor_msgs/CompressedImage texture
   # Location of each vertex within the texture; in the range: [0.0-1.0]
   UVCoordinate[] uv_coordinates

RViz 将完全支持通过内嵌格式进行纹理渲染。

对熟悉 ``mesh_resource`` 的人来说，``resource_retriever`` 应该并不陌生。
这将允许程序员选择数据加载的位置，既可以是本地文件，也可以是网络文件。
为了能够将所有数据记录到 rosbag 中，还提供了内嵌纹理图像的能力。

**网格** 也以类似方式进行了修改，新增了内嵌原始 Mesh 文件的能力以便记录。Meshfile 消息有两个字段：

.. code-block:: bash

   # The filename is used for both debug purposes and to provide a file extension
   # for whatever parser is used.
   string filename

   # This stores the raw text of the mesh file.
   uint8[] data

内嵌的 ``Meshfile`` 消息目前在实现中尚不支持。

相关 PR：`ros2/common_interfaces#153 <https://github.com/ros2/common_interfaces/pull/153>`_ `ros2/rviz#719 <https://github.com/ros2/rviz/pull/719>`_

为 SolidPrimitive 新增 ``PRISM`` 类型
"""""""""""""""""""""""""""""""""""""

``SolidPrimitive`` 消息新增了 ``PRISM`` 类型，以及相应的元数据。
有关更多信息，请参阅 `ros2/common_interfaces#167 <https://github.com/ros2/common_interfaces/pull/167>`_。

rmw
^^^

``struct`` 类型名后缀从 ``_t`` 变更为 ``_s``
""""""""""""""""""""""""""""""""""""""""""""

为避免在生成代码文档时 ``struct`` 类型名与其 ``typedef`` 别名之间出现类型名重复错误，所有 ``struct`` 类型名的后缀都已从 ``_t`` 变更为 ``_s``。
带 ``_t`` 后缀的别名仍然保留。
因此，该变更仅对使用完整 ``struct`` 类型说明符（即 ``struct type_name_t``）的代码而言是破坏性变更。

有关更多细节，请参阅 `ros2/rmw#313 <https://github.com/ros2/rmw/pull/313>`__。

rmw_connextdds
^^^^^^^^^^^^^^

默认使用 Connext 6
""""""""""""""""""

默认情况下，Humble Hawksbill 使用 Connext 6.0.1 作为 ``rmw_connextdds`` 的 DDS 实现。
仍然可以将 Connext 5.3.1 与 ``rmw_connextdds`` 一起使用，但必须从源码重新构建。

rcl
^^^

``struct`` 类型名后缀从 ``_t`` 变更为 ``_s``
""""""""""""""""""""""""""""""""""""""""""""

为避免在生成代码文档时 ``struct`` 类型名与其 ``typedef`` 别名之间出现类型名重复错误，所有 ``struct`` 类型名的后缀都已从 ``_t`` 变更为 ``_s``。
带 ``_t`` 后缀的别名仍然保留。
因此，该变更仅对使用完整 ``struct`` 类型说明符（即 ``struct type_name_t``）的代码而言是破坏性变更。

有关更多细节，请参阅 `ros2/rcl#932 <https://github.com/ros2/rcl/pull/932>`__。

新增 ROS_DISABLE_LOANED_MESSAGES 环境变量
"""""""""""""""""""""""""""""""""""""""""

该环境变量可用于禁用 loaned messages 支持，无论该 rmw 是否支持它们。
有关更多细节，请参阅指南 :doc:`配置零拷贝 loaned messages <../How-To-Guides/Configure-ZeroCopy-loaned-messages>`。

rclcpp
^^^^^^

为发布者和订阅支持类型适配
""""""""""""""""""""""""""

在定义了类型适配器之后，发布者和订阅者可以直接使用自定义数据结构，这有助于避免程序员额外的开发工作以及潜在的错误来源。
这在处理复杂数据类型时特别有用，例如将 OpenCV 的 ``cv::Mat`` 转换为 ROS 的 ``sensor_msgs/msg/Image`` 类型。

以下是一个将 ``std_msgs::msg::String`` 转换为 ``std::string`` 的类型适配器示例：

.. code-block:: cpp

   template<>
   struct rclcpp::TypeAdapter<
      std::string,
      std_msgs::msg::String
   >
   {
     using is_specialized = std::true_type;
     using custom_type = std::string;
     using ros_message_type = std_msgs::msg::String;

     static
     void
     convert_to_ros_message(
       const custom_type & source,
       ros_message_type & destination)
     {
       destination.data = source;
     }

     static
     void
     convert_to_custom(
       const ros_message_type & source,
       custom_type & destination)
     {
       destination = source.data;
     }
   };

以下是使用该类型适配器的示例：

.. code-block:: cpp

   using MyAdaptedType = TypeAdapter<std::string, std_msgs::msg::String>;

   // Publish a std::string
   auto pub = node->create_publisher<MyAdaptedType>(...);
   std::string custom_msg = "My std::string"
   pub->publish(custom_msg);

   // Pass a std::string to a subscription's callback
   auto sub = node->create_subscription<MyAdaptedType>(
     "topic",
     10,
     [](const std::string & msg) {...});

要了解更多信息，请参阅 `publisher <https://github.com/ros2/examples/blob/b83b18598b198b4a5ba44f9266c1bb39a393fa17/rclcpp/topics/minimal_publisher/member_function_with_type_adapter.cpp>`_ 和 `subscription <https://github.com/ros2/examples/blob/b83b18598b198b4a5ba44f9266c1bb39a393fa17/rclcpp/topics/minimal_subscriber/member_function_with_type_adapter.cpp>`_ 示例，以及更复杂的 `demo <https://github.com/ros2/demos/pull/482>`_。
有关更多细节，请参阅 `REP 2007 <https://reps.openrobotics.org/rep-2007/>`_。

``Client::asnyc_send_request(request)`` 返回 ``std::future`` 而非 ``std::shared_future``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

该变更在 `rclcpp#1734 <https://github.com/ros2/rclcpp/pull/1734>`_ 中实现。
这会破坏 API，因为 ``std::future::get()`` 方法会从 future 中取出值。
这意味着，如果该方法被第二次调用，就会抛出异常。
而 ``std::shared_future`` 不会出现这种情况，因为其 ``get()`` 方法返回 ``const &``。
示例：

.. code-block:: cpp

    auto future = client->async_send_request(req);
    ...
    do_something_with_response(future.get());
    ...
    do_something_else_with_response(future.get());  // this will throw an exception now!!

应修改为：

.. code-block:: cpp

    auto future = client->async_send_request(req);
    ...
    auto response = future.get();
    do_something_with_response(response);
    ...
    do_something_else_with_response(response);

如果需要 shared future，可以使用 ``std::future::share()`` 方法。

为 ``Publisher`` 新增 ``wait_for_all_acked`` 方法
"""""""""""""""""""""""""""""""""""""""""""""""""

该新方法会阻塞，直到发布者队列中的所有消息都被匹配的订阅确认（acked），或者指定的超时时间到期。
它只对可靠（reliable）发布者有用，因为在 best effort QoS 的情况下不存在确认机制。
示例：

.. code-block:: cpp

    auto pub = node->create_publisher<std_msgs::msg::String>(...);
    ...
    pub->publish(my_msg);
    ...
    pub->wait_for_all_acked(); // or pub->wait_for_all_acked(timeout)

如需更完整的示例，请参阅 `此处 <https://github.com/ros2/examples/blob/humble/rclcpp/topics/minimal_publisher/member_function_with_wait_for_all_acked.cpp>`__。

从 ``NodeBase`` 和 ``Node`` 类中移除 ``get_callback_groups`` 方法
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

``for_each_callback_group()`` 方法通过提供一种线程安全的方式来访问 ``callback_groups_`` 向量，取代了 ``get_callback_groups()``。
``for_each_callback_group()`` 接受一个函数作为参数，遍历存储的 callback group，并对其中有效的那些调用传入的函数。

有关更多细节，请参阅这个 `pull request <https://github.com/ros2/rclcpp/pull/1723>`_。

``Waitable`` 类的 ``add_to_wait_set`` 方法返回类型从 ``bool`` 变更为 ``void``
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
以前，从 ``Waitable`` 派生并重写 ``add_to_wait_set`` 的类在向 wait set 添加元素失败时会返回 false，因此调用方必须检查这个返回值并抛出或处理错误。
现在这种错误处理应该直接在 ``add_to_wait_set`` 方法中完成，必要时抛出异常。
如果没有错误发生，则不需要返回任何内容。
因此，这对 ``Waitable`` 的下游使用而言是破坏性变更。

有关更多细节，请参阅 `ros2/rclcpp#1612 <https://github.com/ros2/rclcpp/pull/1612>`__。

``NodeBaseInterface`` 类的 ``get_notify_guard_condition`` 方法返回类型发生变更
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
现在 ``rclcpp`` 使用围绕 ``rcl_guard_condition_t`` 的 ``GuardCondition`` 类封装，因此 ``get_notify_guard_condition`` 返回对节点的 ``rclcpp::GuardCondition`` 的引用。
因此，这对 ``NodeBaseInterface`` 和 ``NodeBase`` 的下游使用而言是破坏性变更。

有关更多细节，请参阅 `ros2/rclcpp#1612 <https://github.com/ros2/rclcpp/pull/1612>`__。

为 ``Clock`` 新增 ``sleep_until`` 和 ``sleep_for`` 方法
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
在 `ros2/rclcpp#1814 <https://github.com/ros2/rclcpp/pull/1814>`__ 和 `ros2/rclcpp#1828 <https://github.com/ros2/rclcpp/pull/1828>`__ 中新增了两个方法，用于在特定时钟上睡眠。
``Clock::sleep_until`` 会将当前线程挂起，直到该时钟达到特定时间。
``Clock::sleep_for`` 会将当前线程挂起，直到该时钟从方法被调用时起推进了一定的时长。
如果 ``Context`` 被关闭，这两个方法都会提前唤醒。

rclcpp_lifecycle
^^^^^^^^^^^^^^^^

发布者的激活与停用转换将自动触发
""""""""""""""""""""""""""""""""

以前，用户需要重写 ``LifecylceNode::on_activate()`` 和 ``LifecylceNode::on_deactivate()``，并在 ``LifecyclePublisher`` 上调用同名方法，才能真正触发转换。
现在，``LifecylceNode`` 为这些方法提供了默认实现，已经会自动完成这一工作。
有关 ``lifecycle_talker`` 节点的实现，请参阅 `此处 <https://github.com/ros2/demos/tree/humble/lifecycle>`__。

rclpy
^^^^^

托管节点
""""""""

rclpy 中新增了对生命周期节点的支持。
完整示例可在 `此处 <https://github.com/ros2/demos/tree/humble/lifecycle_py>`__ 找到。

为 ``Publisher`` 新增 ``wait_for_all_acked`` 方法
"""""""""""""""""""""""""""""""""""""""""""""""""

与 rclcpp 中新增的特性类似。

为 ``Clock`` 新增 ``sleep_until`` 和 ``sleep_for`` 方法
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
在 `ros2/rclpy#858 <https://github.com/ros2/rclpy/pull/858>`__ 和 `ros2/rclpy#864 <https://github.com/ros2/rclpy/pull/864>`__ 中新增了两个方法，用于在特定时钟上睡眠。
``sleep_until`` 会将当前线程挂起，直到该时钟达到特定时间。
``sleep_for`` 会将当前线程挂起，直到该时钟从方法被调用时起推进了一定的时长。
如果 ``Context`` 被关闭，这两个方法都会提前唤醒。

ros1_bridge
^^^^^^^^^^^

由于在 Ubuntu Jammy 及更高版本上没有官方的 ROS 1 发行版，``ros1_bridge`` 现在可以与 Ubuntu 打包版本的 ROS 1 兼容。
有关在 Jammy 软件包中使用 ``ros1_bridge`` 的更多细节，请参阅 :doc:`操作指南 <../How-To-Guides/Using-ros1_bridge-Jammy-upstream>`。

ros2cli
^^^^^^^

``ros2`` 命令默认禁用输出缓冲
"""""""""""""""""""""""""""""

在此发行版之前，运行类似如下的命令

.. code-block::

  ros2 echo /chatter | grep "Hello"

在输出缓冲区满之前不会打印任何数据。
用户可以通过设置 ``PYTHONUNBUFFERED=1`` 来绕过这个问题，但这并不十分友好。

取而代之，所有 ``ros2`` 命令现在默认采用行缓冲，因此上述命令在打印出换行符时就会立即生效。
要禁用该行为并使用 Python 默认的缓冲规则，请使用选项 ``--use-python-default-buffering``。
有关更多信息，请参阅 `原始 issue <https://github.com/ros2/ros2cli/issues/595>`__ 和 `pull request <https://github.com/ros2/ros2cli/pull/659>`__。

使用 ``--times/--once/-1`` 时，``ros2 topic pub`` 会等待一个匹配的订阅
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

在使用 ``--times/--once/-1`` 标志时，``ros2 topic pub`` 会在开始发布之前等待发现一个匹配的订阅。
这避免了 ros2cli 节点在发现匹配订阅之前就开始发布、从而导致最初的部分消息丢失的问题。
在使用可靠（reliable）QoS 配置时，这一点尤其出乎意料。

可以使用 ``-w/--wait-matching-subscriptions`` 标志配置开始发布前需要等待的匹配订阅数量，例如：

.. code-block:: console

   $ ros2 topic pub -1 -w 3 /chatter std_msgs/msg/String "{data: 'foo'}"

以在开始发布前等待三个匹配的订阅。

``-w`` 也可以独立于 ``--times/--once/-1`` 使用，但只有在与它们结合使用时其默认值才为 1，否则 ``-w`` 的默认值为零。

有关更多细节，请参阅 https://github.com/ros2/ros2cli/pull/642。

``ros2 param dump`` 默认输出发生变更
""""""""""""""""""""""""""""""""""""

  * dump 命令的 ``--print`` 选项已被 `废弃 <https://github.com/ros2/ros2cli/pull/638>`_。

    默认情况下，它会输出到 stdout：

    .. code-block:: console

      $ ros2 param dump /my_node_name

  * dump 命令的 ``--output-dir`` 选项已被 `废弃 <https://github.com/ros2/ros2cli/pull/638>`_。

    要将参数转储到文件，请运行：

    .. code-block:: console

      $ ros2 param dump /my_node_name > my_node_name.yaml

``ros2 param set`` 现在接受更多 YAML 语法
"""""""""""""""""""""""""""""""""""""""""

以前，尝试向字符串类型的参数设置像 "off" 这样的字符串是无法生效的。
这是因为 ``ros2 param set`` 会将命令行参数解释为 YAML，而 YAML 认为 "off" 是布尔类型。
自 https://github.com/ros2/ros2cli/pull/684 起，``ros2 param set`` 现在接受 YAML 转义序列 "!!str off"，以确保该值被当作字符串处理。

``ros2 pkg create`` 可自动生成 LICENSE 文件
"""""""""""""""""""""""""""""""""""""""""""

如果将 ``--license`` 标志传给 ``ros2 pkg create``，且该许可证属于已知许可证之一，``ros2 pkg create`` 现在会自动在包的根目录下生成 LICENSE 文件。
要查看已知许可证列表，请运行 ``ros2 pkg create --license ? <package_name>``。
有关更多信息，请参阅相关的 `pull request <https://github.com/ros2/ros2cli/pull/650>`__。

robot_state_publisher
^^^^^^^^^^^^^^^^^^^^^

新增 ``frame_prefix`` 参数
""""""""""""""""""""""""""
在 `ros/robot_state_publisher#159 <https://github.com/ros/robot_state_publisher/pull/159>`__ 中新增了参数 ``frame_prefix``。
该参数是一个字符串，会被添加到 ``robot_state_publisher`` 发布的所有坐标系名称之前。
与 ROS 1 中原始 ``tf`` 库里的 ``tf_prefix`` 类似，该参数可用于以不同的坐标系名称多次发布同一个机器人描述。

移除已废弃的 ``use_tf_static`` 参数
"""""""""""""""""""""""""""""""""""

已从 ``robot_state_publisher`` 中移除废弃的 ``use_tf_static`` 参数。
这意味着静态变换会无条件地发布到 ``/tf_static`` 话题，并且静态变换会以 ``transient_local`` 服务质量发布。
这本来就是默认行为，也正是 ``tf2_ros::TransformListener`` 类之前所期望的行为，因此大多数代码无需修改。
任何依赖 ``robot_state_publisher`` 周期性将静态变换发布到 ``/tf`` 的代码，都必须改为以 ``transient_local`` 订阅的方式订阅 ``/tf_static``。


rosidl_cmake
^^^^^^^^^^^^

废弃 ``rosidl_target_interfaces()``
"""""""""""""""""""""""""""""""""""

CMake 函数 ``rosidl_target_interfaces()`` 已被废弃，现在调用时会发出 CMake 警告。
如果希望在使用生成消息/服务/动作的同一个 ROS 包中使用它们，应改为调用 ``rosidl_get_typesupport_target()``，然后调用 ``target_link_libraries()``，使目标依赖于返回的 typesupport 目标。
有关更多细节，请参阅 https://github.com/ros2/rosidl/pull/606，使用新函数的示例请参阅 https://github.com/ros2/demos/pull/529。


rviz2
^^^^^

* `提高了 3 字节像素格式的效率 <https://github.com/ros2/rviz/pull/743>`__
* `将惯量（inertia）的计算方式改为使用 ignition math，而不再使用 Ogre 的数学库 <https://github.com/ros2/rviz/pull/751>`__。


geometry2
^^^^^^^^^

废弃 TF2Error::NO_ERROR 等
""""""""""""""""""""""""""

``tf2`` 库使用名为 ``TF2Error`` 的枚举来返回错误。
遗憾的是，其中的一个枚举值名为 ``NO_ERROR``，它会与 Windows 上的宏冲突。
为解决该问题，``TF2Error`` 中新增了一组枚举值，每个都带有 ``TF2`` 前缀。
原有的枚举值仍然可用，但已被废弃，使用时会产生废弃警告。
所有使用 ``TF2Error`` 枚举值的代码都应更新为使用新的带 ``TF2`` 前缀的错误。
有关更多细节，请参阅 https://github.com/ros2/geometry2/pull/349。

static_transform_publisher 更直观的命令行参数
"""""""""""""""""""""""""""""""""""""""""""""

``static_transform_publisher`` 程序过去接收这样的参数：``ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 1 foo bar``。
前三个数字是平移量 x、y、z，接下来四个是四元数 x、y、z、w，最后两个参数是父坐标系和子坐标系 ID。
虽然这样可以工作，但存在两个问题：

* 用户必须指定 *所有* 参数，即使只是设置一个数值
* 阅读命令行很难判断它正在发布什么

为同时解决这两个问题，命令行处理方式已改为使用标志，并且除 ``--frame-id`` 和 ``--child-frame-id`` 之外的所有标志都是可选的。
因此，上面的命令可以简化为：``ros2 run tf2_ros static_transform_publisher --frame-id foo --child-frame-id bar``
如果只想修改平移量 x，命令可以是：``ros2 run tf2_ros static_transform_publisher --x 1.5 --frame-id foo --child-frame-id bar``。

在本发行版中仍然允许使用旧式参数，但它们已被废弃，并会打印警告。
它们将在未来的发行版中被移除。
有关更多细节，请参阅 https://github.com/ros2/geometry2/pull/392。

变换监听器的 spin 线程不再执行节点回调
""""""""""""""""""""""""""""""""""""""

``tf2_ros::TransformListener`` 不再对传入的节点对象执行 spin。
取而代之，它会创建一个回调组，以便对其内部创建的实体执行回调。
这意味着，如果你在创建变换监听器时设置了参数 ``spin_thread=true``，就
不能再依赖自己的回调被执行。
你必须在节点上调用 ``spin`` 函数（例如 ``rclcpp::spin``），或者把节点添加到自己的执行器中。

相关 pull request：`geometry2#442 <https://github.com/ros2/geometry2/pull/442>`_

rosbag2
^^^^^^^

新的回放与录制控制
""""""""""""""""""

新增了多个 pull request，以增强用户对包回放的控制能力。
Pull request `931 <https://github.com/ros2/rosbag2/pull/931>`_ 增加了指定开始回放时间戳的能力。
得益于 pull request `789 <https://github.com/ros2/rosbag2/pull/789>`_，现在可以按指定时长延迟回放的开始。

与此相关，``rosbag2`` 还为用户提供了在回放过程中控制回放的新方式。
Pull request `847 <https://github.com/ros2/rosbag2/pull/847>`_ 增加了在终端回放期间暂停、恢复和播放下一消息的键盘控制。
得益于 pull request `905 <https://github.com/ros2/rosbag2/pull/905>`_ 和 `904 <https://github.com/ros2/rosbag2/pull/904>`_，还可以以暂停状态开始回放，这便于用户先启动回放再逐条查看消息，例如在调试数据流水线时。
Pull request `836 <https://github.com/ros2/rosbag2/pull/836>`_ 增加了在包内跳转的接口，允许用户在回放期间在包内任意移动。

最后，pull request `851 <https://github.com/ros2/rosbag2/pull/851>`_ 为录制新增了快照模式。
该模式适用于事件记录场景，它允许录制先开始填充缓冲区，但在服务被调用之前不会开始将数据写入磁盘。

突发模式回放
""""""""""""

虽然从包中实时回放数据是包文件最常见的用途，但在某些情况下你可能希望尽快获取包中的数据。
通过 pull request `977 <https://github.com/ros2/rosbag2/pull/977>`_，``rosbag2`` 获得了从包中“突发”（burst）输出数据的能力。
在突发模式下，数据会以尽可能快的速度回放。
这在机器学习等应用中很有用。

零拷贝回放
""""""""""

默认情况下，如果可以使用租借消息（loaned message），回放的消息会以租借消息的形式发布。
这有助于减少数据拷贝次数，因此对发送大数据尤其有益。
Pull request `981 <https://github.com/ros2/rosbag2/pull/981>`_ 为回放新增了 ``--disable-loan-message`` 选项。

等待确认
""""""""

该新选项会一直等待，直到所有已发布的消息都被所有订阅者确认，或者在回放终止前以毫秒为单位的超时时间到期。
尤其适用于在短时间内发送大尺寸消息的场景。
该选项仅在发布者的 QOS 配置为 RELIABLE 时有效。
Pull request `951 <https://github.com/ros2/rosbag2/pull/951>`_ 为回放新增了 ``--wait-for-all-acked`` 选项。

包编辑
""""""

``rosbag2`` 正在逐步支持包的编辑操作，例如删除某个话题的所有消息，或者将多个包合并为一个包。
Pull request `921 <https://github.com/ros2/rosbag2/pull/921>`_ 增加了包重写功能以及 ``ros2 bag convert`` 子命令。

其他变更
""""""""

Pull request `925 <https://github.com/ros2/rosbag2/pull/925>`_ 使 ``rosbag2`` 在录制时忽略“叶子话题”（没有发布者的话题）。
这些话题将不再被自动添加到包中。

已知问题
--------

* 在 `Ubuntu 22.04 Jammy 主机上安装 ROS 2 <../../humble/Installation/Ubuntu-Install-Debians.html>`__ 时，请务必在安装 ROS 2 软件包之前更新系统。
  特别要确保 ``systemd`` 和 ``udev`` 已更新到可用的最新版本，否则安装依赖 ``libudev1`` 的 ``ros-humble-desktop`` 时可能会导致系统关键软件包被移除。
  详细信息请参见 `ros2/ros2#1272 <https://github.com/ros2/ros2/issues/1272>`_ 和 `Launchpad #1974196 <https://bugs.launchpad.net/ubuntu/+source/systemd/+bug/1974196>`_

* 当 ROS 2 的 apt 仓库可用时，Ubuntu 中的 ROS 1 软件包将无法安装。有关更多信息，请参阅 :doc:`Ubuntu Jammy 上的 ros1_bridge <../How-To-Guides/Using-ros1_bridge-Jammy-upstream>` 文档。

* 一些主流 Linux 发行版开始修改 Python，使软件包安装到 ``/usr/local``，这会破坏 ``ament_package`` 的某些部分以及使用 ``colcon`` 的构建。
  特别是，在 Ubuntu Jammy 上使用通过 pip 安装的 ``setuptools`` 会出现这种异常行为，因此不推荐这样做。
  目前有一个 `提议的解决方案 <https://github.com/colcon/colcon-core/pull/512>`_，但在广泛发布之前还需要进一步测试。

* 按大小或时长拆分的 ROS 2 包无法正确回放。
  只会回放最后录制的那个包。
  建议避免按大小或时长拆分包。
  详细信息请参见 `ros2/rosbag2#966 <https://github.com/ros2/rosbag2/issues/966>`__。

发行时间线
----------

    2022 年 3 月 21 日（周一）- Alpha + RMW 冻结
        对 ROS Base [1]_ 软件包进行初步测试和稳定化，并冻结 RMW 提供方软件包的 API 和特性。

    2022 年 4 月 4 日（周一）- 冻结
        冻结 Rolling Ridley 中 ROS Base [1]_ 软件包的 API 和特性。
        此时间点之后只应发布缺陷修复版本。
        新软件包可以独立发布。

    2022 年 4 月 18 日（周一）- 分支
        从 Rolling Ridley 分支。
        ``rosdistro`` 重新开放接受 ROS Base [1]_ 软件包的 Rolling PR。
        Humble 的开发从 ``ros-rolling-*`` 软件包转向 ``ros-humble-*`` 软件包。

    2022 年 4 月 25 日（周一）- Beta
        提供更新后的 ROS Desktop [2]_ 软件包版本。
        征集广泛测试。

    2022 年 5 月 16 日（周一）- 发布候选
        构建发布候选（Release Candidate）软件包。
        提供更新后的 ROS Desktop [2]_ 软件包版本。

    2022 年 5 月 19 日（周四）- 发行版冻结
        冻结 rosdistro。
        不会合并 ``rosdistro`` 仓库上针对 Humble 的 PR（在发布公告后重新开放）。

    2022 年 5 月 23 日（周一）- 正式发布
        发布公告。
        ``rosdistro`` 重新开放接受 Humble PR。

.. [1] ``ros_base`` 变体的说明见 `REP 2001 (ros-base) <https://reps.openrobotics.org/rep-2001/#ros-base>`_。
.. [2] ``desktop`` 变体的说明见 `REP 2001 (desktop-variants) <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_。
