.. redirect-from::

   Concepts/About-Composition

组合
====

.. contents:: 目录
   :local:

ROS 1 - 节点与 Nodelet
----------------------

在 ROS 1 中，你可以将代码编写为 `ROS 节点 <https://wiki.ros.org/Nodes>`__ 或 `ROS nodelet <https://wiki.ros.org/nodelet>`__。
ROS 1 节点被编译为可执行文件。
另一方面，ROS 1 nodelet 被编译为共享库，然后在运行时由容器进程加载。

ROS 2 - 统一的 API
------------------

在 ROS 2 中，推荐编写代码的方式类似于 nodelet——我们称之为 ``Component``。
这使得向现有代码添加通用概念变得容易，例如 `生命周期 <https://design.ros2.org/articles/node_lifecycle.html>`__。
ROS 1 最大的缺点是存在不同的 API，而 ROS 2 避免了这一点，因为两种方式使用相同的 API。

.. note::

   仍然可以使用类似节点的“编写自己的 main”风格，但对于常见情况，不推荐这样做。

通过将进程布局作为部署时的决策，用户可以在以下两者之间进行选择：

* 在单独的进程中运行多个节点，其优点是进程/故障隔离以及更容易调试单个节点，以及
* 在单个进程中运行多个节点，开销更低，并且可以选择更高效的通信（参见 :doc:`进程内通信 <../../Tutorials/Demos/Intra-Process-Communication>`）。

此外，``ros2 launch`` 可用于通过专门的启动动作来自动化这些操作。

.. _ComponentContainer:

组件容器
--------

组件容器是一个宿主进程，允许你在运行时在同一进程空间内加载和管理多个组件。

目前，有以下几种通用的组件容器类型：

* `component_container <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container.cpp>`__

  * 最通用的组件容器，使用单个 ``SingleThreadedExecutor`` 来执行所有组件。

* `component_container_mt <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container_mt.cpp>`__

  * 使用单个 ``MultiThreadedExecutor`` 来执行组件的组件容器。

* `component_container_isolated <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container_isolated.cpp>`__

  * 为每个组件使用专用执行器的组件容器：``SingleThreadedExecutor`` （默认）或 ``MultiThreadedExecutor``。

有关执行器类型的更多信息，请参阅 :ref:`TypesOfExecutors`。
有关每个组件容器选项的更多信息，请参阅组合教程中的 :ref:`ComponentContainerTypes`。

编写组件
--------

由于组件只构建为共享库，因此它没有 ``main`` 函数（参见 `Talker 源代码 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/talker_component.cpp>`__）。
组件通常是 ``rclcpp::Node`` 的子类。
由于它不控制线程，因此不应在其构造函数中执行任何长时间运行或阻塞的任务。
相反，它可以使用定时器来获取周期性通知。
此外，它可以创建发布者、订阅、服务器和客户端。

使这样的类成为组件的一个重要方面是，该类使用 ``rclcpp_components`` 包中的宏来注册自己（参见源代码中的最后一行）。
这使得组件在其库被加载到运行中的进程时可被发现——它充当一种入口点。

此外，一旦创建了组件，就必须将其注册到索引中，以便工具能够发现它。

.. code-block:: cmake

   add_library(talker_component SHARED src/talker_component.cpp)
   rclcpp_components_register_nodes(talker_component "composition::Talker")
   # To register multiple components in the same shared library, use multiple calls
   # rclcpp_components_register_nodes(talker_component "composition::Talker2")

例如，:doc:`查看本教程 <../../Tutorials/Intermediate/Writing-a-Composable-Node>`

.. note::

   为了让 component_container 能够找到所需的组件，必须从已 source 相应工作空间的 shell 中执行或启动它。

CMake 注册宏
------------

ROS 2 提供两个用于注册组件的 CMake 宏，每个宏有不同的用途：

``rclcpp_components_register_node``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
此宏注册一个组件并生成一个独立的可执行文件。
当你既希望组件可组合，又希望节点能够作为独立进程运行时，请使用此宏。

.. code-block:: cmake

   add_library(talker_component SHARED src/talker_component.cpp)
   rclcpp_components_register_node(talker_component
     PLUGIN "composition::Talker"
     EXECUTABLE talker)

``rclcpp_components_register_nodes``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
此宏注册一个或多个用于运行时组合的组件，**不** 创建独立的可执行文件。
当你希望创建纯组件库并在运行时加载到组件容器中时，请使用此宏。

.. code-block:: cmake

   add_library(talker_component SHARED src/talker_component.cpp)
   rclcpp_components_register_nodes(talker_component "composition::Talker")

使用组件
--------

`composition <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/composition>`__ 包包含几种使用组件的不同方法。
三种最常见的方法是：

#. 启动一个（`通用容器进程 <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp_components/src/component_container.cpp>`__）并调用容器提供的 ROS 服务 `load_node <https://github.com/ros2/rcl_interfaces/blob/{REPOS_FILE_BRANCH}/composition_interfaces/srv/LoadNode.srv>`__。
   然后，ROS 服务将加载由传入的包名和库名指定的组件，并在运行中的进程内开始执行它。
   除了以编程方式调用 ROS 服务之外，你还可以使用 `命令行工具 <https://github.com/ros2/ros2cli/tree/{REPOS_FILE_BRANCH}/ros2component>`__ 通过传入的命令行参数来调用 ROS 服务
#. 创建一个 `自定义可执行文件 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/manual_composition.cpp>`__，其中包含在编译时已知的多个节点。
   这种方法要求每个组件都有一个头文件（第一种情况并不严格要求这一点）。
#. 创建一个 launch 文件，并使用 ``ros2 launch`` 创建加载了多个组件的容器进程。

实际应用
--------

尝试 :doc:`组合演示 <../../Tutorials/Intermediate/Composition>`。
