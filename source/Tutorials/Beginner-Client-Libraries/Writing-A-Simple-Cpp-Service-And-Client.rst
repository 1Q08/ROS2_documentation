.. redirect-from::

    Tutorials/Writing-A-Simple-Cpp-Service-And-Client

.. _CppSrvCli:

编写一个简单的服务和客户端（C++）
=================================

**目标：** 使用 C++ 创建并运行服务和客户端节点。

**教程级别：** 初级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

当 :doc:`节点 <../Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>` 使用 :doc:`服务 <../Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services>` 进行通信时，发送数据请求的节点称为客户端节点，响应请求的节点称为服务节点。
请求和响应的结构由一个 ``.srv`` 文件决定。

这里使用的例子是一个简单的整数加法系统；一个节点请求两个整数的和，另一个节点以结果响应。


前置条件
--------

在前面的教程中，你学习了如何 :doc:`创建工作空间 <./Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <./Creating-Your-First-ROS2-Package>`。

任务
----

1 创建一个包
^^^^^^^^^^^^

打开一个新终端，并 :doc:`source 你的 ROS 2 安装环境 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，这样 ``ros2`` 命令才能正常工作。

进入在 :ref:`之前的教程 <new-directory>` 中创建的 ``ros2_ws`` 目录。

请记住，包应该在 ``src`` 目录中创建，而不是在工作空间的根目录。
进入 ``ros2_ws/src`` 并创建一个新包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_srvcli --dependencies rclcpp example_interfaces

你的终端将返回一条消息，验证你的包 ``cpp_srvcli`` 及其所有必要的文件和文件夹已创建。

``--dependencies`` 参数会自动将必要的依赖行添加到 ``package.xml`` 和 ``CMakeLists.txt``。
``example_interfaces`` 是包含 `.srv 文件 <https://github.com/ros2/example_interfaces/blob/{REPOS_FILE_BRANCH}/srv/AddTwoInts.srv>`__ 的包，你需要用这个文件来结构化你的请求和响应：

.. code-block:: bash

    int64 a
    int64 b
    ---
    int64 sum

前两行是请求的参数，虚线下方是响应。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

因为你在创建包时使用了 ``--dependencies`` 选项，所以你不必手动向 ``package.xml`` 或 ``CMakeLists.txt`` 添加依赖。

不过，和往常一样，请确保将描述、维护者邮箱和姓名以及许可证信息添加到 ``package.xml``。

.. code-block:: xml

  <description>C++ client server tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>


2 编写服务节点
^^^^^^^^^^^^^^

在 ``ros2_ws/src/cpp_srvcli/src`` 目录中，创建一个名为 ``add_two_ints_server.cpp`` 的新文件，并在其中粘贴以下代码：

.. code-block:: C++

      #include "rclcpp/rclcpp.hpp"
      #include "example_interfaces/srv/add_two_ints.hpp"

      #include <memory>

      void add(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
                std::shared_ptr<example_interfaces::srv::AddTwoInts::Response>      response)
      {
        response->sum = request->a + request->b;
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Incoming request\na: %ld" " b: %ld",
                      request->a, request->b);
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "sending back response: [%ld]", (long int)response->sum);
      }

      int main(int argc, char **argv)
      {
        rclcpp::init(argc, argv);

        std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("add_two_ints_server");

        rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service =
          node->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", &add);

        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready to add two ints.");

        rclcpp::spin(node);
        rclcpp::shutdown();
      }

2.1 检查代码
~~~~~~~~~~~~

前两个 ``#include`` 语句是你的包依赖。

``add`` 函数将请求中的两个整数相加，并将和赋值给响应，同时使用日志通知控制台其状态。

.. code-block:: C++

    void add(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
             std::shared_ptr<example_interfaces::srv::AddTwoInts::Response>      response)
    {
        response->sum = request->a + request->b;
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Incoming request\na: %ld" " b: %ld",
            request->a, request->b);
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "sending back response: [%ld]", (long int)response->sum);
    }

``main`` 函数逐行完成以下工作：

* 初始化 ROS 2 C++ 客户端库：

  .. code-block:: C++

    rclcpp::init(argc, argv);

* 创建一个名为 ``add_two_ints_server`` 的节点：

  .. code-block:: C++

    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("add_two_ints_server");

* 为该节点创建一个名为 ``add_two_ints`` 的服务，并通过 ``&add`` 方法自动在网络上广播它：

  .. code-block:: C++

    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service =
    node->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", &add);

* 准备好后打印一条日志消息：

  .. code-block:: C++

    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Ready to add two ints.");

* spin 节点，使服务可用。

  .. code-block:: C++

    rclcpp::spin(node);

2.2 添加可执行文件
~~~~~~~~~~~~~~~~~~

``add_executable`` 宏生成一个可以使用 ``ros2 run`` 运行的可执行文件。
在依赖项下面将以下代码块添加到 ``CMakeLists.txt`` 中，以创建一个名为 ``server`` 的可执行文件：

.. code-block:: cmake

    add_executable(server src/add_two_ints_server.cpp)
    ament_target_dependencies(server rclcpp example_interfaces)

为了让 ``ros2 run`` 能够找到可执行文件，在文件末尾、``ament_package()`` 之前添加以下几行：

.. code-block:: cmake

    install(TARGETS
        server
      DESTINATION lib/${PROJECT_NAME})

你现在可以构建你的包，source 本地安装文件并运行它，但让我们先创建客户端节点，这样你就可以看到完整的系统在运行。

3 编写客户端节点
^^^^^^^^^^^^^^^^

在 ``ros2_ws/src/cpp_srvcli/src`` 目录中，创建一个名为 ``add_two_ints_client.cpp`` 的新文件，并在其中粘贴以下代码：

.. code-block:: C++

  #include "rclcpp/rclcpp.hpp"
  #include "example_interfaces/srv/add_two_ints.hpp"

  #include <chrono>
  #include <cstdlib>
  #include <memory>

  using namespace std::chrono_literals;

  int main(int argc, char **argv)
  {
    rclcpp::init(argc, argv);

    if (argc != 3) {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "usage: add_two_ints_client X Y");
        return 1;
    }

    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("add_two_ints_client");
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client =
      node->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");

    auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    request->a = atoll(argv[1]);
    request->b = atoll(argv[2]);

    while (!client->wait_for_service(1s)) {
      if (!rclcpp::ok()) {
        RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Interrupted while waiting for the service. Exiting.");
        return 0;
      }
      RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "service not available, waiting again...");
    }

    auto result = client->async_send_request(request);
    // Wait for the result.
    if (rclcpp::spin_until_future_complete(node, result) ==
      rclcpp::FutureReturnCode::SUCCESS)
    {
      RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Sum: %ld", result.get()->sum);
    } else {
      RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call service add_two_ints");
    }

    rclcpp::shutdown();
    return 0;
  }


3.1 检查代码
~~~~~~~~~~~~

与服务节点类似，以下几行代码创建节点，然后为该节点创建客户端：

.. code-block:: C++

    std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("add_two_ints_client");
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client =
      node->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");

接下来，创建请求。
其结构由前面提到的 ``.srv`` 文件定义。

.. code-block:: C++

  auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
  request->a = atoll(argv[1]);
  request->b = atoll(argv[2]);

``while`` 循环给客户端 1 秒的时间在网络中搜索服务节点。
如果找不到任何服务节点，它将继续等待。

.. code-block:: C++

  RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "service not available, waiting again...");

如果客户端被取消（例如你在终端中输入 ``Ctrl+C``），它将返回一条错误日志消息，说明它被中断了。

.. code-block:: C++

  RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Interrupted while waiting for the service. Exiting.");

然后客户端发送它的请求，节点 spin 直到它收到响应或失败。

3.2 添加可执行文件
~~~~~~~~~~~~~~~~~~

返回到 ``CMakeLists.txt``，为新节点添加可执行文件和目标。
在从自动生成的文件中删除一些不必要的样板代码后，你的 ``CMakeLists.txt`` 应该看起来像这样：

.. code-block:: cmake

  cmake_minimum_required(VERSION 3.5)
  project(cpp_srvcli)

  find_package(ament_cmake REQUIRED)
  find_package(rclcpp REQUIRED)
  find_package(example_interfaces REQUIRED)

  add_executable(server src/add_two_ints_server.cpp)
  ament_target_dependencies(server rclcpp example_interfaces)

  add_executable(client src/add_two_ints_client.cpp)
  ament_target_dependencies(client rclcpp example_interfaces)

  install(TARGETS
    server
    client
    DESTINATION lib/${PROJECT_NAME})

  ament_package()


4 构建并运行
^^^^^^^^^^^^

在构建之前，最好在工作空间的根目录（``ros2_ws``）运行 ``rosdep`` 来检查缺失的依赖：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

  .. group-tab:: macOS

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

  .. group-tab:: Windows

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。


返回到工作空间的根目录 ``ros2_ws``，并构建你的新包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select cpp_srvcli

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select cpp_srvcli

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select cpp_srvcli

打开一个新终端，进入 ``ros2_ws``，然后 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在运行服务节点：

.. code-block:: console

  $ ros2 run cpp_srvcli server

终端应该返回以下消息，然后等待：

.. code-block:: console

    [INFO] [rclcpp]: Ready to add two ints.

打开另一个终端，再次从 ``ros2_ws`` 内 source 安装文件。
启动客户端节点，后面跟上任意两个以空格分隔的整数。
例如，如果你选择 ``2`` 和 ``3``，客户端会收到这样的响应：

.. code-block:: console

  $ ros2 run cpp_srvcli client 2 3
  [INFO] [rclcpp]: Sum: 5

返回到服务节点正在运行的终端。
你会看到它在收到请求时发布了日志消息，以及它接收到的数据和它发回的响应：

.. code-block:: console

    [INFO] [rclcpp]: Incoming request
    a: 2 b: 3
    [INFO] [rclcpp]: sending back response: [5]

在服务终端中输入 ``Ctrl+C`` 来停止节点的 spin。

总结
----

你创建了两个节点，通过服务请求和响应数据。
你将它们的依赖和可执行文件添加到了包配置文件中，这样你就可以构建并运行它们，并看到服务/客户端系统的实际运行。

后续步骤
--------

在最后几个教程中，你一直在利用接口通过话题和服务传递数据。
接下来，你将学习如何 :doc:`创建自定义接口 <./Custom-ROS2-Interfaces>`。

相关内容
--------

* 有多种方式可以用 C++ 编写服务和客户端；请查看 `ros2/examples <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclcpp/services>`_ 仓库中的 ``minimal_service`` 和 ``minimal_client`` 包。
