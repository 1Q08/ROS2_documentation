.. redirect-from::

    FastDDS-Configuration
    Tutorials/FastDDS-Configuration/FastDDS-Configuration

释放 Fast DDS 中间件的潜力 [社区贡献]
=====================================

**目标：** 本教程将展示如何在 ROS 2 中使用 Fast DDS 的扩展配置能力。

**教程级别：** 高级

**预计用时：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

ROS 2 栈与 *Fast DDS* 之间的接口由 ROS 2 中间件实现 `rmw_fastrtps <https://github.com/ros2/rmw_fastrtps>`_ 提供。
这个实现在所有 ROS 2 发行版中都可使用，无论是二进制形式还是源码形式。

ROS 2 RMW 只允许配置某些中间件 QoS
（参见 :doc:`ROS 2 QoS 策略 <../../Concepts/Intermediate/About-Quality-of-Service-Settings>`）。
然而，``rmw_fastrtps`` 提供了扩展的配置能力，以充分利用 *Fast DDS* 中的特性。
本教程将通过一系列示例，解释如何使用 XML 文件来释放这些扩展配置。

要获取更多关于在 ROS 2 上使用 *Fast DDS* 的信息，请查看 `以下文档 <https://fast-dds.docs.eprosima.com/en/latest/fastdds/ros2/ros2.html>`__。


前置条件
--------

本教程假设你知道如何 :doc:`创建一个包 <../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>`。
它还假设你知道如何编写一个 :doc:`简单的发布者和订阅者<../Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber>` 以及一个 :doc:`简单的服务和客户端 <../Beginner-Client-Libraries/Writing-A-Simple-Cpp-Service-And-Client>`。
虽然示例是用 C++ 实现的，但相同的概念也适用于 Python 包。


在同一节点中混合同步和异步发布
------------------------------

在第一个示例中，将创建一个包含两个发布者的节点，其中一个使用同步发布模式，另一个使用异步发布模式。

``rmw_fastrtps`` 默认使用同步发布模式。

在同步发布模式下，数据直接在用户线程的上下文中发送。
这意味着写入操作期间发生的任何阻塞调用都会阻塞用户线程，从而阻止应用程序继续其操作。
然而，这种模式通常能以较低的延迟获得更高的吞吐量，因为线程之间没有通知，也没有上下文切换。

另一方面，在异步发布模式下，每次发布者调用写入操作时，数据都会被复制到队列中，
一个后台线程（异步线程）会收到关于队列新增的通知，并且在实际发送数据之前，线程的控制权就返回给了用户。
后台线程负责消费队列并将数据发送给每一个匹配的读取者。

创建带有发布者的节点
^^^^^^^^^^^^^^^^^^^^

首先，在新工作空间中创建一个名为 ``sync_async_node_example_cpp`` 的新包：

.. tabs::

    .. group-tab:: Linux

       .. code-block:: console

         $ mkdir -p ~/ros2_ws/src
         $ cd ~/ros2_ws/src
         $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 --dependencies rclcpp std_msgs -- sync_async_node_example_cpp

    .. group-tab:: macOS

      .. code-block:: console

        $ mkdir -p ~/ros2_ws/src
        $ cd ~/ros2_ws/src
        $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 --dependencies rclcpp std_msgs -- sync_async_node_example_cpp

    .. group-tab:: Windows

      .. code-block:: console

        $ md \ros2_ws\src
        $ cd \ros2_ws\src
        $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 --dependencies rclcpp std_msgs -- sync_async_node_example_cpp


然后，向包中添加一个名为 ``src/sync_async_writer.cpp`` 的文件，内容如下。
请注意，同步发布者将在主题 ``sync_topic`` 上发布，而异步发布者将在主题 ``async_topic`` 上发布。

.. code-block:: C++

    #include <chrono>
    #include <functional>
    #include <memory>
    #include <string>

    #include "rclcpp/rclcpp.hpp"
    #include "std_msgs/msg/string.hpp"

    using namespace std::chrono_literals;

    class SyncAsyncPublisher : public rclcpp::Node
    {
    public:
        SyncAsyncPublisher()
            : Node("sync_async_publisher"), count_(0)
        {
            // Create the synchronous publisher on topic 'sync_topic'
            sync_publisher_ = this->create_publisher<std_msgs::msg::String>("sync_topic", 10);

            // Create the asynchronous publisher on topic 'async_topic'
            async_publisher_ = this->create_publisher<std_msgs::msg::String>("async_topic", 10);

            // Actions to run every time the timer expires
            auto timer_callback = [this](){

                // Create a new message to be sent
                auto sync_message = std_msgs::msg::String();
                sync_message.data = "SYNC: Hello, world! " + std::to_string(count_);

                // Log the message to the console to show progress
                RCLCPP_INFO(this->get_logger(), "Synchronously publishing: '%s'", sync_message.data.c_str());

                // Publish the message using the synchronous publisher
                sync_publisher_->publish(sync_message);

                // Create a new message to be sent
                auto async_message = std_msgs::msg::String();
                async_message.data = "ASYNC: Hello, world! " + std::to_string(count_);

                // Log the message to the console to show progress
                RCLCPP_INFO(this->get_logger(), "Asynchronously publishing: '%s'", async_message.data.c_str());

                // Publish the message using the asynchronous publisher
                async_publisher_->publish(async_message);

                // Prepare the count for the next message
                count_++;
            };

            // This timer will trigger the publication of new data every half a second
            timer_ = this->create_wall_timer(500ms, timer_callback);
        }

    private:
        // This timer will trigger the publication of new data every half a second
        rclcpp::TimerBase::SharedPtr timer_;

        // A publisher that publishes asynchronously
        rclcpp::Publisher<std_msgs::msg::String>::SharedPtr async_publisher_;

        // A publisher that publishes synchronously
        rclcpp::Publisher<std_msgs::msg::String>::SharedPtr sync_publisher_;

        // Number of messages sent so far
        size_t count_;
    };

    int main(int argc, char * argv[])
    {
        rclcpp::init(argc, argv);
        rclcpp::spin(std::make_shared<SyncAsyncPublisher>());
        rclcpp::shutdown();
        return 0;
    }

现在打开 ``CMakeLists.txt`` 文件，添加一个新可执行文件并将其命名为 ``SyncAsyncWriter``，这样你就可以使用 ``ros2 run`` 运行你的节点：

.. code-block:: cmake

    add_executable(SyncAsyncWriter src/sync_async_writer.cpp)
    ament_target_dependencies(SyncAsyncWriter rclcpp std_msgs)

最后，添加 ``install(TARGETS…)`` 部分，以便 ``ros2 run`` 可以找到你的可执行文件：

.. code-block:: cmake

    install(TARGETS
        SyncAsyncWriter
        DESTINATION lib/${PROJECT_NAME})

你可以通过删除一些不必要的部分和注释来清理你的 ``CMakeLists.txt``，使它看起来像这样：

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.8)
    project(sync_async_node_example_cpp)

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

    add_executable(SyncAsyncWriter src/sync_async_writer.cpp)
    ament_target_dependencies(SyncAsyncWriter rclcpp std_msgs)

    install(TARGETS
        SyncAsyncWriter
        DESTINATION lib/${PROJECT_NAME})

    ament_package()

如果现在构建并运行这个节点，两个发布者的行为将相同，在两个主题上都会异步发布，因为这是默认的发布模式。
默认发布模式配置可以在节点启动过程中通过 XML 文件在运行时更改。

创建包含配置文件配置的 XML 文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建一个名为 ``SyncAsync.xml`` 的文件，内容如下：

.. code-block:: XML

    <?xml version="1.0" encoding="UTF-8" ?>
    <profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">

        <!-- default publisher profile -->
        <publisher profile_name="default_publisher" is_default_profile="true">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
        </publisher>

        <!-- default subscriber profile -->
        <subscriber profile_name="default_subscriber" is_default_profile="true">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
        </subscriber>

        <!-- publisher profile for topic sync_topic -->
        <publisher profile_name="/sync_topic">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
            <qos>
                <publishMode>
                    <kind>SYNCHRONOUS</kind>
                </publishMode>
            </qos>
        </publisher>

        <!-- publisher profile for topic async_topic -->
        <publisher profile_name="/async_topic">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
            <qos>
                <publishMode>
                    <kind>ASYNCHRONOUS</kind>
                </publishMode>
            </qos>
        </publisher>

     </profiles>

请注意，这里为发布者和订阅者定义了多个配置文件。
有两个默认配置文件，它们通过将 ``is_default_profile`` 设置为 ``true`` 来定义；还有两个名称与之前定义的主题名称相同的配置文件：``sync_topic`` 和另一个用于 ``async_topic`` 的配置文件。
后两个配置文件分别将发布模式设置为 ``SYNCHRONOUS`` 或 ``ASYNCHRONOUS``。
还要注意，所有配置文件都指定了一个 ``historyMemoryPolicy`` 值，这是示例运行所必需的，原因将在本教程稍后解释。

运行发布者节点
^^^^^^^^^^^^^^

你需要导出以下环境变量，才能加载 XML：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ export RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ export FASTRTPS_DEFAULT_PROFILES_FILE=path/to/SyncAsync.xml

  .. group-tab:: macOS

    .. code-block:: console

      $ export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ export RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ export FASTRTPS_DEFAULT_PROFILES_FILE=path/to/SyncAsync.xml

  .. group-tab:: Windows

    .. code-block:: console

      $ SET RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ SET RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ SET FASTRTPS_DEFAULT_PROFILES_FILE=path/to/SyncAsync.xml

最后，确保你已经 source 了 setup 文件，然后运行节点：

.. code-block:: console

    $ source install/setup.bash
    $ ros2 run sync_async_node_example_cpp SyncAsyncWriter
    [INFO] [1612972049.994630332] [sync_async_publisher]: Synchronously publishing: 'SYNC: Hello, world! 0'
    [INFO] [1612972049.995097767] [sync_async_publisher]: Asynchronously publishing: 'ASYNC: Hello, world! 0'
    [INFO] [1612972050.494478706] [sync_async_publisher]: Synchronously publishing: 'SYNC: Hello, world! 1'
    [INFO] [1612972050.494664334] [sync_async_publisher]: Asynchronously publishing: 'ASYNC: Hello, world! 1'
    [INFO] [1612972050.994368474] [sync_async_publisher]: Synchronously publishing: 'SYNC: Hello, world! 2'
    [INFO] [1612972050.994549851] [sync_async_publisher]: Asynchronously publishing: 'ASYNC: Hello, world! 2'

现在，你有了一个同步发布者和一个异步发布者运行在同一个节点内。


创建带有订阅者的节点
^^^^^^^^^^^^^^^^^^^^

接下来，将创建一个包含订阅者的新节点，这些订阅者将监听 ``sync_topic`` 和 ``async_topic`` 的发布。
在一个名为 ``src/sync_async_reader.cpp`` 的新源文件中写入以下内容：

.. code-block:: C++

    #include <memory>

    #include "rclcpp/rclcpp.hpp"
    #include "std_msgs/msg/string.hpp"

    class SyncAsyncSubscriber : public rclcpp::Node
    {
    public:

        SyncAsyncSubscriber()
            : Node("sync_async_subscriber")
        {
            // Lambda function to run every time a new message is received
            auto topic_callback = [this](const std_msgs::msg::String & msg){
                RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
            };

            // Create the synchronous subscriber on topic 'sync_topic'
            // and tie it to the topic_callback
            sync_subscription_ = this->create_subscription<std_msgs::msg::String>(
                "sync_topic", 10, topic_callback);

            // Create the asynchronous subscriber on topic 'async_topic'
            // and tie it to the topic_callback
            async_subscription_ = this->create_subscription<std_msgs::msg::String>(
                "async_topic", 10, topic_callback);
        }

    private:

        // A subscriber that listens to topic 'sync_topic'
        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sync_subscription_;

        // A subscriber that listens to topic 'async_topic'
        rclcpp::Subscription<std_msgs::msg::String>::SharedPtr async_subscription_;
    };

    int main(int argc, char * argv[])
    {
        rclcpp::init(argc, argv);
        rclcpp::spin(std::make_shared<SyncAsyncSubscriber>());
        rclcpp::shutdown();
        return 0;
    }


打开 ``CMakeLists.txt`` 文件，在上一个 ``SyncAsyncWriter`` 下面添加一个新可执行文件并将其命名为 ``SyncAsyncReader``：

.. code-block:: cmake

    add_executable(SyncAsyncReader src/sync_async_reader.cpp)
    ament_target_dependencies(SyncAsyncReader rclcpp std_msgs)

    install(TARGETS
        SyncAsyncReader
        DESTINATION lib/${PROJECT_NAME})


运行订阅者节点
^^^^^^^^^^^^^^

在发布者节点在一个终端运行的情况下，打开另一个终端并导出加载 XML 所需的环境变量：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ export RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ export FASTRTPS_DEFAULT_PROFILES_FILE=path/to/SyncAsync.xml

  .. group-tab:: macOS

    .. code-block:: console

      $ export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ export RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ export FASTRTPS_DEFAULT_PROFILES_FILE=path/to/SyncAsync.xml

  .. group-tab:: Windows

    .. code-block:: console

      $ SET RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ SET RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ SET FASTRTPS_DEFAULT_PROFILES_FILE=path/to/SyncAsync.xml

最后，确保你已经 source 了 setup 文件，然后运行节点：

.. code-block:: console

    $ source install/setup.bash
    $ ros2 run sync_async_node_example_cpp SyncAsyncReader
    [INFO] [1612972054.495429090] [sync_async_subscriber]: I heard: 'SYNC: Hello, world! 10'
    [INFO] [1612972054.995410057] [sync_async_subscriber]: I heard: 'ASYNC: Hello, world! 10'
    [INFO] [1612972055.495453494] [sync_async_subscriber]: I heard: 'SYNC: Hello, world! 11'
    [INFO] [1612972055.995396561] [sync_async_subscriber]: I heard: 'ASYNC: Hello, world! 11'
    [INFO] [1612972056.495534818] [sync_async_subscriber]: I heard: 'SYNC: Hello, world! 12'
    [INFO] [1612972056.995473953] [sync_async_subscriber]: I heard: 'ASYNC: Hello, world! 12'


示例分析
^^^^^^^^

配置文件 XML
~~~~~~~~~~~~

该 XML 文件为发布者和订阅者定义了多个配置。
你可以有一个默认的发布者配置文件以及多个主题特定的发布者配置文件。
唯一的要求是所有发布者配置文件都有不同的名称，并且只有一个默认配置文件。
订阅者也是如此。

为了给特定主题定义配置，只需将配置文件命名为 ROS 2 主题名（例如示例中的 ``/sync_topic`` 和 ``/async_topic``），
``rmw_fastrtps`` 就会将该配置文件应用到该主题的所有发布者和订阅者。
默认配置文件由设置为 ``true`` 的属性 ``is_default_profile`` 标识，并且在没有其他名称与主题名匹配的配置文件时充当回退配置文件。

环境变量 ``FASTRTPS_DEFAULT_PROFILES_FILE`` 用于告知 *Fast DDS* 要加载的包含配置文件的 XML 文件的路径。

RMW_FASTRTPS_USE_QOS_FROM_XML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

在所有可配置属性中，``rmw_fastrtps`` 对 ``publishMode`` 和 ``historyMemoryPolicy`` 的处理方式不同。
默认情况下，在 ``rmw_fastrtps`` 实现中，这些值被设置为 ``ASYNCHRONOUS`` 和 ``PREALLOCATED_WITH_REALLOC``，而 XML 文件中设置的值会被忽略。
为了使用 XML 文件中的值，必须将环境变量 ``RMW_FASTRTPS_USE_QOS_FROM_XML`` 设置为 ``1``。

然而，这带来了\ **另一个注意事项**：如果设置了 ``RMW_FASTRTPS_USE_QOS_FROM_XML``，但 XML 文件没有定义
``publishMode`` 或 ``historyMemoryPolicy``，这些属性将采用 *Fast DDS* 的默认值，而不是 ``rmw_fastrtps`` 的默认值。
这一点很重要，尤其是对于 ``historyMemoryPolicy``，因为 *Fast DDS* 的默认值是 ``PREALLOCATED``，它不适用于 ROS2 主题数据类型。
因此，在示例中，已经为这个策略显式设置了一个有效值（``DYNAMIC``）。


rmw_qos_profile_t 的优先级
~~~~~~~~~~~~~~~~~~~~~~~~~~

包含在 `rmw_qos_profile_t <http://docs.ros.org/en/{DISTRO}/p/rmw/generated/structrmw__qos__profile__s.html>`_ 中的 ROS 2 QoS 始终会被遵守，除非设置为 ``*_SYSTEM_DEFAULT``。
在这种情况下，将应用 XML 值（在没有 XML 值的情况下则为 *Fast DDS* 默认值）。
这意味着，如果 ``rmw_qos_profile_t`` 中的任何 QoS 被设置为除 ``*_SYSTEM_DEFAULT`` 以外的值，XML 中对应的值将被忽略。


通过 XML 使用其他 FastDDS 能力
------------------------------

虽然我们已经创建了一个具有两个不同配置发布者的节点，但要检查它们的行为是否不同并不容易。
现在已经介绍了 XML 配置文件的基础知识，让我们用它们来配置一些对节点有视觉效果的东西。
具体来说，将在一个发布者上设置匹配订阅者的最大数量，并在另一个发布者上设置分区定义。
请注意，这些只是可以通过 XML 文件在 ``rmw_fastrtps`` 上调整的所有配置属性中的一些非常简单的示例。
请参阅 `*Fast DDS* 文档 <https://fast-dds.docs.eprosima.com/en/latest/fastdds/xml_configuration/xml_configuration.html#xml-profiles>`__，查看可以通过 XML 文件配置的属性的完整列表。

限制匹配订阅者的数量
^^^^^^^^^^^^^^^^^^^^

向 ``/async_topic`` 发布者配置文件添加匹配订阅者的最大数量。
它应该看起来像这样：

.. code-block:: XML

    <!-- publisher profile for topic async_topic -->
    <publisher profile_name="/async_topic">
        <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
        <qos>
            <publishMode>
                <kind>ASYNCHRONOUS</kind>
            </publishMode>
        </qos>
        <matchedSubscribersAllocation>
            <initial>0</initial>
            <maximum>1</maximum>
            <increment>1</increment>
        </matchedSubscribersAllocation>
    </publisher>

匹配订阅者的数量被限制为一个。

现在打开三个终端，不要忘记 source setup 文件并设置所需的环境变量。
在第一个终端运行发布者节点，在其他两个终端运行订阅者节点。
你应该看到只有第一个订阅者节点收到来自两个主题的消息。
第二个订阅者无法完成 ``/async_topic`` 的匹配过程，因为发布者阻止了它，因为发布者已经达到了匹配发布者的最大数量。
因此，在第三个终端中只会收到来自 ``/sync_topic`` 的消息：

.. code-block:: console

    [INFO] [1613127657.088860890] [sync_async_subscriber]: I heard: 'SYNC: Hello, world! 18'
    [INFO] [1613127657.588896594] [sync_async_subscriber]: I heard: 'SYNC: Hello, world! 19'
    [INFO] [1613127658.088849401] [sync_async_subscriber]: I heard: 'SYNC: Hello, world! 20'


在主题中使用分区
^^^^^^^^^^^^^^^^

分区特性可以用于控制哪些发布者和订阅者在同一主题内交换信息。

分区在由域 ID 引起的物理隔离内部引入了逻辑实体隔离级别的概念。
发布者要与订阅者通信，它们必须至少属于一个共同的分区。
分区代表了在域和主题之外，用于分离发布者和订阅者的另一个层级。
与域和主题不同，一个端点可以同时属于多个分区。
要在不同域或主题之间共享某些数据，每个域或主题都必须有不同的发布者，各自共享自己的变更历史。
然而，一个发布者可以使用单个主题数据变更在不同分区之间共享同一个数据样本，从而减少网络开销。

让我们将 ``/sync_topic`` 发布者改到分区 ``part1``，并创建一个使用分区 ``part2`` 的新 ``/sync_topic`` 订阅者。
它们的配置文件现在应该看起来像这样：

.. code-block:: XML

    <!-- publisher profile for topic sync_topic -->
    <publisher profile_name="/sync_topic">
        <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
        <qos>
            <publishMode>
                <kind>SYNCHRONOUS</kind>
            </publishMode>
            <partition>
                <names>
                    <name>part1</name>
                </names>
            </partition>
        </qos>
    </publisher>

    <!-- subscriber profile for topic sync_topic -->
    <subscriber profile_name="/sync_topic">
        <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
        <qos>
            <partition>
                <names>
                    <name>part2</name>
                </names>
            </partition>
        </qos>
    </subscriber>

打开两个终端。
不要忘记 source setup 文件并设置所需的环境变量。
在第一个终端运行发布者节点，在另一个终端运行订阅者节点。
你应该看到只有 ``/async_topic`` 消息到达订阅者。
``/sync_topic`` 订阅者没有接收到数据，因为它与相应的发布者处于不同的分区。

.. code-block:: console

    [INFO] [1612972054.995410057] [sync_async_subscriber]: I heard: 'ASYNC: Hello, world! 10'
    [INFO] [1612972055.995396561] [sync_async_subscriber]: I heard: 'ASYNC: Hello, world! 11'
    [INFO] [1612972056.995473953] [sync_async_subscriber]: I heard: 'ASYNC: Hello, world! 12'


配置服务和客户端
----------------

服务和客户端各有一个发布者和一个订阅者，它们通过两个不同的主题进行通信。
例如，对于一个名为 ``ping`` 的服务，存在：

* 一个服务订阅者，监听 ``/rq/ping`` 上的请求。
* 一个服务发布者，在 ``/rr/ping`` 上发送响应。
* 一个客户端发布者，在 ``/rq/ping`` 上发送请求。
* 一个客户端订阅者，监听 ``/rr/ping`` 上的响应。

虽然你可以使用这些主题名在 XML 上设置配置文件，但有时你可能希望将同一个配置文件应用到节点上的所有服务或客户端。
与其为所有服务生成的所有主题名复制同一个配置文件，不如创建一个名为 ``service`` 的发布者和订阅者配置文件对。
对于客户端也可以这样做，创建一个名为 ``client`` 的对。


创建带有服务和客户端的节点
^^^^^^^^^^^^^^^^^^^^^^^^^^

首先创建带有服务的节点。
在你的包中添加一个名为 ``src/ping_service.cpp`` 的新源文件，内容如下：

.. code-block:: C++

    #include <memory>

    #include "rclcpp/rclcpp.hpp"
    #include "example_interfaces/srv/trigger.hpp"

    /**
     * Service action: responds with success=true and prints the request on the console
     */
    void ping(const std::shared_ptr<example_interfaces::srv::Trigger::Request> request,
            std::shared_ptr<example_interfaces::srv::Trigger::Response> response)
    {
        // The request data is unused
        (void) request;

        // Build the response
        response->success = true;

        // Log to the console
        RCLCPP_INFO(rclcpp::get_logger("ping_server"), "Incoming request");
        RCLCPP_INFO(rclcpp::get_logger("ping_server"), "Sending back response");
    }

    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);

        // Create the node and the service
        std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("ping_server");
        rclcpp::Service<example_interfaces::srv::Trigger>::SharedPtr service =
            node->create_service<example_interfaces::srv::Trigger>("ping", &ping);

        // Log that the service is ready
        RCLCPP_INFO(rclcpp::get_logger("ping_server"), "Ready to serve.");

        // run the node
        rclcpp::spin(node);
        rclcpp::shutdown();
    }

在一个名为 ``src/ping_client.cpp`` 的文件中创建客户端，内容如下：

.. code-block:: C++

    #include <chrono>
    #include <memory>

    #include "rclcpp/rclcpp.hpp"
    #include "example_interfaces/srv/trigger.hpp"

    using namespace std::chrono_literals;

    int main(int argc, char **argv)
    {
        rclcpp::init(argc, argv);

        // Create the node and the client
        std::shared_ptr<rclcpp::Node> node = rclcpp::Node::make_shared("ping_client");
        rclcpp::Client<example_interfaces::srv::Trigger>::SharedPtr client =
            node->create_client<example_interfaces::srv::Trigger>("ping");

        // Create a request
        auto request = std::make_shared<example_interfaces::srv::Trigger::Request>();

        // Wait for the service to be available
        while (!client->wait_for_service(1s)) {
            if (!rclcpp::ok()) {
                RCLCPP_ERROR(rclcpp::get_logger("ping_client"), "Interrupted while waiting for the service. Exiting.");
                return 0;
            }
            RCLCPP_INFO(rclcpp::get_logger("ping_client"), "Service not available, waiting again...");
        }

        // Now that the service is available, send the request
        RCLCPP_INFO(rclcpp::get_logger("ping_client"), "Sending request");
        auto result = client->async_send_request(request);

        // Wait for the result and log it to the console
        if (rclcpp::spin_until_future_complete(node, result) ==
            rclcpp::FutureReturnCode::SUCCESS)
        {
            RCLCPP_INFO(rclcpp::get_logger("ping_client"), "Response received");
        } else {
            RCLCPP_ERROR(rclcpp::get_logger("ping_client"), "Failed to call service ping");
        }

        rclcpp::shutdown();
        return 0;
    }

打开 ``CMakeLists.txt`` 文件，添加两个新的可执行文件 ``ping_service`` 和 ``ping_client``：

.. code-block:: cmake

    find_package(example_interfaces REQUIRED)

    add_executable(ping_service src/ping_service.cpp)
    ament_target_dependencies(ping_service example_interfaces rclcpp)

    add_executable(ping_client src/ping_client.cpp)
    ament_target_dependencies(ping_client example_interfaces rclcpp)

    install(TARGETS
        ping_service
        DESTINATION lib/${PROJECT_NAME})

    install(TARGETS
        ping_client
        DESTINATION lib/${PROJECT_NAME})

最后，构建该包。


为服务和客户端创建 XML 配置文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建一个名为 ``ping.xml`` 的文件，内容如下：

.. code-block:: XML

    <?xml version="1.0" encoding="UTF-8" ?>
    <profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">

        <!-- default publisher profile -->
        <publisher profile_name="default_publisher" is_default_profile="true">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
        </publisher>

        <!-- default subscriber profile -->
        <subscriber profile_name="default_subscriber" is_default_profile="true">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
        </subscriber>

        <!-- service publisher is SYNC -->
        <publisher profile_name="service">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
            <qos>
                <publishMode>
                    <kind>SYNCHRONOUS</kind>
                </publishMode>
            </qos>
        </publisher>

        <!-- client publisher is ASYNC -->
        <publisher profile_name="client">
            <historyMemoryPolicy>DYNAMIC</historyMemoryPolicy>
            <qos>
                <publishMode>
                    <kind>ASYNCHRONOUS</kind>
                </publishMode>
            </qos>
        </publisher>

    </profiles>


此配置文件将服务的发布模式设置为 ``SYNCHRONOUS``，将客户端的发布模式设置为 ``ASYNCHRONOUS``。
请注意，我们只为服务和客户端定义了发布者配置文件，但也可以提供订阅者配置文件。


运行节点
^^^^^^^^

打开两个终端，并在每个终端上 source setup 文件。
然后设置加载 XML 所需的环境变量：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ export RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ export FASTRTPS_DEFAULT_PROFILES_FILE=path/to/ping.xml

  .. group-tab:: macOS

    .. code-block:: console

      $ export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ export RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ export FASTRTPS_DEFAULT_PROFILES_FILE=path/to/ping.xml

  .. group-tab:: Windows

    .. code-block:: console

      $ SET RMW_IMPLEMENTATION=rmw_fastrtps_cpp
      $ SET RMW_FASTRTPS_USE_QOS_FROM_XML=1
      $ SET FASTRTPS_DEFAULT_PROFILES_FILE=path/to/ping.xml


在第一个终端运行服务节点。
你应该看到服务在等待请求：

.. code-block:: console

    $ ros2 run sync_async_node_example_cpp ping_service
    [INFO] [1612977403.805799037] [ping_server]: Ready to serve.

在第二个终端运行客户端节点。
你应该看到客户端发送请求并接收响应：


.. code-block:: console

    $ ros2 run sync_async_node_example_cpp ping_client
    [INFO] [1612977404.805799037] [ping_client]: Sending request
    [INFO] [1612977404.825473835] [ping_client]: Response received

与此同时，服务器控制台中的输出已经更新：

.. code-block:: console

    [INFO] [1612977403.805799037] [ping_server]: Ready to serve.
    [INFO] [1612977404.807314904] [ping_server]: Incoming request
    [INFO] [1612977404.836405125] [ping_server]: Sending back response
