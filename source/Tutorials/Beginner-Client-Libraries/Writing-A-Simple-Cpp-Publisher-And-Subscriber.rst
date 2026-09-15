.. redirect-from::

    Tutorials/Writing-A-Simple-Cpp-Publisher-And-Subscriber

.. _CppPubSub:

编写一个简单的发布者和订阅者（C++）
===================================

**目标：** 使用 C++ 创建并运行发布者和订阅者节点。

**教程级别：** 初级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

:doc:`节点 <../Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>` 是通过 ROS 图进行通信的可执行进程。
在本教程中，节点将通过 :doc:`话题 <../Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics>` 以字符串消息的形式相互传递信息。
这里使用的例子是一个简单的“说者”（talker）和“听者”（listener）系统；一个节点发布数据，另一个节点订阅话题以接收该数据。

这些例子中使用的代码可以在 `这里 <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclcpp/topics>`__ 找到。

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
因此，进入 ``ros2_ws/src``，然后运行包创建命令：

.. code-block:: console

    $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_pubsub

你的终端将返回一条消息，验证你的包 ``cpp_pubsub`` 及其所有必要的文件和文件夹已创建。

进入 ``ros2_ws/src/cpp_pubsub/src``。
请记住，这是任何 CMake 包中包含可执行文件的源文件所在的目录。


2 编写发布者节点
^^^^^^^^^^^^^^^^

通过输入以下命令下载示例 talker 代码：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

            $ wget -O publisher_lambda_function.cpp https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_publisher/lambda.cpp

   .. group-tab:: macOS

      .. code-block:: console

            $ wget -O publisher_lambda_function.cpp https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_publisher/lambda.cpp

   .. group-tab:: Windows

      在 Windows 命令行提示符中：

      .. code-block:: console

            $ curl -sk https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_publisher/lambda.cpp -o publisher_lambda_function.cpp

      或在 powershell 中：

      .. code-block:: console

            $ curl https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_publisher/lambda.cpp -o publisher_lambda_function.cpp

现在会有一个名为 ``publisher_lambda_function.cpp`` 的新文件。
使用你喜欢的文本编辑器打开该文件。

.. code-block:: C++

    #include <chrono>
    #include <memory>
    #include <string>

    #include "rclcpp/rclcpp.hpp"
    #include "std_msgs/msg/string.hpp"

    using namespace std::chrono_literals;

    /* This example creates a subclass of Node and uses a fancy C++11 lambda
    * function to shorten the callback syntax, at the expense of making the
    * code somewhat more difficult to understand at first glance. */

    class MinimalPublisher : public rclcpp::Node
    {
    public:
      MinimalPublisher()
      : Node("minimal_publisher"), count_(0)
      {
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
        auto timer_callback =
          [this]() -> void {
            auto message = std_msgs::msg::String();
            message.data = "Hello, world! " + std::to_string(this->count_++);
            RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
            this->publisher_->publish(message);
          };
        timer_ = this->create_wall_timer(500ms, timer_callback);
      }

    private:
      rclcpp::TimerBase::SharedPtr timer_;
      rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
      size_t count_;
    };

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<MinimalPublisher>());
      rclcpp::shutdown();
      return 0;
    }

2.1 检查代码
~~~~~~~~~~~~

代码顶部包含你将使用的标准 C++ 头文件。
在标准 C++ 头文件之后是 ``rclcpp/rclcpp.hpp`` 的包含，它允许你使用 ROS 2 系统最常用的部分。
最后是 ``std_msgs/msg/string.hpp``，它包含你将用于发布数据的内置消息类型。

.. code-block:: C++

    #include <chrono>
    #include <memory>
    #include <string>

    #include "rclcpp/rclcpp.hpp"
    #include "std_msgs/msg/string.hpp"

    using namespace std::chrono_literals;

这些行表示节点的依赖。
请记住，依赖必须添加到 ``package.xml`` 和 ``CMakeLists.txt`` 中，你将在下一节中完成。

下一行通过继承 ``rclcpp::Node`` 创建节点类 ``MinimalPublisher``。
代码中的每个 ``this`` 都指代节点。

.. code-block:: C++

    class MinimalPublisher : public rclcpp::Node

公有构造函数将节点命名为 ``minimal_publisher``，并将 ``count_`` 初始化为 0。
在构造函数内部，发布者使用 ``String`` 消息类型、话题名称 ``topic`` 以及限制消息积压所需的队列大小进行初始化。
接下来，声明了一个名为 ``timer_callback`` 的 `lambda 函数 <https://en.cppreference.com/w/cpp/language/lambda>`_。
它对当前对象 ``this`` 进行引用捕获，不接受输入参数并返回 void。
``timer_callback`` 函数创建一个新的 ``String`` 类型消息，将其数据设置为所需字符串并发布它。
``RCLCPP_INFO`` 宏确保每条发布的消息都打印到控制台。
最后，``timer_`` 被初始化，这会导致 ``timer_callback`` 函数每秒执行两次。

.. code-block:: C++

    public:
      MinimalPublisher()
      : Node("minimal_publisher"), count_(0)
      {
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
        auto timer_callback =
          [this]() -> void {
            auto message = std_msgs::msg::String();
            message.data = "Hello, world! " + std::to_string(this->count_++);
            RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
            this->publisher_->publish(message);
          };
        timer_ = this->create_wall_timer(500ms, timer_callback);
      }

在类的底部是计时器、发布者和计数器字段的声明。

.. code-block:: C++

    private:
      rclcpp::TimerBase::SharedPtr timer_;
      rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
      size_t count_;

在 ``MinimalPublisher`` 类之后是 ``main``，节点在这里实际执行。
``rclcpp::init`` 初始化 ROS 2，``rclcpp::spin`` 开始处理来自节点的数据，包括来自计时器的回调。

.. code-block:: C++

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<MinimalPublisher>());
      rclcpp::shutdown();
      return 0;
    }

2.2 添加依赖
~~~~~~~~~~~~

返回上一级目录，进入 ``ros2_ws/src/cpp_pubsub``，那里已经为你创建了 ``CMakeLists.txt`` 和 ``package.xml`` 文件。

用文本编辑器打开 ``package.xml``。

如 :doc:`之前的教程 <./Creating-Your-First-ROS2-Package>` 所述，请确保填写 ``<description>``、``<maintainer>`` 和 ``<license>`` 标签：

.. code-block:: xml

      <description>Examples of minimal publisher/subscriber using rclcpp</description>
      <maintainer email="you@email.com">Your Name</maintainer>
      <license>Apache-2.0</license>

在 ``ament_cmake`` 构建工具依赖之后添加一行，并粘贴与你的节点的 include 语句相对应的以下依赖：

.. code-block:: xml

    <depend>rclcpp</depend>
    <depend>std_msgs</depend>

这声明了该包在构建和执行其代码时需要 ``rclcpp`` 和 ``std_msgs``。

请确保保存文件。

2.3 CMakeLists.txt
~~~~~~~~~~~~~~~~~~

现在打开 ``CMakeLists.txt`` 文件。
在现有依赖 ``find_package(ament_cmake REQUIRED)`` 下面添加以下行：

.. code-block:: cmake

    find_package(rclcpp REQUIRED)
    find_package(std_msgs REQUIRED)

之后，添加可执行文件并将其命名为 ``talker``，这样你就可以使用 ``ros2 run`` 运行你的节点：

.. code-block:: cmake

    add_executable(talker src/publisher_lambda_function.cpp)
    ament_target_dependencies(talker rclcpp std_msgs)

最后，添加 ``install(TARGETS...)`` 部分，以便 ``ros2 run`` 可以找到你的可执行文件：

.. code-block:: cmake

  install(TARGETS
    talker
    DESTINATION lib/${PROJECT_NAME})

你可以通过删除一些不必要的部分和注释来整理你的 ``CMakeLists.txt``，使其看起来像这样：

.. code-block:: cmake

  cmake_minimum_required(VERSION 3.5)
  project(cpp_pubsub)

  # Default to C++14
  if(NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 14)
  endif()

  if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
  endif()

  find_package(ament_cmake REQUIRED)
  find_package(rclcpp REQUIRED)
  find_package(std_msgs REQUIRED)

  add_executable(talker src/publisher_lambda_function.cpp)
  ament_target_dependencies(talker rclcpp std_msgs)

  install(TARGETS
    talker
    DESTINATION lib/${PROJECT_NAME})

  ament_package()

你现在可以构建你的包，source 本地安装文件并运行它，但让我们先创建订阅者节点，这样你就可以看到完整的系统在运行。

3 编写订阅者节点
^^^^^^^^^^^^^^^^

返回到 ``ros2_ws/src/cpp_pubsub/src`` 来创建下一个节点。
在终端中输入以下代码：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

            $ wget -O subscriber_lambda_function.cpp https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_subscriber/lambda.cpp

   .. group-tab:: macOS

      .. code-block:: console

            $ wget -O subscriber_lambda_function.cpp https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_subscriber/lambda.cpp

   .. group-tab:: Windows

      在 Windows 命令行提示符中：

      .. code-block:: console

            $ curl -sk https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_subscriber/lambda.cpp -o subscriber_lambda_function.cpp

      或在 powershell 中：

      .. code-block:: console

            $ curl https://raw.githubusercontent.com/ros2/examples/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_subscriber/lambda.cpp -o subscriber_lambda_function.cpp

检查以确保这些文件存在：

.. code-block:: console

    publisher_lambda_function.cpp  subscriber_lambda_function.cpp

用文本编辑器打开 ``subscriber_lambda_function.cpp``。

.. code-block:: C++

    #include <memory>

    #include "rclcpp/rclcpp.hpp"
    #include "std_msgs/msg/string.hpp"

    class MinimalSubscriber : public rclcpp::Node
    {
    public:
      MinimalSubscriber()
      : Node("minimal_subscriber")
      {
        auto topic_callback =
          [this](std_msgs::msg::String::UniquePtr msg) -> void {
            RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
          };
        subscription_ =
          this->create_subscription<std_msgs::msg::String>("topic", 10, topic_callback);
      }

    private:
      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
    };

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<MinimalSubscriber>());
      rclcpp::shutdown();
      return 0;
    }

3.1 检查代码
~~~~~~~~~~~~

订阅者节点的代码与发布者几乎相同。
现在节点被命名为 ``minimal_subscriber``，构造函数使用节点的 ``create_subscription`` 函数来执行回调。

这里没有计时器，因为订阅者只是在有数据发布到 ``topic`` 话题时做出响应。

``topic_callback`` 函数接收通过话题发布的字符串消息数据，并使用 ``RCLCPP_INFO`` 宏将其写入控制台。

回顾 :doc:`话题教程 <../Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics>`，发布者和订阅者使用的话题名称和消息类型必须匹配，才能进行通信。

.. code-block:: C++

    public:
      MinimalSubscriber()
      : Node("minimal_subscriber")
      {
        auto topic_callback =
          [this](std_msgs::msg::String::UniquePtr msg) -> void {
            RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
          };
        subscription_ =
          this->create_subscription<std_msgs::msg::String>("topic", 10, topic_callback);
      }

这个类中唯一的字段声明是订阅。

.. code-block:: C++

    private:
      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;

``main`` 函数完全相同，只是现在它 spin 的是 ``MinimalSubscriber`` 节点。
对于发布者节点，spin 意味着启动计时器，但对于订阅者，它只意味着准备好在消息到来时接收它们。

由于这个节点与发布者节点具有相同的依赖，因此无需向 ``package.xml`` 添加新内容。

3.2 CMakeLists.txt
~~~~~~~~~~~~~~~~~~

重新打开 ``CMakeLists.txt``，在发布者的条目下面添加订阅者节点的可执行文件和目标。

.. code-block:: cmake

  add_executable(listener src/subscriber_lambda_function.cpp)
  ament_target_dependencies(listener rclcpp std_msgs)

  install(TARGETS
    talker
    listener
    DESTINATION lib/${PROJECT_NAME})

请确保保存文件，然后你的发布/订阅系统就应该准备好了。

.. _cpppubsub-build-and-run:

4 构建并运行
^^^^^^^^^^^^
你可能已经安装了 ``rclcpp`` 和 ``std_msgs`` 包作为 ROS 2 系统的一部分。
在构建之前，最好在工作空间的根目录（``ros2_ws``）运行 ``rosdep`` 来检查缺失的依赖：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

            $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

   .. group-tab:: Windows

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。


仍然在工作空间的根目录 ``ros2_ws``，构建你的新包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select cpp_pubsub

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select cpp_pubsub

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select cpp_pubsub

打开一个新终端，进入 ``ros2_ws``，然后 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在运行 talker 节点。
终端应该每 0.5 秒开始发布一次信息消息，如下所示：

.. code-block:: console

     $ ros2 run cpp_pubsub talker
     [INFO] [minimal_publisher]: Publishing: "Hello World: 0"
     [INFO] [minimal_publisher]: Publishing: "Hello World: 1"
     [INFO] [minimal_publisher]: Publishing: "Hello World: 2"
     [INFO] [minimal_publisher]: Publishing: "Hello World: 3"
     [INFO] [minimal_publisher]: Publishing: "Hello World: 4"

打开另一个终端，再次从 ``ros2_ws`` 内 source 安装文件，然后启动 listener 节点。
listener 将开始向控制台打印消息，从发布者当时的消息计数开始：

.. code-block:: console

     $ ros2 run cpp_pubsub listener
     [INFO] [minimal_subscriber]: I heard: "Hello World: 10"
     [INFO] [minimal_subscriber]: I heard: "Hello World: 11"
     [INFO] [minimal_subscriber]: I heard: "Hello World: 12"
     [INFO] [minimal_subscriber]: I heard: "Hello World: 13"
     [INFO] [minimal_subscriber]: I heard: "Hello World: 14"

在每个终端中输入 ``Ctrl+C`` 来停止节点的 spin。

总结
----

你创建了两个节点，通过话题发布和订阅数据。
在编译和运行它们之前，你将它们的依赖和可执行文件添加到了包配置文件中。

后续步骤
--------

接下来你将使用服务/客户端模型创建另一个简单的 ROS 2 包。
同样，你可以选择用 :doc:`C++ <./Writing-A-Simple-Cpp-Service-And-Client>` 或 :doc:`Python <./Writing-A-Simple-Py-Service-And-Client>` 编写它。

相关内容
--------

有多种方式可以用 C++ 编写发布者和订阅者；请查看 `ros2/examples <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclcpp/topics>`_ 仓库中的 ``minimal_publisher`` 和 ``minimal_subscriber`` 包。
