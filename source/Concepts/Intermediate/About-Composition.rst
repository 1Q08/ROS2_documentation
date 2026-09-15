.. redirect-from::

   Concepts/About-Composition

组合
====

.. contents:: 目录
   :local:

ROS 1 - 节点与节点管理器
------------------------

在 ROS 1 中，您可以将代码编写为 `ROS 节点 <https://wiki.ros.org/Nodes>`__，也可以写成 `ROS 节点管理器 <https://wiki.ros.org/nodelet>`__。
ROS 1 节点会被编译为可执行文件。
另一方面，ROS 1 节点管理器会被编译为共享库，然后由容器进程在运行时加载。

ROS 2 - 统一 API
----------------

在 ROS 2 中，推荐的编写方式类似于节点管理器——我们称之为 ``Component``。
这使得在现有代码中添加通用概念变得很容易，比如 `生命周期 <https://design.ros2.org/articles/node_lifecycle.html>`__。
不同 API 的问题是 ROS 1 的主要缺点之一，而在 ROS 2 中，由于两种方式都使用相同的 API，因此这一问题得以避免。

.. note::

   仍然可以使用“自己编写 main”的节点式风格，但在一般情况下并不推荐。

通过将进程布局设为部署时决策，用户可以在以下两种方式之间选择：

* 在单独进程中运行多个节点，带来进程/故障隔离的优点，并使单个节点更容易调试；
* 在单个进程中运行多个节点，带来更低的开销，并可选用更高效的通信方式（参见 :doc:`进程内通信 <../../Tutorials/Demos/Intra-Process-Communication>`）。

另外，``ros2 launch`` 可以通过专用启动动作自动执行这些操作。

.. _ComponentContainer:

组件容器
--------

组件容器是一个宿主进程，允许在同一进程空间内动态加载和管理多个组件。

目前，以下通用组件容器类型可用：

* `component_container <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container.cpp>`__

  * 最通用的组件容器，使用单个 ``SingleThreadedExecutor`` 执行所有组件。

* `component_container_mt <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container_mt.cpp>`__

  * 组件容器使用单个 ``MultiThreadedExecutor`` 执行这些组件。

* `component_container_isolated <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container_isolated.cpp>`__

  * 组件容器为每个组件使用独立的执行器：可以是 ``SingleThreadedExecutor`` （默认）或 ``MultiThreadedExecutor``。

有关执行器类型的更多信息，请参阅 :ref:`TypesOfExecutors`。
有关每种组件容器选项的更多信息，请参阅组合教程中的 :ref:`ComponentContainerTypes`。

编写组件
--------

由于组件只会编译为共享库，因此它没有 ``main`` 函数（见 `Talker 源代码 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/talker_component.cpp>`__）。
组件通常是 ``rclcpp::Node`` 的子类。
由于它不受线程控制，因此在构造函数中不应执行耗时或阻塞任务。
相反，它可以使用定时器来获取周期性通知。
此外，它还可以创建发布器、订阅器、服务器和客户端。

使类成为组件的一个重要方面是，它通过包 ``rclcpp_components`` 中的宏自行注册（见源代码最后一行）。
这使得组件在库加载到正在运行的进程时可被发现——它在某种程度上充当入口点。

另外，一旦组件创建成功，必须向索引注册，才能被工具发现。

.. code-block:: cmake

   add_library(talker_component SHARED src/talker_component.cpp)
   rclcpp_components_register_nodes(talker_component "composition::Talker")
   # 为同一个共享库注册多个组件时，使用多次调用
   # rclcpp_components_register_nodes(talker_component "composition::Talker2")

例如，可查看 :doc:`该教程 <../../Tutorials/Intermediate/Writing-a-Composable-Node>`

.. note::

   为了使组件容器能够找到所需组件，它必须在已加载相应工作区环境的 shell 中执行或启动。

CMake 注册宏
------------

ROS 2 提供了两个用于注册组件的 CMake 宏，它们各有不同用途：

``rclcpp_components_register_node``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
该宏注册组件并生成独立可执行文件。
当您既想要可组合性，又希望节点能够作为独立进程运行时，请使用它。

.. code-block:: cmake

   add_library(talker_component SHARED src/talker_component.cpp)
   rclcpp_components_register_node(talker_component
     PLUGIN "composition::Talker"
     EXECUTABLE talker)

``rclcpp_components_register_nodes``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
该宏注册一个或多个组件供运行时组合使用，不会创建独立可执行文件。
当您希望生成纯组件库并在运行时加载到组件容器时，请使用它。

.. code-block:: cmake

   add_library(talker_component SHARED src/talker_component.cpp)
   rclcpp_components_register_nodes(talker_component "composition::Talker")

使用组件
--------

`composition <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/composition>`__ 包提供了几种不同的组件使用方式。
最常见的三种方式是：

#. 启动一个（`通用容器进程 <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container.cpp>`__），并调用容器提供的 ROS 服务 `load_node <https://github.com/ros2/rcl_interfaces/blob/{REPOS_FILE_BRANCH}/composition_interfaces/srv/LoadNode.srv>`__。
   该 ROS 服务将根据传入的包名、库名加载组件，并在正在运行的进程中启动执行。
   也可以不通过程序化方式调用该 ROS 服务，而是使用 `命令行工具 <https://github.com/ros2/ros2cli/tree/{REPOS_FILE_BRANCH}/ros2component>`__，把命令行参数传给服务来触发加载。
#. 创建一个包含多个在编译期已知节点的 `自定义可执行文件 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/manual_composition.cpp>`__。
   这种方式要求每个组件都有头文件（但对于第一种方式来说，这不是严格要求）。
#. 创建一个启动文件，并使用 ``ros2 launch`` 创建一个容器进程，同时加载多个组件。

实际应用
--------

试试 :doc:`Composition demos <../../Tutorials/Intermediate/Composition>`。
