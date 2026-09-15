.. redirect-from::

    Tutorials/Content-Filtering-Subscription

创建内容过滤订阅
================

**目标：** 创建一个内容过滤订阅。

**教程级别：** 高级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 1
   :local:

概述
----

ROS 2 应用通常由话题组成，用于将数据从发布者传输到订阅。
基本上，订阅会接收话题上发布者发布的所有数据。
但有时，订阅可能只对发布者发送的数据中的一小部分感兴趣。
内容过滤订阅允许只接收应用感兴趣的数据。

在本演示中，我们将重点介绍如何创建内容过滤订阅以及它们是如何工作的。

RMW 支持
--------

内容过滤订阅需要 RMW 实现的支持。

.. list-table::  内容过滤订阅支持状态
   :widths: 25 25

   * - rmw_fastrtps
     - 支持
   * - rmw_connextdds
     - 支持
   * - rmw_cyclonedds
     - 不支持
   * - rmw_zenoh_cpp
     - 不支持

目前所有支持内容过滤订阅的 RMW 实现都是基于 `DDS <https://www.omg.org/omg-dds-portal/>`__ 的。
这意味着支持的过滤表达式和参数也依赖于 `DDS <https://www.omg.org/omg-dds-portal/>`__，你可以参考 `DDS 规范 <https://www.omg.org/spec/DDS/1.4/PDF>`__ 中的 ``Annex B - Syntax for Queries and Filters`` 获取详细信息。

安装演示
--------

有关安装 ROS 2 的详细信息，请参阅 :doc:`安装说明 <../../Installation>`。

如果你是通过软件包安装 ROS 2 的，请确保已安装 ``ros-{DISTRO}-demo-nodes-cpp``。
如果你下载了归档文件或从源代码构建了 ROS 2，它将已经是安装的一部分。

温度过滤演示
------------

本演示展示了如何使用内容过滤订阅，只接收超出可接受温度范围的温度值，从而检测紧急情况。
内容过滤订阅会过滤掉不感兴趣的温度数据，因此订阅回调不会被触发。

ContentFilteringPublisher：

https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/content_filtering_publisher.cpp

.. code-block:: c++

    #include <array>
    #include <chrono>
    #include <memory>
    #include <utility>

    #include "rclcpp/rclcpp.hpp"
    #include "rclcpp_components/register_node_macro.hpp"

    #include "std_msgs/msg/float32.hpp"

    #include "demo_nodes_cpp/visibility_control.hpp"

    namespace demo_nodes_cpp
    {
    // The simulated temperature data starts from -100.0 and ends at 150.0 with a step size of 10.0
    constexpr std::array<float, 3> TEMPERATURE_SETTING {-100.0f, 150.0f, 10.0f};

    // Create a ContentFilteringPublisher class that subclasses the generic rclcpp::Node base class.
    // The main function below will instantiate the class as a ROS node.
    class ContentFilteringPublisher final : public rclcpp::Node
    {
    public:
      DEMO_NODES_CPP_PUBLIC
      explicit ContentFilteringPublisher(const rclcpp::NodeOptions & options)
      : Node("content_filtering_publisher", options)
      {
        // Create a function for when messages are to be sent.
        auto publish_message =
          [this]() -> void
          {
            msg_ = std::make_unique<std_msgs::msg::Float32>();
            msg_->data = temperature_;
            temperature_ += TEMPERATURE_SETTING[2];
            if (temperature_ > TEMPERATURE_SETTING[1]) {
              temperature_ = TEMPERATURE_SETTING[0];
            }
            RCLCPP_INFO(this->get_logger(), "Publishing: '%f'", msg_->data);
            // Put the message into a queue to be processed by the middleware.
            // This call is non-blocking.
            pub_->publish(std::move(msg_));
          };
        // Create a publisher with a custom Quality of Service profile.
        // Uniform initialization is suggested so it can be trivially changed to
        // rclcpp::KeepAll{} if the user wishes.
        // (rclcpp::KeepLast(7) -> rclcpp::KeepAll() fails to compile)
        rclcpp::QoS qos(rclcpp::KeepLast{7});
        pub_ = this->create_publisher<std_msgs::msg::Float32>("temperature", qos);

        int64_t publish_ms = this->declare_parameter("publish_ms", 1000);

        // Use a timer to schedule periodic message publishing.
        timer_ = this->create_wall_timer(std::chrono::milliseconds(publish_ms), publish_message);
      }

    private:
      float temperature_ = TEMPERATURE_SETTING[0];
      std::unique_ptr<std_msgs::msg::Float32> msg_;
      rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr pub_;
      rclcpp::TimerBase::SharedPtr timer_;
    };

    }  // namespace demo_nodes_cpp

内容过滤器定义在订阅一侧，发布者不需要进行任何特殊配置即可支持内容过滤。
``ContentFilteringPublisher`` 节点每秒发布一次从 -100.0 开始、到 150.0 结束、步长为 10.0 的模拟温度数据。

我们可以通过运行 ``ros2 run demo_nodes_cpp content_filtering_publisher`` 可执行文件来运行演示（别忘了先 source 安装文件）：

.. code-block:: console

    $ ros2 run demo_nodes_cpp content_filtering_publisher
    [INFO] [1651094594.822753479] [content_filtering_publisher]: Publishing: '-100.000000'
    [INFO] [1651094595.822723857] [content_filtering_publisher]: Publishing: '-90.000000'
    [INFO] [1651094596.822752996] [content_filtering_publisher]: Publishing: '-80.000000'
    [INFO] [1651094597.822752475] [content_filtering_publisher]: Publishing: '-70.000000'
    [INFO] [1651094598.822721485] [content_filtering_publisher]: Publishing: '-60.000000'
    [INFO] [1651094599.822696188] [content_filtering_publisher]: Publishing: '-50.000000'
    [INFO] [1651094600.822699217] [content_filtering_publisher]: Publishing: '-40.000000'
    [INFO] [1651094601.822744113] [content_filtering_publisher]: Publishing: '-30.000000'
    [INFO] [1651094602.822694805] [content_filtering_publisher]: Publishing: '-20.000000'
    [INFO] [1651094603.822735805] [content_filtering_publisher]: Publishing: '-10.000000'
    [INFO] [1651094604.822722094] [content_filtering_publisher]: Publishing: '0.000000'
    [INFO] [1651094605.822699960] [content_filtering_publisher]: Publishing: '10.000000'
    [INFO] [1651094606.822748946] [content_filtering_publisher]: Publishing: '20.000000'
    [INFO] [1651094607.822694017] [content_filtering_publisher]: Publishing: '30.000000'
    [INFO] [1651094608.822708798] [content_filtering_publisher]: Publishing: '40.000000'
    [INFO] [1651094609.822692417] [content_filtering_publisher]: Publishing: '50.000000'
    [INFO] [1651094610.822696426] [content_filtering_publisher]: Publishing: '60.000000'
    [INFO] [1651094611.822751913] [content_filtering_publisher]: Publishing: '70.000000'
    [INFO] [1651094612.822692231] [content_filtering_publisher]: Publishing: '80.000000'
    [INFO] [1651094613.822745549] [content_filtering_publisher]: Publishing: '90.000000'
    [INFO] [1651094614.822701982] [content_filtering_publisher]: Publishing: '100.000000'
    [INFO] [1651094615.822691465] [content_filtering_publisher]: Publishing: '110.000000'
    [INFO] [1651094616.822649070] [content_filtering_publisher]: Publishing: '120.000000'
    [INFO] [1651094617.822693616] [content_filtering_publisher]: Publishing: '130.000000'
    [INFO] [1651094618.822691832] [content_filtering_publisher]: Publishing: '140.000000'
    [INFO] [1651094619.822688452] [content_filtering_publisher]: Publishing: '150.000000'
    [INFO] [1651094620.822645327] [content_filtering_publisher]: Publishing: '-100.000000'
    [INFO] [1651094621.822689219] [content_filtering_publisher]: Publishing: '-90.000000'
    [INFO] [1651094622.822694292] [content_filtering_publisher]: Publishing: '-80.000000'
    [...]

ContentFilteringSubscriber：

https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/content_filtering_subscriber.cpp

.. code-block:: c++

    #include <array>
    #include <string>

    #include "rclcpp/rclcpp.hpp"
    #include "rclcpp_components/register_node_macro.hpp"
    #include "rcpputils/join.hpp"

    #include "std_msgs/msg/float32.hpp"

    #include "demo_nodes_cpp/visibility_control.hpp"

    namespace demo_nodes_cpp
    {
    // Emergency temperature data less than -30 or greater than 100
    constexpr std::array<float, 2> EMERGENCY_TEMPERATURE {-30.0f, 100.0f};

    // Create a ContentFilteringSubscriber class that subclasses the generic rclcpp::Node base class.
    // The main function below will instantiate the class as a ROS node.
    class ContentFilteringSubscriber : public rclcpp::Node
    {
    public:
      DEMO_NODES_CPP_PUBLIC
      explicit ContentFilteringSubscriber(const rclcpp::NodeOptions & options)
      : Node("content_filtering_subscriber", options)
      {
        // Create a callback function for when messages are received.
        auto callback =
          [this](const std_msgs::msg::Float32 & msg) -> void
          {
            if (msg.data < EMERGENCY_TEMPERATURE[0] || msg.data > EMERGENCY_TEMPERATURE[1]) {
              RCLCPP_INFO(
                this->get_logger(),
                "I receive an emergency temperature data: [%f]", msg.data);
            } else {
              RCLCPP_INFO(this->get_logger(), "I receive a temperature data: [%f]", msg.data);
            }
          };

        // Initialize a subscription with a content filter to receive emergency temperature data that
        // are less than -30 or greater than 100.
        rclcpp::SubscriptionOptions sub_options;
        sub_options.content_filter_options.filter_expression = "data < %0 OR data > %1";
        sub_options.content_filter_options.expression_parameters = {
          std::to_string(EMERGENCY_TEMPERATURE[0]),
          std::to_string(EMERGENCY_TEMPERATURE[1])
        };

        sub_ = create_subscription<std_msgs::msg::Float32>("temperature", 10, callback, sub_options);

        if (!sub_->is_cft_enabled()) {
          RCLCPP_WARN(
            this->get_logger(), "Content filter is not enabled since it's not supported");
        } else {
          RCLCPP_INFO(
            this->get_logger(),
            "subscribed to topic \"%s\" with content filter options \"%s, {%s}\"",
            sub_->get_topic_name(),
            sub_options.content_filter_options.filter_expression.c_str(),
            rcpputils::join(sub_options.content_filter_options.expression_parameters, ", ").c_str());
        }
      }

    private:
      rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr sub_;
    };

    }  // namespace demo_nodes_cpp

要启用内容过滤，应用可以在 ``SubscriptionOptions`` 中设置过滤表达式和表达式参数。
应用还可以检查订阅上是否启用了内容过滤。

在本演示中，``ContentFilteringSubscriber`` 节点创建了一个内容过滤订阅，只有当温度值小于 -30.0 或大于 100.0 时才接收消息。

如前所述，内容过滤订阅的支持取决于 RMW 实现。
应用可以使用 ``is_cft_enabled`` 方法检查订阅上是否实际启用了内容过滤。

为了测试内容过滤订阅，让我们运行它：

.. code-block:: console

    $ ros2 run demo_nodes_cpp content_filtering_subscriber
    [INFO] [1651094590.682660703] [content_filtering_subscriber]: subscribed to topic "/temperature" with content filter options "data < %0 OR data > %1, {-30.000000, 100.000000}"
    [INFO] [1651094594.823805294] [content_filtering_subscriber]: I receive an emergency temperature data: [-100.000000]
    [INFO] [1651094595.823419993] [content_filtering_subscriber]: I receive an emergency temperature data: [-90.000000]
    [INFO] [1651094596.823410859] [content_filtering_subscriber]: I receive an emergency temperature data: [-80.000000]
    [INFO] [1651094597.823350377] [content_filtering_subscriber]: I receive an emergency temperature data: [-70.000000]
    [INFO] [1651094598.823282657] [content_filtering_subscriber]: I receive an emergency temperature data: [-60.000000]
    [INFO] [1651094599.823297857] [content_filtering_subscriber]: I receive an emergency temperature data: [-50.000000]
    [INFO] [1651094600.823355597] [content_filtering_subscriber]: I receive an emergency temperature data: [-40.000000]
    [INFO] [1651094615.823315377] [content_filtering_subscriber]: I receive an emergency temperature data: [110.000000]
    [INFO] [1651094616.823258458] [content_filtering_subscriber]: I receive an emergency temperature data: [120.000000]
    [INFO] [1651094617.823323525] [content_filtering_subscriber]: I receive an emergency temperature data: [130.000000]
    [INFO] [1651094618.823315527] [content_filtering_subscriber]: I receive an emergency temperature data: [140.000000]
    [INFO] [1651094619.823331424] [content_filtering_subscriber]: I receive an emergency temperature data: [150.000000]
    [INFO] [1651094620.823271748] [content_filtering_subscriber]: I receive an emergency temperature data: [-100.000000]
    [INFO] [1651094621.823343550] [content_filtering_subscriber]: I receive an emergency temperature data: [-90.000000]
    [INFO] [1651094622.823286326] [content_filtering_subscriber]: I receive an emergency temperature data: [-80.000000]
    [INFO] [1651094623.823371031] [content_filtering_subscriber]: I receive an emergency temperature data: [-70.000000]
    [INFO] [1651094624.823333112] [content_filtering_subscriber]: I receive an emergency temperature data: [-60.000000]
    [INFO] [1651094625.823266469] [content_filtering_subscriber]: I receive an emergency temperature data: [-50.000000]
    [INFO] [1651094626.823284093] [content_filtering_subscriber]: I receive an emergency temperature data: [-40.000000]

你应该会看到一条显示所用内容过滤选项的消息，以及每条消息的日志——只有当温度值小于 -30.0 或大于 100.0 时才会收到。

如果 RMW 实现不支持内容过滤，订阅仍会被创建，但不会启用内容过滤。
我们可以通过执行 ``RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ros2 run demo_nodes_cpp content_filtering_publisher`` 来尝试这一点。

.. code-block:: console

    $ RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ros2 run demo_nodes_cpp content_filtering_subscriber
    [WARN] [1651096637.893842072] [content_filtering_subscriber]: Content filter is not enabled since it is not supported
    [INFO] [1651096641.246043703] [content_filtering_subscriber]: I receive an emergency temperature data: [-100.000000]
    [INFO] [1651096642.245833527] [content_filtering_subscriber]: I receive an emergency temperature data: [-90.000000]
    [INFO] [1651096643.245743471] [content_filtering_subscriber]: I receive an emergency temperature data: [-80.000000]
    [INFO] [1651096644.245833932] [content_filtering_subscriber]: I receive an emergency temperature data: [-70.000000]
    [INFO] [1651096645.245916679] [content_filtering_subscriber]: I receive an emergency temperature data: [-60.000000]
    [INFO] [1651096646.245861895] [content_filtering_subscriber]: I receive an emergency temperature data: [-50.000000]
    [INFO] [1651096647.245946352] [content_filtering_subscriber]: I receive an emergency temperature data: [-40.000000]
    [INFO] [1651096648.245934569] [content_filtering_subscriber]: I receive a temperature data: [-30.000000]
    [INFO] [1651096649.245877906] [content_filtering_subscriber]: I receive a temperature data: [-20.000000]
    [INFO] [1651096650.245939068] [content_filtering_subscriber]: I receive a temperature data: [-10.000000]
    [INFO] [1651096651.245911450] [content_filtering_subscriber]: I receive a temperature data: [0.000000]
    [INFO] [1651096652.245879830] [content_filtering_subscriber]: I receive a temperature data: [10.000000]
    [INFO] [1651096653.245858329] [content_filtering_subscriber]: I receive a temperature data: [20.000000]
    [INFO] [1651096654.245916370] [content_filtering_subscriber]: I receive a temperature data: [30.000000]
    [INFO] [1651096655.245933741] [content_filtering_subscriber]: I receive a temperature data: [40.000000]
    [INFO] [1651096656.245833975] [content_filtering_subscriber]: I receive a temperature data: [50.000000]
    [INFO] [1651096657.245971483] [content_filtering_subscriber]: I receive a temperature data: [60.000000]

你可以看到消息 ``Content filter is not enabled``，因为底层 RMW 实现不支持该功能，但演示仍然成功创建了普通订阅来接收所有温度数据。

相关内容
--------

- `内容过滤示例 <https://github.com/ros2/examples/blob/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_subscriber/content_filtering.cpp>`__ 涵盖了内容过滤订阅的所有接口。
- `内容过滤设计 PR <https://github.com/ros2/design/pull/282>`__
