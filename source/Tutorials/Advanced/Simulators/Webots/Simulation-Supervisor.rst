Ros2Supervisor 节点
===================

**目标：** 使用默认的 Supervisor 机器人（名为 ``Ros2Supervisor``）扩展该接口。

**教程级别：** 高级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在本教程中，你将学习如何启用 ``Ros2Supervisor`` 节点，它通过创建额外的服务和话题来与该仿真交互，从而增强接口能力。
例如，你可以在仿真运行期间直接从 ROS 2 接口录制动画或生成 Webots 节点。
以下说明详细列出了当前已实现的功能及其使用方法。

前提条件
--------

在继续本教程之前，请确保你已完成以下内容：

- 了解初学者 :doc:`../../../../Tutorials` 中涵盖的 ROS 2 节点和话题。
- 了解 Webots、ROS 2 及其接口软件包。
- 熟悉 :doc:`./Setting-Up-Simulation-Webots-Basic` 。

``Ros2Supervisor`` 节点
-----------------------

``Ros2Supervisor`` 由两个主要部分组成：

* 添加到仿真世界中的 Webots Robot 节点。
  其 ``supervisor`` 字段被设置为 TRUE。
* 一个 ROS 2 节点，它以外部控制器的方式连接到该 Webots Robot（与你自己的机器人插件类似）。

该 ROS 2 节点充当控制器，调用 Supervisor API 函数来控制或与仿真世界交互。
用户与该 ROS 2 节点的交互主要通过服务和话题进行。

这些节点可以在启动 Webots 时通过 ``WebotsLauncher`` 中的 ``ros2_supervisor`` 参数自动创建。

.. code-block:: python

    webots = WebotsLauncher(
        world=PathJoinSubstitution([package_dir, 'worlds', world]),
        mode=mode,
        ros2_supervisor=True
    )

还必须将 ``webots._supervisor`` 对象包含在 launch 文件返回的 ``LaunchDescription`` 中。

.. code-block:: python

    return LaunchDescription([
        webots,
        webots._supervisor,

        # This action will kill all nodes once the Webots simulation has exited
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[
                    launch.actions.EmitEvent(event=launch.events.Shutdown())
                ],
            )
        )
    ])

有关 ``webots_ros2`` 项目 launch 文件的更多信息，请参阅 :doc:`./Setting-Up-Simulation-Webots-Basic` 。

时钟话题
--------

``Ros2Supervisor`` 节点负责获取 Webots 仿真的时间并将其发布到 ``/clock`` 话题。
这意味着，如果其他一些节点的 ``use_sim_time`` 参数被设置为 ``true`` ，则必须生成 ``Ros2Supervisor``。
有关 ``/clock`` 话题的更多信息，请参阅 `ROS wiki <http://wiki.ros.org/Clock>`_。

导入 Webots 节点
----------------

``Ros2Supervisor`` 节点还允许你通过一个服务从字符串生成 Webots 节点。

该服务名为 ``/Ros2Supervisor/spawn_node_from_string``，类型为 ``webots_ros2_msgs/srv/SpawnNodeFromString``。
``SpawnNodeFromString`` 类型期望输入一个 ``data`` 字符串，并返回一个 ``success`` 布尔值。

根据给定的字符串，Supervisor 节点会获取所导入节点的名称，并将其添加到一个内部列表中，以便之后可能删除（请参见 :ref:`移除 Webots 中导入的节点 <Remove a Webots imported node>` ）。

该节点通过 ``importMFNodeFromString(nodeString)`` `API 函数 <https://cyberbotics.com/doc/reference/supervisor?tab-language=python#wb_supervisor_field_import_mf_node_from_string>`_ 导入。

下面是一个导入名为 ``imported_robot`` 的简单 Robot 的示例：

.. code-block:: console

    $ ros2 service call /Ros2Supervisor/spawn_node_from_string webots_ros2_msgs/srv/SpawnNodeFromString "data: Robot { name \"imported_robot\" }"

.. note::
    如果你尝试在节点字符串中导入某些 PROTO，它们各自的 URL 必须在 ``.wbt`` 世界文件中声明为 EXTERNPROTO 或 IMPORTABLE EXTERNPROTO。

.. _Remove a Webots imported node:

移除 Webots 中导入的节点
------------------------

一旦使用 ``/Ros2Supervisor/spawn_node_from_string`` 服务导入了某个节点，它也可以被移除。

这可以通过将节点名称发送到名为 ``/Ros2Supervisor/remove_node`` 的话题（类型为 ``std_msgs/msg/String``）来实现。

如果该节点确实在已导入列表中，则会使用 ``remove()`` `API 方法 <https://cyberbotics.com/doc/reference/supervisor?tab-language=python#wb_supervisor_node_remove>`_ 将其移除。

下面是一个移除 ``imported_robot`` Robot 的示例：

.. code-block:: console

    $ ros2 topic pub --once /Ros2Supervisor/remove_node std_msgs/msg/String "{data: imported_robot}"

录制动画
--------

``Ros2Supervisor`` 节点还会创建两个额外的服务，用于录制 HTML5 动画。

``/Ros2Supervisor/animation_start_recording`` 服务的类型为 ``webots_ros2_msgs/srv/SetString``，用于开始录制动画。
``SetString`` 类型期望输入一个 ``value`` 字符串，并返回一个 ``success`` 布尔值。
输入的 ``value`` 表示所保存动画文件目录的绝对路径。

下面是一个开始录制动画的示例：

.. code-block:: console

    $ ros2 service call /Ros2Supervisor/animation_start_recording webots_ros2_msgs/srv/SetString "{value: "<ABSOLUTE_PATH>/index.html"}"


``/Ros2Supervisor/animation_stop_recording`` 服务的类型为 ``webots_ros2_msgs/srv/GetBool``，用于停止录制动画。

.. code-block:: console

    $ ros2 service call /Ros2Supervisor/animation_stop_recording webots_ros2_msgs/srv/GetBool "{ask: True}"


概述
----

在本教程中，你学习了如何启用 ``Ros2Supervisor``，以及如何用 Webots 仿真扩展该接口。
该节点会创建多个服务和话题，用于与仿真交互并修改仿真。
