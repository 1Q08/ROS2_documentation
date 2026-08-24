.. redirect-from::

    Tutorials/Actions/Writing-a-Cpp-Action-Server-Client

.. _ActionsCpp:

编写一个 action 服务器和客户端（C++）
=====================================

**目标：** 用 C++ 实现一个 action 服务器和客户端。

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

Action 是 ROS 中一种异步通信的形式。
*Action 客户端* 向 *action 服务器* 发送目标请求。
*Action 服务器* 向 *action 客户端* 发送目标反馈和结果。

先决条件
--------

你需要 ``custom_action_interfaces`` 包以及在前面教程 :doc:`../Creating-an-Action` 中定义的 ``Fibonacci.action`` 接口。

任务
----

1 创建 custom_action_cpp 包
^^^^^^^^^^^^^^^^^^^^^^^^^^^

正如我们在 :doc:`../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package` 教程中看到的，我们需要创建一个新包来存放我们的 C++ 和支持代码。

1.1 创建 custom_action_cpp 包
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

进入你在 :doc:`前面教程 <../Creating-an-Action>` 中创建的 action 工作区（记得 source 工作区），并为 C++ action 服务器创建一个新包：


.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ cd ~/ros2_ws/src
      $ ros2 pkg create --dependencies custom_action_interfaces rclcpp rclcpp_action rclcpp_components --license Apache-2.0 -- custom_action_cpp

  .. group-tab:: macOS

    .. code-block:: console

      $ cd ~/ros2_ws/src
      $ ros2 pkg create --dependencies custom_action_interfaces rclcpp rclcpp_action rclcpp_components --license Apache-2.0 -- custom_action_cpp

  .. group-tab:: Windows

    .. code-block:: console

      $ cd \ros2_ws\src
      $ ros2 pkg create --dependencies custom_action_interfaces rclcpp rclcpp_action rclcpp_components --license Apache-2.0 -- custom_action_cpp

1.2 添加可见性控制
~~~~~~~~~~~~~~~~~~

为了使包在 Windows 上能编译和运行，我们需要添加一些 "可见性控制"。
更多细节，请参阅 :ref:`Windows 技巧与窍门文档中的 Windows 符号可见性 <Windows_Symbol_Visibility>`。

打开 ``custom_action_cpp/include/custom_action_cpp/visibility_control.h``，并把以下代码放进去：

.. code-block:: c++

  #ifndef CUSTOM_ACTION_CPP__VISIBILITY_CONTROL_H_
  #define CUSTOM_ACTION_CPP__VISIBILITY_CONTROL_H_

  #ifdef __cplusplus
  extern "C"
  {
  #endif

  // This logic was borrowed (then namespaced) from the examples on the gcc wiki:
  //     https://gcc.gnu.org/wiki/Visibility

  #if defined _WIN32 || defined __CYGWIN__
    #ifdef __GNUC__
      #define CUSTOM_ACTION_CPP_EXPORT __attribute__ ((dllexport))
      #define CUSTOM_ACTION_CPP_IMPORT __attribute__ ((dllimport))
    #else
      #define CUSTOM_ACTION_CPP_EXPORT __declspec(dllexport)
      #define CUSTOM_ACTION_CPP_IMPORT __declspec(dllimport)
    #endif
    #ifdef CUSTOM_ACTION_CPP_BUILDING_DLL
      #define CUSTOM_ACTION_CPP_PUBLIC CUSTOM_ACTION_CPP_EXPORT
    #else
      #define CUSTOM_ACTION_CPP_PUBLIC CUSTOM_ACTION_CPP_IMPORT
    #endif
    #define CUSTOM_ACTION_CPP_PUBLIC_TYPE CUSTOM_ACTION_CPP_PUBLIC
    #define CUSTOM_ACTION_CPP_LOCAL
  #else
    #define CUSTOM_ACTION_CPP_EXPORT __attribute__ ((visibility("default")))
    #define CUSTOM_ACTION_CPP_IMPORT
    #if __GNUC__ >= 4
      #define CUSTOM_ACTION_CPP_PUBLIC __attribute__ ((visibility("default")))
      #define CUSTOM_ACTION_CPP_LOCAL  __attribute__ ((visibility("hidden")))
    #else
      #define CUSTOM_ACTION_CPP_PUBLIC
      #define CUSTOM_ACTION_CPP_LOCAL
    #endif
    #define CUSTOM_ACTION_CPP_PUBLIC_TYPE
  #endif

  #ifdef __cplusplus
  }
  #endif

  #endif  // CUSTOM_ACTION_CPP__VISIBILITY_CONTROL_H_

2 编写一个 action 服务器
^^^^^^^^^^^^^^^^^^^^^^^^

让我们专注于编写一个 action 服务器，它使用我们在 :doc:`../Creating-an-Action` 教程中创建的 action 来计算斐波那契数列。

2.1 编写 action 服务器代码
~~~~~~~~~~~~~~~~~~~~~~~~~~

打开 ``custom_action_cpp/src/fibonacci_action_server.cpp``，并把以下代码放进去：

.. literalinclude:: scripts/server.cpp
    :language: c++

前几行包含了我们编译所需的所有头文件。

接下来我们创建一个派生自 ``rclcpp::Node`` 的类：

.. literalinclude:: scripts/server.cpp
    :language: c++
    :lines: 14

``FibonacciActionServer`` 类的构造函数将节点名初始化为 ``fibonacci_action_server``：

.. literalinclude:: scripts/server.cpp
    :language: c++
    :lines: 21-22

构造函数还实例化了一个新的 action 服务器：

.. literalinclude:: scripts/server.cpp
    :language: c++
    :lines: 52-57

一个 action 服务器需要 6 样东西：

1. 模板化的 action 类型名：``Fibonacci``。
2. 一个要添加 action 的 ROS 2 节点：``this``。
3. action 名称：``'fibonacci'``。
4. 一个处理目标的回调函数：``handle_goal``
5. 一个处理取消的回调函数：``handle_cancel``。
6. 一个处理目标接受的回调函数：``handle_accept``。

各种回调的实现是在构造函数中使用 `lambda 表达式 <https://en.cppreference.com/w/cpp/language/lambda>`_ 完成的。
注意所有回调都需要快速返回，否则我们就有可能让执行器饥饿。

我们从处理新目标的回调开始：

.. literalinclude:: scripts/server.cpp
    :language: c++
    :lines: 26-33

这个实现只是接受所有目标。

接下来是处理取消的回调：

.. literalinclude:: scripts/server.cpp
    :language: c++
    :lines: 35-41

这个实现只是告诉客户端它接受了取消。

最后一个回调接受一个新目标并开始处理它：

.. literalinclude:: scripts/server.cpp
    :language: c++
    :lines: 43-50

由于执行是一个长期运行的操作，我们启动一个线程来做实际工作，并从 ``handle_accepted`` 快速返回。

所有进一步的处理和更新都在新线程的 ``execute`` 方法中完成：

.. literalinclude:: scripts/server.cpp
    :language: c++
    :lines: 63-96

这个工作线程每秒处理斐波那契数列的一个序列号，为每一步发布一个反馈更新。
当它处理完后，将 ``goal_handle`` 标记为成功，然后退出。

我们现在有了一个完全可用的 action 服务器。
让我们把它构建并运行起来。

2.2 编译 action 服务器
~~~~~~~~~~~~~~~~~~~~~~

在前一节中，我们把 action 服务器代码放了进去。
为了让它编译和运行，我们还需要做几件额外的事情。

首先，我们需要设置 CMakeLists.txt，以便编译 action 服务器。
打开 ``custom_action_cpp/CMakeLists.txt``，并在 ``find_package`` 调用之后添加以下内容：

.. code-block:: cmake

  add_library(action_server SHARED
    src/fibonacci_action_server.cpp)
  target_include_directories(action_server PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
  target_compile_definitions(action_server
    PRIVATE "CUSTOM_ACTION_CPP_BUILDING_DLL")
  ament_target_dependencies(action_server
    "custom_action_interfaces"
    "rclcpp"
    "rclcpp_action"
    "rclcpp_components")
  rclcpp_components_register_node(action_server PLUGIN "custom_action_cpp::FibonacciActionServer" EXECUTABLE fibonacci_action_server)
  install(TARGETS
    action_server
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin)

现在我们可以编译包了。
前往 ``ros2_ws`` 的顶层，然后运行：

.. code-block:: console

  $ colcon build

这应该会编译整个工作区，包括 ``custom_action_cpp`` 包中的 ``fibonacci_action_server``。

2.3 运行 action 服务器
~~~~~~~~~~~~~~~~~~~~~~

现在我们已经构建好了 action 服务器，可以运行它了。
Source 我们刚构建的工作区（``ros2_ws``），并尝试运行 action 服务器：

.. code-block:: console

  $ ros2 run custom_action_cpp fibonacci_action_server

3 编写一个 action 客户端
^^^^^^^^^^^^^^^^^^^^^^^^

3.1 编写 action 客户端代码
~~~~~~~~~~~~~~~~~~~~~~~~~~

打开 ``custom_action_cpp/src/fibonacci_action_client.cpp``，并把以下代码放进去：

.. literalinclude:: scripts/client.cpp
    :language: c++

前几行包含了我们编译所需的所有头文件。

接下来我们创建一个派生自 ``rclcpp::Node`` 的类：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 15

``FibonacciActionClient`` 类的构造函数将节点名初始化为 ``fibonacci_action_client``：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 20-22

构造函数还实例化了一个新的 action 客户端：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 24-26

一个 action 客户端需要 3 样东西：

1. 模板化的 action 类型名：``Fibonacci``。
2. 一个要添加 action 客户端的 ROS 2 节点：``this``。
3. action 名称：``'fibonacci'``。

我们还实例化一个 ROS 定时器，它将触发对 ``send_goal`` 的唯一一次调用：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 28-31

当定时器到期时，它会调用 ``send_goal``：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 34-96

这个函数做以下事情：

1. 取消定时器（这样它只会被调用一次）。
2. 等待 action 服务器上线。
3. 实例化一个新的 ``Fibonacci::Goal``。
4. 设置响应、反馈和结果回调。
5. 将目标发送到服务器。

当服务器收到并接受目标时，它会向客户端发送一个响应。
该响应由 ``goal_response_callback`` 处理：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 51-58

假设目标被服务器接受，它将开始处理。
发送给客户端的任何反馈将由 ``feedback_callback`` 处理：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 60-70

当服务器处理完毕后，它会向客户端返回一个结果。
结果由 ``result_callback`` 处理：

.. literalinclude:: scripts/client.cpp
    :language: c++
    :lines: 72-94

我们现在有了一个完全可用的 action 客户端。
让我们把它构建并运行起来。

3.2 编译 action 客户端
~~~~~~~~~~~~~~~~~~~~~~

在前一节中，我们把 action 客户端代码放了进去。
为了让它编译和运行，我们还需要做几件额外的事情。

首先，我们需要设置 CMakeLists.txt，以便编译 action 客户端。
打开 ``custom_action_cpp/CMakeLists.txt``，并在 ``find_package`` 调用之后添加以下内容：

.. code-block:: cmake

  add_library(action_client SHARED
    src/fibonacci_action_client.cpp)
  target_include_directories(action_client PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
  target_compile_definitions(action_client
    PRIVATE "CUSTOM_ACTION_CPP_BUILDING_DLL")
  ament_target_dependencies(action_client
    "custom_action_interfaces"
    "rclcpp"
    "rclcpp_action"
    "rclcpp_components")
  rclcpp_components_register_node(action_client PLUGIN "custom_action_cpp::FibonacciActionClient" EXECUTABLE fibonacci_action_client)
  install(TARGETS
    action_client
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin)

现在我们可以编译包了。
前往 ``ros2_ws`` 的顶层，然后运行：

.. code-block:: console

  $ colcon build

这应该会编译整个工作区，包括 ``custom_action_cpp`` 包中的 ``fibonacci_action_client``。

3.3 运行 action 客户端
~~~~~~~~~~~~~~~~~~~~~~

现在我们已经构建好了 action 客户端，可以运行它了。
首先确保 action 服务器在另一个终端中运行。
现在 source 我们刚构建的工作区（``ros2_ws``），并尝试运行 action 客户端：

.. code-block:: console

  $ ros2 run custom_action_cpp fibonacci_action_client

你应该会看到关于目标被接受、反馈被打印以及最终结果的日志消息。

总结
----

在本教程中，你逐行组装了一个 C++ action 服务器和 action 客户端，并配置它们来交换目标、反馈和结果。

相关内容
--------

* 用 C++ 编写 action 服务器和客户端有多种方法；请查看 `ros2/examples <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclcpp>`_ 仓库中的 ``minimal_action_server`` 和 ``minimal_action_client`` 包。

* 有关 ROS action 的更多详细信息，请参阅 `设计文章 <http://design.ros2.org/articles/actions.html>`__。
