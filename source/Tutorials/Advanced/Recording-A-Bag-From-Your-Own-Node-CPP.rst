.. redirect-from::

    Tutorials/Ros2bag/Recording-A-Bag-From-Your-Own-Node-Cpp

.. _ROS2BagOwnNode:

从节点录制 bag（C++）
=====================

**目标：** 将你自己 C++ 节点的数据录制到 bag 中。

**教程级别：** 高级

**预计用时：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``rosbag2`` 不仅仅提供 ``ros2 bag`` 命令行工具。
它还提供了一个 C++ API，用于从你自己的源代码中读取和写入 bag。
这允许你订阅一个主题，并在对该数据执行任何其他处理的同时，将接收到的数据保存到 bag 中。

前置条件
--------

你应该已经在常规的 ROS 2 安装中安装了 ``rosbag2`` 包。

如果你是在 Linux 上通过 deb 包安装的，它可能已默认安装。
如果没有，你可以使用以下命令安装它。

.. code-block:: console

  $ sudo apt install ros-{DISTRO}-rosbag2

本教程讨论如何使用 ROS 2 bag，包括从终端使用。
你应该已经完成了 :doc:`基础的 ROS 2 bag 教程 <../Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data>`。

任务
----

1 创建包
^^^^^^^^

打开一个新终端，并 :doc:`source 你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，使 ``ros2`` 命令能够正常工作。

导航到在 :ref:`上一教程 <new-directory>` 中创建的 ``ros2_ws`` 目录。
导航到 ``ros2_ws/src`` 目录，并创建一个新包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 bag_recorder_nodes --dependencies example_interfaces rclcpp rosbag2_cpp std_msgs

你的终端将返回一条消息，确认包 ``bag_recorder_nodes`` 及其所有必要文件和文件夹已创建。
``--dependencies`` 参数会自动将必要的依赖行添加到 ``package.xml`` 和 ``CMakeLists.txt``。
在这种情况下，该包将使用 ``rosbag2_cpp`` 包和 ``rclcpp`` 包。
对于本教程后面的部分，还需要依赖 ``example_interfaces`` 包。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

由于你在创建包时使用了 ``--dependencies`` 选项，因此无需手动向 ``package.xml`` 或 ``CMakeLists.txt`` 添加依赖。
不过，和往常一样，请确保向 ``package.xml`` 添加描述、维护者邮箱和姓名以及许可证信息。

.. code-block:: xml

  <description>C++ bag writing tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

2 编写 C++ 节点
^^^^^^^^^^^^^^^

在 ``ros2_ws/src/bag_recorder_nodes/src`` 目录中，创建一个名为 ``simple_bag_recorder.cpp`` 的新文件，并将以下代码粘贴进去。

.. code-block:: C++


    #include <rclcpp/rclcpp.hpp>
    #include <std_msgs/msg/string.hpp>

    #include <rosbag2_cpp/writer.hpp>

    class SimpleBagRecorder : public rclcpp::Node
    {
    public:
      SimpleBagRecorder()
      : Node("simple_bag_recorder")
      {
        writer_ = std::make_unique<rosbag2_cpp::Writer>();

        writer_->open("my_bag");

        auto subscription_callback_lambda = [this](std::shared_ptr<const rclcpp::SerializedMessage> msg){
          rclcpp::Time time_stamp = this->now();

          writer_->write(msg, "chatter", "std_msgs/msg/String", time_stamp);
        };

        subscription_ = create_subscription<std_msgs::msg::String>(
          "chatter", 10, subscription_callback_lambda);
      }

    private:

      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
      std::unique_ptr<rosbag2_cpp::Writer> writer_;
    };

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<SimpleBagRecorder>());
      rclcpp::shutdown();
      return 0;
    }

2.1 分析代码
~~~~~~~~~~~~

顶部的 ``#include`` 语句是包依赖。
注意包含了来自 ``rosbag2_cpp`` 包的头文件，这些头文件提供了处理 bag 文件所需的函数和结构。

在类构造函数中，我们首先创建将用于写入 bag 的 writer 对象。

.. code-block:: C++

        writer_ = std::make_unique<rosbag2_cpp::Writer>();

现在我们有了一个 writer 对象，可以用它打开 bag。
我们只指定要创建的 bag 的 URI，其他选项保持默认值。
使用默认的存储选项，这意味着将创建一个 ``mcap`` 格式的 bag。
也使用默认的转换选项，这将不执行任何转换，而是以接收到的序列化格式存储消息。

.. code-block:: C++

        writer_->open("my_bag");

现在 writer 已设置为录制我们传给它的数据，我们创建一个订阅并为其指定一个回调。
我们将在回调中将数据写入 bag。

.. code-block:: C++

        auto subscription_callback_lambda = [this](std::shared_ptr<const rclcpp::SerializedMessage> msg){
          rclcpp::Time time_stamp = this->now();

          writer_->write(msg, "chatter", "std_msgs/msg/String", time_stamp);
        };

        subscription_ = create_subscription<std_msgs::msg::String>(
          "chatter", 10, subscription_callback_lambda);

回调本身与典型的回调不同。
我们不是接收主题数据类型的实例，而是接收一个 ``rclcpp::SerializedMessage``。
这样做有两个原因。

1. 消息数据在写入 bag 之前需要由 ``rosbag2`` 序列化，因此与其在接收数据时反序列化再重新序列化，我们不如让 ROS 直接给我们原样的序列化消息。
2. writer API 可以接受序列化的消息。

.. code-block:: C++

        auto subscription_callback_lambda = [this](std::shared_ptr<const rclcpp::SerializedMessage> msg){

在订阅回调中，首先要做的是确定要用于所存储消息的时间戳。
这可以是任何适合你数据的值，但两个常见的值是数据产生的时间（如果已知）和接收数据的时间。
这里使用第二个选项，即接收时间。

.. code-block:: C++

        rclcpp::Time time_stamp = this->now();

然后我们可以将消息写入 bag。
因为我们还没有向 bag 注册任何主题，所以必须随消息一起指定完整的主题信息。
这就是为什么我们要传入主题名和主题类型。

.. code-block:: C++

        writer_->write(msg, "chatter", "std_msgs/msg/String", time_stamp);

该类包含两个成员变量。

1. 订阅对象。
2. 一个指向用于写入 bag 的 writer 对象的受管理指针。
   请注意，这里使用的 writer 类型是 ``rosbag2_cpp::Writer``，即通用 writer 接口。
   可能还有其他具有不同行为的 writer。

.. code-block:: C++

      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
      std::unique_ptr<rosbag2_cpp::Writer> writer_;

文件以 ``main`` 函数结束，该函数用于创建节点的实例并启动 ROS 对其进行处理。

.. code-block:: C++

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<SimpleBagRecorder>());
      rclcpp::shutdown();
      return 0;
    }

2.2 添加可执行文件
~~~~~~~~~~~~~~~~~~

现在打开 ``CMakeLists.txt`` 文件。

在文件顶部附近，将 ``CMAKE_CXX_STANDARD`` 从 ``14`` 改为 ``17``。

.. code-block:: cmake

    # Default to C++17
    if(NOT CMAKE_CXX_STANDARD)
      set(CMAKE_CXX_STANDARD 17)
    endif()

在包含 ``find_package(rosbag2_cpp REQUIRED)`` 的依赖块下面，添加以下代码行。

.. code-block:: cmake

    add_executable(simple_bag_recorder src/simple_bag_recorder.cpp)
    ament_target_dependencies(simple_bag_recorder rclcpp rosbag2_cpp std_msgs)

    install(TARGETS
      simple_bag_recorder
      DESTINATION lib/${PROJECT_NAME}
    )

3 构建并运行
^^^^^^^^^^^^

导航回工作空间的根目录 ``ros2_ws``，并构建你的新包。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select bag_recorder_nodes

打开一个新终端，导航到 ``ros2_ws``，并 source 安装文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在运行该节点：

.. code-block:: console

    $ ros2 run bag_recorder_nodes simple_bag_recorder

打开第二个终端，运行 ``talker`` 示例节点。

.. code-block:: console

    $ ros2 run demo_nodes_cpp talker

这将开始在 ``chatter`` 主题上发布数据。
当 bag 写入节点接收到这些数据时，它会将数据写入 ``my_bag`` bag。

终止两个节点。
然后，在一个终端中启动 ``listener`` 示例节点。

.. code-block:: console

    $ ros2 run demo_nodes_cpp listener

在另一个终端中，使用 ``ros2 bag`` 播放你的节点录制的 bag。

.. code-block:: console

    $ ros2 bag play my_bag

你将看到来自 bag 的消息被 ``listener`` 节点接收。

如果你想再次运行 bag 写入节点，你需要先删除 ``my_bag`` 目录。

4 从节点录制合成数据
^^^^^^^^^^^^^^^^^^^^

任何数据都可以录制到 bag 中，而不仅仅是通过主题接收到的数据。
从自己的节点写入 bag 的一个常见用例是生成并存储合成数据。
在本节中，你将学习如何编写一个节点，生成一些数据并将其存储在 bag 中。
我们将演示两种实现方法。
第一种使用带定时器的节点；如果你的数据生成在节点外部（例如直接从硬件读取数据，如相机），你可以使用这种方法。
第二种方法不使用节点；当你不需要使用 ROS 基础设施的任何功能时，可以使用这种方法。

4.1 编写 C++ 节点
~~~~~~~~~~~~~~~~~

在 ``ros2_ws/src/bag_recorder_nodes/src`` 目录中，创建一个名为 ``data_generator_node.cpp`` 的新文件，并将以下代码粘贴进去。

.. code-block:: C++

    #include <chrono>

    #include <example_interfaces/msg/int32.hpp>
    #include <rclcpp/rclcpp.hpp>

    #include <rosbag2_cpp/writer.hpp>

    using namespace std::chrono_literals;

    class DataGenerator : public rclcpp::Node
    {
    public:
      DataGenerator()
      : Node("data_generator")
      {
        data_.data = 0;
        writer_ = std::make_unique<rosbag2_cpp::Writer>();

        writer_->open("timed_synthetic_bag");

        writer_->create_topic(
        {
          0u,
          "synthetic",
          "example_interfaces/msg/Int32",
          rmw_get_serialization_format(),
          {},
          "",
        });

        auto timer_callback_lambda = [this](){return this->timer_callback();};
        timer_ = create_wall_timer(1s, timer_callback_lambda);
      }

    private:
      void timer_callback()
      {
        writer_->write(data_, "synthetic", now());

        ++data_.data;
      }

      rclcpp::TimerBase::SharedPtr timer_;
      std::unique_ptr<rosbag2_cpp::Writer> writer_;
      example_interfaces::msg::Int32 data_;
    };

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<DataGenerator>());
      rclcpp::shutdown();
      return 0;
    }

4.2 分析代码
~~~~~~~~~~~~

这段代码的大部分与第一个示例相同。
重要的差异在此处描述。

首先，bag 的名称被更改。

.. code-block:: C++

        writer_->open("timed_synthetic_bag");

在这个示例中，我们提前向 bag 注册了主题。
在大多数情况下这是可选的，但在传入不带主题信息的序列化消息时必须这样做。

.. code-block:: C++

        writer_->create_topic(
        {
          0u,
          "synthetic",
          "example_interfaces/msg/Int32",
          rmw_get_serialization_format(),
          {},
          "",
        });

这个节点没有订阅主题，而是有一个定时器。
定时器以一秒为周期触发，并在触发时调用给定的成员函数。

.. code-block:: C++

        auto timer_callback_lambda = [this](){return this->timer_callback();};
        timer_ = create_wall_timer(1s, timer_callback_lambda);

在定时器回调中，我们生成（或以其他方式获取，例如从连接到某些硬件的串口读取）我们希望存储在 bag 中的数据。
这与上一个示例的重要区别在于数据尚未序列化。
相反，我们向 writer 对象传递一个 ROS 消息数据类型，在本例中是 ``example_interfaces/msg/Int32`` 的实例。
writer 会在将数据写入 bag 之前为我们序列化数据。

.. code-block:: C++

        writer_->write(data_, "synthetic", now());

4.3 添加可执行文件
~~~~~~~~~~~~~~~~~~

打开 ``CMakeLists.txt`` 文件，在之前添加的行之后（具体来说，在 ``install(TARGETS ...)`` 宏调用之后）添加以下行。

.. code-block:: cmake

    add_executable(data_generator_node src/data_generator_node.cpp)
    ament_target_dependencies(data_generator_node rclcpp rosbag2_cpp example_interfaces)

    install(TARGETS
      data_generator_node
      DESTINATION lib/${PROJECT_NAME}
    )

4.4 构建并运行
~~~~~~~~~~~~~~

导航回工作空间的根目录 ``ros2_ws``，并构建你的包。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select bag_recorder_nodes

打开一个新终端，导航到 ``ros2_ws``，并 source 安装文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

（如果 ``timed_synthetic_bag`` 目录已经存在，你必须先删除它，然后再运行节点。）

现在运行该节点：

.. code-block:: console

    $ ros2 run bag_recorder_nodes data_generator_node

等待大约 30 秒，然后用 :kbd:`ctrl-c` 终止节点。
接下来，播放创建的 bag。

.. code-block:: console

    $ ros2 bag play timed_synthetic_bag

打开第二个终端，回显 ``/synthetic`` 主题。

.. code-block:: console

    $ ros2 topic echo /synthetic

你将看到生成并存储在 bag 中的数据以每秒一条消息的速率打印到控制台。

5 从可执行文件录制合成数据
^^^^^^^^^^^^^^^^^^^^^^^^^^

既然你可以创建一个 bag 来存储来自主题之外的数据源的数据，你将学习如何从一个非节点可执行文件生成和录制合成数据。
这种方法的优点是代码更简单，并且可以快速创建大量数据。

5.1 编写 C++ 可执行文件
~~~~~~~~~~~~~~~~~~~~~~~

在 ``ros2_ws/src/bag_recorder_nodes/src`` 目录中，创建一个名为 ``data_generator_executable.cpp`` 的新文件，并将以下代码粘贴进去。

.. code-block:: C++

    #include <chrono>

    #include <rclcpp/rclcpp.hpp>  // For rclcpp::Clock, rclcpp::Duration and rclcpp::Time
    #include <example_interfaces/msg/int32.hpp>

    #include <rosbag2_cpp/writer.hpp>
    #include <rosbag2_cpp/writers/sequential_writer.hpp>
    #include <rosbag2_storage/serialized_bag_message.hpp>

    using namespace std::chrono_literals;

    int main(int, char**)
    {
      example_interfaces::msg::Int32 data;
      data.data = 0;
      std::unique_ptr<rosbag2_cpp::Writer> writer_ = std::make_unique<rosbag2_cpp::Writer>();

      writer_->open("big_synthetic_bag");

      writer_->create_topic(
      {
        0u,
        "synthetic",
        "example_interfaces/msg/Int32",
        rmw_get_serialization_format(),
        {},
        "",
      });

      rclcpp::Clock clock;
      rclcpp::Time time_stamp = clock.now();
      for (int32_t ii = 0; ii < 100; ++ii) {
        writer_->write(data, "synthetic", time_stamp);
        ++data.data;
        time_stamp += rclcpp::Duration(1s);
      }

      return 0;
    }

5.2 分析代码
~~~~~~~~~~~~

将本示例与上一个示例进行比较就会发现，它们并没有太大区别。
唯一显著的差异是使用 for 循环而不是定时器来驱动数据生成。

请注意，我们现在还为数据生成时间戳，而不是为每个样本依赖当前系统时间。
时间戳可以是你需要的任何值。
数据将以这些时间戳给出的速率播放，因此这是控制样本默认播放速度的有用方法。
还要注意，虽然每个样本之间的间隔在时间上是完整的一秒，但这个可执行文件不需要在每个样本之间等待一秒。
这使我们能够在比播放所需时间短得多的时间内，生成覆盖大范围时间的大量数据。

.. code-block:: C++

      rclcpp::Clock clock;
      rclcpp::Time time_stamp = clock.now();
      for (int32_t ii = 0; ii < 100; ++ii) {
        writer_->write(data, "synthetic", time_stamp);
        ++data.data;
        time_stamp += rclcpp::Duration(1s);
      }

5.3 添加可执行文件
~~~~~~~~~~~~~~~~~~

打开 ``CMakeLists.txt`` 文件，在之前添加的行之后添加以下行。

.. code-block:: cmake

    add_executable(data_generator_executable src/data_generator_executable.cpp)
    ament_target_dependencies(data_generator_executable rclcpp rosbag2_cpp example_interfaces)

    install(TARGETS
      data_generator_executable
      DESTINATION lib/${PROJECT_NAME}
    )

5.4 构建并运行
~~~~~~~~~~~~~~

导航回工作空间的根目录 ``ros2_ws``，并构建你的包。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select bag_recorder_nodes

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select bag_recorder_nodes

打开一个终端，导航到 ``ros2_ws``，并 source 安装文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

（如果 ``big_synthetic_bag`` 目录已经存在，你必须先删除它，然后再运行可执行文件。）

现在运行该可执行文件：

.. code-block:: console

    $ ros2 run bag_recorder_nodes data_generator_executable

请注意，该可执行文件运行并非常快速地完成。

现在播放创建的 bag。

.. code-block:: console

    $ ros2 bag play big_synthetic_bag

打开第二个终端，回显 ``/synthetic`` 主题。

.. code-block:: console

    $ ros2 topic echo /synthetic

你将看到生成并存储在 bag 中的数据以每秒一条消息的速率打印到控制台。
即使 bag 是快速生成的，它仍然以时间戳指示的速率播放。

总结
----

你创建了一个节点，将它在主题上接收到的数据录制到 bag 中。
你测试了使用该节点录制 bag，并通过播放 bag 验证了数据已被录制。
然后，你继续创建了一个节点和一个可执行文件来生成合成数据并将其存储在 bag 中。
