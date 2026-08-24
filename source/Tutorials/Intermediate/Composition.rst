.. redirect-from::

    Composition
    Tutorials/Composition

在单个进程中组合多个节点
========================

.. contents:: 目录
   :depth: 2
   :local:

**目标：** 将多个节点组合到单个进程中。

**教程级别：** 中级

**时间：** 20 分钟

背景
----

请参阅 :doc:`概念文章 <../../Concepts/Intermediate/About-Composition>`。

有关如何编写可组合节点的信息，请 :doc:`查阅本教程 <Writing-a-Composable-Node>`。

前提条件
--------

本教程使用来自 `rclcpp_components <https://github.com/ros2/rclcpp/tree/{REPOS_FILE_BRANCH}/rclcpp_components>`__、`ros2component <https://github.com/ros2/ros2cli/tree/{REPOS_FILE_BRANCH}/ros2component>`__、`composition <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/composition>`__ 和 `image_tools <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/image_tools>`__ 软件包中的可执行文件。
如果你已按照 :doc:`安装说明 <../../Installation>` 为你的平台进行了安装，这些应该已经安装。

运行演示
--------

发现可用组件
^^^^^^^^^^^^

要查看工作空间中注册并可用的组件，请在 shell 中执行以下命令：

.. code-block:: console

   $ ros2 component types
   (... components of other packages here)
   composition
     composition::Talker
     composition::Listener
     composition::NodeLikeListener
     composition::Server
     composition::Client
   (... components of other packages here)


使用 ROS 服务与发布者和订阅者进行运行时组合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在第一个 shell 中，启动组件容器：

.. code-block:: console

   $ ros2 run rclcpp_components component_container

打开第二个 shell，并通过 ``ros2`` 命令行工具验证容器正在运行。
你应该能看到组件的名称：

.. code-block:: console

   $ ros2 component list
   /ComponentManager

在第二个 shell 中加载 talker 组件（参见 `talker <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/talker_component.cpp>`__ 源代码）。
该命令将返回已加载组件的唯一 ID 以及节点名称：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Talker
   Loaded component 1 into '/ComponentManager' container node as '/talker'

现在第一个 shell 应显示一条消息，表明组件已加载，以及发布消息的重复消息。

在第二个 shell 中运行另一个命令以加载 listener 组件（参见 `listener <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/listener_component.cpp>`__ 源代码）：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Listener
   Loaded component 2 into '/ComponentManager' container node as '/listener'

现在可以使用 ``ros2`` 命令行工具检查容器的状态：

.. code-block:: console

   $ ros2 component list
   /ComponentManager
      1  /talker
      2  /listener

现在第一个 shell 应显示每条收到的消息的重复输出。

使用 ROS 服务与服务器和客户端进行运行时组合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

服务器和客户端的示例非常相似。

在第一个 shell 中：

.. code-block:: console

   $ ros2 run rclcpp_components component_container

在第二个 shell 中（参见 `server <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/server_component.cpp>`__ 和 `client <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/client_component.cpp>`__ 源代码）：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Server
   $ ros2 component load /ComponentManager composition composition::Client

在这种情况下，客户端向服务器发送请求，服务器处理请求并回复响应，客户端打印收到的响应。

使用硬编码节点的编译时组合
^^^^^^^^^^^^^^^^^^^^^^^^^^

此演示展示同一共享库可被复用，以编译一个无需使用 ROS 接口即可运行多个组件的单一可执行文件。
该可执行文件包含上述全部四个组件：talker 和 listener 以及 server 和 client，这些都在 main 函数中硬编码。

在 shell 中调用（参见 `源代码 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/manual_composition.cpp>`__）：

.. code-block:: console

   $ ros2 run composition manual_composition

这应显示来自两对组件的重复消息：talker 和 listener 以及 server 和 client。

.. note::

   手动组合的组件不会显示在 ``ros2 component list`` 命令行工具的输出中。

使用 dlopen 进行运行时组合
^^^^^^^^^^^^^^^^^^^^^^^^^^

此演示展示了运行时组合的另一种方法，通过创建一个通用容器进程并显式传入要加载的库，而无需使用 ROS 接口。
该进程将打开每个库，并在库中创建每个“rclcpp::Node”类的一个实例（`源代码 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/dlopen_composition.cpp>`__）。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ ros2 run composition dlopen_composition `ros2 pkg prefix composition`/lib/libtalker_component.so `ros2 pkg prefix composition`/lib/liblistener_component.so

  .. group-tab:: macOS

    .. code-block:: console

       $ ros2 run composition dlopen_composition `ros2 pkg prefix composition`/lib/libtalker_component.dylib `ros2 pkg prefix composition`/lib/liblistener_component.dylib

  .. group-tab:: Windows

    .. code-block:: console

       $ ros2 pkg prefix composition

    获取 composition 安装路径。
    然后调用

    .. code-block:: console

       $ ros2 run composition dlopen_composition <path_to_composition_install>\bin\talker_component.dll <path_to_composition_install>\bin\listener_component.dll

现在 shell 应显示每条发送和接收的消息的重复输出。

.. note::

   dlopen 组合的组件不会显示在 ``ros2 component list`` 命令行工具的输出中。


使用 launch 操作进行组合
^^^^^^^^^^^^^^^^^^^^^^^^

虽然命令行工具对于调试和诊断组件配置很有用，但同时启动一组组件通常更方便。
为了自动化此操作，我们可以使用一个 `launch 文件 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/launch/composition_demo_launch.py>`__：

.. code-block:: console

   $ ros2 launch composition composition_demo_launch.py


高级主题
--------

既然我们已经看到了组件的基本操作，我们可以讨论一些更高级的主题。

.. _ComponentContainerTypes:

组件容器类型
^^^^^^^^^^^^

如 :ref:`ComponentContainer` 中所介绍，有几种具有不同选项的组件容器类型。
你可以根据需求选择最合适的组件容器类型。

* ``component_container`` （无可用选项/参数）

   .. code-block:: console

      $ ros2 run rclcpp_components component_container

* 带 ``MultiThreadedExecutor`` 的 ``component_container_mt``，由 4 个线程组成。
   * ``thread_num`` 参数选项可用于指定 ``MultiThreadedExecutor`` 中的线程数。

   .. code-block:: console

      $ ros2 run rclcpp_components component_container_mt --ros-args -p thread_num:=4

* 为每个组件使用 ``MultiThreadedExecutor`` 的 ``component_container_isolated``。
   * ``--use_multi_threaded_executor`` 参数指定每个组件使用的执行器类型为 ``MultiThreadedExecutor``。

   .. code-block:: console

      $ ros2 run rclcpp_components component_container_isolated --use_multi_threaded_executor

卸载组件
^^^^^^^^

在第一个 shell 中，启动组件容器：

.. code-block:: console

   $ ros2 run rclcpp_components component_container

通过 ``ros2`` 命令行工具验证容器正在运行：

.. code-block:: console

   $ ros2 component list
   /ComponentManager

在第二个 shell 中，像之前一样同时加载 talker 和 listener：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Talker
   Loaded component 1 into '/ComponentManager' container node as '/talker'
   $ ros2 component load /ComponentManager composition composition::Listener
   Loaded component 2 into '/ComponentManager' container node as '/listener'

组件的唯一 ID 在加载时会被打印出来。
既然它们已加载，你也可以通过列出所有组件来获取其唯一 ID：

.. code-block:: console

   $ ros2 component list
   /ComponentManager
     1  /talker
     2  /listener

使用唯一 ID 从组件容器中卸载组件。

.. code-block:: console

   $ ros2 component unload /ComponentManager 1 2
   Unloaded component 1 from '/ComponentManager' container
   Unloaded component 2 from '/ComponentManager' container

在第一个 shell 中，验证来自 talker 和 listener 的重复消息已停止。


重映射容器名称和命名空间
^^^^^^^^^^^^^^^^^^^^^^^^

组件管理器的名称和命名空间可以通过标准命令行参数进行重映射：

.. code-block:: console

   $ ros2 run rclcpp_components component_container --ros-args -r __node:=MyContainer -r __ns:=/ns

在第二个 shell 中，可以使用更新后的容器名称加载组件：

.. code-block:: console

   $ ros2 component load /ns/MyContainer composition composition::Listener

.. note::

   容器的命名空间重映射不会影响已加载的组件。


重映射组件名称和命名空间
^^^^^^^^^^^^^^^^^^^^^^^^

组件名称和命名空间可以通过 load 命令的参数进行调整。

在第一个 shell 中，启动组件容器：

.. code-block:: console

   $ ros2 run rclcpp_components component_container


一些重映射名称和命名空间的示例。

重映射节点名称：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Talker --node-name talker2

重映射命名空间：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Talker --node-namespace /ns

同时重映射两者：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Talker --node-name talker3 --node-namespace /ns2

现在使用 ``ros2`` 命令行工具：

.. code-block:: console

   $ ros2 component list
   /ComponentManager
      1  /talker2
      2  /ns/talker
      3  /ns2/talker3

.. note::

   容器的命名空间重映射不会影响已加载的组件。

向组件传递参数值
^^^^^^^^^^^^^^^^

``ros2 component load`` 命令行支持在节点构造时向其传递任意参数。
此功能可按如下方式使用：

.. code-block:: console

   $ ros2 component load /ComponentManager image_tools image_tools::Cam2Image -p burger_mode:=true
   $ ros2 run rqt_image_view rqt_image_view  # 显示弹跳的汉堡，而不是来自相机的图像

向组件传递额外参数
^^^^^^^^^^^^^^^^^^

``ros2 component load`` 命令行支持向组件管理器传递特定选项，以便在构造节点时使用。

以下示例展示了额外参数 ``use_intra_process_comms`` 和 ``forward_global_arguments`` 的用法：

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Talker -e use_intra_process_comms:=true -e forward_global_arguments:=false

支持以下额外参数。

.. list-table:: 组件管理器的额外参数
   :widths: 15 15 15 15
   :header-rows: 1

   * - 参数
     - 类型
     - 默认值
     - 描述
   * - ``forward_global_arguments``
     - Boolean
     - True
     - 加载时将全局参数应用于组件节点。
   * - ``use_intra_process_comms``
     - Boolean
     - False
     - 在组件节点中启用进程内通信。


作为共享库的可组合节点
----------------------

如果你想将可组合节点作为共享库从软件包中导出，并在另一个进行链接时组合的软件包中使用该节点，请在 CMake 文件中添加导入下游软件包中实际目标的代码。

然后安装生成的文件并导出生成的文件。

此处可看到一个实际示例：`ROS Discourse - Ament 共享库最佳实践 <https://discourse.openrobotics.org/t/ament-best-practice-for-sharing-libraries/3602>`__

组合非节点派生的组件
--------------------

在 ROS 2 中，组件可以更高效地利用系统资源，并提供了一项强大的功能，使你能够创建不绑定到特定节点的可重用功能。

使用组件的一个优势是，它们允许你以独立可执行文件或共享库的形式创建非节点派生的功能，并可根据需要加载到 ROS 系统中。

要创建非节点派生的组件，请遵循以下准则：

1. 实现一个接受 ``const rclcpp::NodeOptions&`` 作为参数的构造函数。
2. 实现 ``get_node_base_interface()`` 方法，该方法应返回 ``NodeBaseInterface::SharedPtr``。
   你可以使用在构造函数中创建的节点的 ``get_node_base_interface()`` 方法来提供此接口。

以下是一个非节点派生的组件示例，它监听 ROS 主题：`node_like_listener_component <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/composition/src/node_like_listener_component.cpp>`__。

有关此主题的更多信息，你可以参考此 `讨论 <https://github.com/ros2/rclcpp/issues/2110#issuecomment-1454228192>`__。
