设置重置处理器
==============

**目标：** 使用重置处理器扩展机器人仿真，以便在按下 Webots 的重置按钮时重启节点。

**教程级别：** 高级

**用时：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在本教程中，你将学习如何使用 Webots 在机器人仿真中实现重置处理器。
Webots 的重置按钮会将世界恢复到初始状态并重启控制器。
它很方便，因为它可以快速重置仿真，但在 ROS 2 的上下文中，机器人控制器不会再次启动，导致仿真停止。
重置处理器允许你在按下 Webots 中的重置按钮时重启特定节点或执行额外操作。
这对于需要重置仿真状态或重启特定组件而无需完全重启整个 ROS 系统的场景非常有用。

前置条件
--------

在继续本教程之前，请确保你已完成以下内容：

- 理解初学者 :doc:`../../../../Tutorials` 中涵盖的 ROS 2 节点和话题。
- 了解 Webots、ROS 2 及其接口包。
- 熟悉 :doc:`./Setting-Up-Simulation-Webots-Basic`。


简单场景的重置处理器（仅控制器）
--------------------------------

在你的包的启动文件中，添加 ``respawn`` 参数。

.. code-block:: python

  def generate_launch_description():
      robot_driver = WebotsController(
          robot_name='my_robot',
          parameters=[
              {'robot_description': robot_description_path}
          ],

          # Every time one resets the simulation the controller is automatically respawned
          respawn=True
      )

      # Starts Webots
      webots = WebotsLauncher(world=PathJoinSubstitution([package_dir, 'worlds', world]))

      return LaunchDescription([
          webots,
          robot_driver
      ])

重置时，Webots 会终止所有驱动节点。
因此，要在重置后再次启动它们，你应该将驱动节点的 ``respawn`` 属性设置为 ``True``。
它将确保驱动节点在重置后正常运行。

多节点的重置处理器（无需关闭）
------------------------------

如果你有一些必须与驱动节点一起启动的其他节点（例如 ``ros2_control`` 节点），那么你可以使用 ``OnProcessExit`` 事件处理器：

.. code-block:: python

  def get_ros2_control_spawners(*args):
      # Declare here all nodes that must be restarted at simulation reset
      ros_control_node = Node(
          package='controller_manager',
          executable='spawner',
          arguments=['diffdrive_controller']
      )
      return [
          ros_control_node
      ]

  def generate_launch_description():
      robot_driver = WebotsController(
          robot_name='my_robot',
          parameters=[
              {'robot_description': robot_description_path}
          ],

          # Every time one resets the simulation the controller is automatically respawned
          respawn=True
      )

      # Starts Webots
      webots = WebotsLauncher(world=PathJoinSubstitution([package_dir, 'worlds', world]))

      # Declare the reset handler that respawns nodes when robot_driver exits
      reset_handler = launch.actions.RegisterEventHandler(
          event_handler=launch.event_handlers.OnProcessExit(
              target_action=robot_driver,
              on_exit=get_ros2_control_spawners,
          )
      )

      return LaunchDescription([
          webots,
          robot_driver,
          reset_handler
      ] + get_ros2_control_spawners())

无法在 ``ros2_control`` 节点上使用 ``respawn`` 属性，因为 spawner 是在启动时退出，而不是在仿真重置时退出。
相反，我们应该在一个函数（例如 ``get_ros2_control_spawners``）中声明一个节点列表。
此列表中的节点在执行启动文件时与其他节点一起启动。
使用 ``reset_handler``，该函数还被声明为在 ``robot_driver`` 节点退出时要启动的操作，这对应着在 Webots 界面中重置仿真的时刻。
``robot_driver`` 节点仍将 ``respawn`` 属性设置为 ``True``，以便它与 ``ros2_control`` 节点一起被重启。

需要关闭节点的重置处理器
------------------------

在当前的 ROS 2 launch API 中，无法让重置在节点需要在重启前关闭的启动文件中工作（例如 ``Nav2`` 或 ``RViz``）。
原因是目前 ROS 2 不允许从启动文件关闭特定节点。
有一个解决方案，但它需要在按下重置按钮后手动重启节点。

Webots 需要在一个不带其他节点的特定启动文件中启动。

.. code-block:: python

  def generate_launch_description():
      # Starts Webots
      webots = WebotsLauncher(world=PathJoinSubstitution([package_dir, 'worlds', world]))

      return LaunchDescription([
          webots
      ])


第二个启动文件必须从另一个进程启动。
此启动文件包含所有其他节点，包括机器人控制器/插件、Navigation2 节点、RViz、状态发布者等。

.. code-block:: python

  def generate_launch_description():
      robot_driver = WebotsController(
          robot_name='my_robot',
          parameters=[
              {'robot_description': robot_description_path}
          ]
      )

      ros_control_node = Node(
          package='controller_manager',
          executable='spawner',
          arguments=['diffdrive_controller']
      )

      nav2_node = IncludeLaunchDescription(
          PythonLaunchDescriptionSource(os.path.join(
              get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')),
          launch_arguments=[
              ('map', nav2_map),
              ('params_file', nav2_params),
          ],
      )

      rviz = Node(
          package='rviz2',
          executable='rviz2',
          output='screen'
      )

      # Declare the handler that shuts all nodes down when robot_driver exits
      shutdown_handler = launch.actions.RegisterEventHandler(
          event_handler=launch.event_handlers.OnProcessExit(
              target_action=robot_driver,
              on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
          )
      )

      return LaunchDescription([
          robot_driver,
          ros_control_node,
          nav2_node,
          rviz,
          shutdown_handler
      ])

第二个启动文件包含一个处理器，当驱动节点退出时（即仿真被重置时的情况）触发关闭事件。
此第二个启动文件必须在按下重置按钮后从命令行手动重启。

总结
----

在本教程中，你学习了如何使用 Webots 在机器人仿真中实现重置处理器。
重置处理器允许你在按下 Webots 中的重置按钮时重启特定节点或执行额外操作。
你根据仿真的复杂性和节点的需求探索了不同的方法。
