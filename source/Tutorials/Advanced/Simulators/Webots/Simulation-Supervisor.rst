Ros2Supervisor 节点
===================

**目标：** 使用一个默认的 Supervisor 机器人（名为 ``Ros2Supervisor``）扩展接口。

**教程级别：** 高级

**用时：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在本教程中，你将学习如何启用 ``Ros2Supervisor`` 节点，该节点通过创建额外的服务和话题来与仿真交互，从而增强接口。
例如，你可以在仿真运行时录制动画，或直接从 ROS 2 接口生成 Webots 节点。
这些说明详细列出了当前已实现的功能以及如何使用它们。

前置条件
--------

在继续本教程之前，请确保你已完成以下内容：

- 理解初学者 :doc:`../../../../Tutorials` 中涵盖的 ROS 2 节点和话题。
- 了解 Webots、ROS 2 及其接口包。
- 熟悉 :doc:`./Setting-Up-Simulation-Webots-Basic`。

``Ros2Supervisor``
------------------

``Ros2Supervisor`` 由两个主要部分组成：

* 一个添加到仿真世界中的 Webots Robot 节点。
  它的 ``supervisor`` 字段设置为 TRUE。
* 一个 ROS 2 节点，作为外部控制器连接到 Webots Robot（方式与你自己的机器人插件类似）。

该 ROS 2 节点充当控制器，调用 Supervisor API 函数来控制或与仿真世界交互。
用户与 ROS 2 节点的交互主要通过服务和话题进行。

这些节点可以在启动 Webots 时通过 ``WebotsLauncher`` 中的 ``ros2_supervisor`` 参数自动创建。

.. code-block:: python

    webots = WebotsLauncher(
        world=PathJoinSubstitution([package_dir, 'worlds', world]),
        mode=mode,
        ros2_supervisor=True
    )

``webots._supervisor`` 对象也必须包含在启动文件返回的 ``LaunchDescription`` 中。

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

有关 ``webots_ros2`` 项目启动文件的更多信息，请参见 :doc:`./Setting-Up-Simulation-Webots-Basic`。

Clock 话题
----------

``Ros2Supervisor`` 节点负责获取 Webots 仿真的时间，并将其发布到 ``/clock`` 话题。
这意味着如果其他节点的 ``use_sim_time`` 参数设置为 ``true``，则必须生成 ``Ros2Supervisor``。
有关 ``/clock`` 话题的更多信息，请参见 `ROS wiki <http://wiki.ros.org/Clock>`_。

导入 Webots 节点
----------------

``Ros2Supervisor`` 节点还允许你通过服务从字符串生成 Webots 节点。

该服务名为 ``/Ros2Supervisor/spawn_node_from_string``，类型为 ``webots_ros2_msgs/srv/SpawnNodeFromString``。
``SpawnNodeFromString`` 类型期望一个 ``data`` 字符串作为输入，并返回一个 ``success`` 布尔值。

根据给定的字符串，Supervisor 节点获取被导入节点的名称，并将其添加到内部列表中，以便之后可能删除（见 :ref:`Remove a Webots imported node`）。

该节点使用 `API 函数 <https://cyberbotics.com/doc/reference/supervisor?tab-language=python#wb_supervisor_field_import_mf_node_from_string>`_ ``importMFNodeFromString(nodeString)`` 导入。

下面是一个导入名为 ``imported_robot`` 的简单 Robot 的示例：

.. code-block:: console

    $ ros2 service call /Ros2Supervisor/spawn_node_from_string webots_ros2_msgs/srv/SpawnNodeFromString "data: Robot { name \"imported_robot\" }"

.. note::
    如果你尝试在节点字符串中导入一些 PROTO，它们各自的 URL 必须在 ``.wbt`` 世界文件中声明为 EXTERNPROTO 或 IMPORTABLE EXTERNPROTO。

.. _Remove a Webots imported node:

删除 Webots 导入节点
--------------------

一旦通过 ``/Ros2Supervisor/spawn_node_from_string`` 服务导入了一个节点，它也可以被删除。

这可以通过将节点名称发送到类型为 ``std_msgs/msg/String`` 的话题 ``/Ros2Supervisor/remove_node`` 来实现。

如果该节点确实在导入列表中，则使用 `API 方法 <https://cyberbotics.com/doc/reference/supervisor?tab-language=python#wb_supervisor_node_remove>`_ ``remove()`` 删除它。

下面是一个如何删除 ``imported_robot`` Robot 的示例：

.. code-block:: console

    $ ros2 topic pub --once /Ros2Supervisor/remove_node std_msgs/msg/String "{data: imported_robot}"

录制动画
--------

``Ros2Supervisor`` 节点还创建了两个额外的服务来录制 HTML5 动画。

``/Ros2Supervisor/animation_start_recording`` 服务的类型为 ``webots_ros2_msgs/srv/SetString``，用于开始动画。
``SetString`` 类型期望一个 ``value`` 字符串作为输入，并返回一个 ``success`` 布尔值。
输入 ``value`` 表示动画文件应保存到的目录的绝对路径。

下面是一个如何开始动画的示例：

.. code-block:: console

    $ ros2 service call /Ros2Supervisor/animation_start_recording webots_ros2_msgs/srv/SetString "{value: "<ABSOLUTE_PATH>/index.html"}"


``/Ros2Supervisor/animation_stop_recording`` 服务的类型为 ``webots_ros2_msgs/srv/GetBool``，用于停止动画。

.. code-block:: console

    $ ros2 service call /Ros2Supervisor/animation_stop_recording webots_ros2_msgs/srv/GetBool "{ask: True}"


总结
----

在本教程中，你学习了如何启用 ``Ros2Supervisor``，以及如何用 Webots 仿真扩展接口。
该节点创建了多个服务和话题，用于与仿真交互并修改仿真。
