.. redirect-from::

  How-To-Guides/Disabling-ZeroCopy-loaned-messages

配置零拷贝借出消息
==================

.. contents:: 目录
   :depth: 2
   :local:

概述
----

ROS 2 借出消息与零拷贝数据共享是旨在通过尽可能减少数据复制来提升性能的机制。
使用借出消息时，RMW 中间件可以分配并管理消息内存，使发布者和订阅者能够直接共享数据缓冲区。
这降低了内存分配和数据复制带来的开销，从而实现更低的延迟和更高的吞吐量。
零拷贝数据共享在对大量数据需要高效传输的高性能应用中尤为有益。

关于借出消息的工作原理，请参阅 `Loaned Messages <https://design.ros2.org/articles/zero_copy.html>`__ 一文了解更多细节。

RMW 支持
--------

借出消息需要 RMW 实现提供支持。

.. list-table::  借出消息支持状态
   :widths: 25 25 25

   * - RMW 实现
     - 支持状态
     - 文档
   * - rmw_fastrtps
     - 支持
     - `启用零拷贝数据共享 <https://github.com/ros2/rmw_fastrtps?tab=readme-ov-file#enable-zero-copy-data-sharing>`__
   * - rmw_connextdds
     - 不支持
     - 不适用
   * - rmw_cyclonedds
     - 不支持
     - 不适用

安装演示
--------

关于安装 ROS 2 的详细信息，请参阅 :doc:`安装说明 <../../Installation>`。

如果你是通过软件包安装的 ROS 2，请确保已安装 ``ros-{DISTRO}-demo-nodes-cpp``。
如果你下载的是压缩包或是从源码构建的 ROS 2，它已经是安装内容的一部分。

使用借出消息
------------

当底层 RMW 实现支持借出消息时，发布者上的借出消息会被默认使用。
如果 RMW 实现不支持借出消息，消息将使用发布者提供的分配器实例进行分配。
`talker_loaned_message 示例 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/topics/talker_loaned_message.cpp>`__ 演示了如何创建一个使用借出消息的 ROS 2 发布者，从而在不复制消息数据的情况下高效地发布数据。

.. code-block:: c++

    #include <chrono>
    #include <cstdio>
    #include <memory>
    #include <utility>

    #include "rclcpp/rclcpp.hpp"
    #include "rclcpp_components/register_node_macro.hpp"

    #include "std_msgs/msg/float64.hpp"
    #include "std_msgs/msg/string.hpp"

    #include "demo_nodes_cpp/visibility_control.h"

    using namespace std::chrono_literals;

    namespace demo_nodes_cpp
    {
    // Create a Talker class that subclasses the generic rclcpp::Node base class.
    // The main function below will instantiate the class as a ROS node.
    class LoanedMessageTalker : public rclcpp::Node
    {
    public:
      DEMO_NODES_CPP_PUBLIC
      explicit LoanedMessageTalker(const rclcpp::NodeOptions & options)
      : Node("loaned_message_talker", options)
      {
        // Create a function for when messages are to be sent.
        setvbuf(stdout, NULL, _IONBF, BUFSIZ);

        // We differentiate in this demo between two fundamental message types - POD and non-POD
        // PODs are plain old data types, meaning all the data of its type is encapsulated within
        // the structure and does not require any heap allocation or dynamic resizing.
        // non-PODs are essentially the opposite where the data size changes during runtime.
        // All containers (including Strings) are such non-PODs.
        // Most middlewares won't be able to loan non-POD datatypes.
        // We thus feature two publishers in this demo where both, a POD and non-POD message
        // will be used to publish data.
        // The take-away for this is that the rclcpp API for message loaning can cope with
        // either POD and non-POD transparently.
        auto publish_message =
          [this]() -> void
          {
            // We loan a message here and don't allocate the memory on the stack.
            // For middlewares which support message loaning, this means the middleware
            // completely owns the memory for this message.
            // This enables a zero-copy message transport for middlewares with shared memory
            // capabilities.
            // If the middleware doesn't support this, the loaned message will be allocated
            // with the allocator instance provided by the publisher.
            auto pod_loaned_msg = pod_pub_->borrow_loaned_message();
            auto pod_msg_data = static_cast<double>(count_);
            pod_loaned_msg.get().data = pod_msg_data;
            RCLCPP_INFO(this->get_logger(), "Publishing: '%f'", pod_msg_data);
            // As the middleware might own the memory allocated for this message,
            // a call to publish explicitly transfers ownership back to the middleware.
            // The loaned message instance is thus no longer valid after a call to publish.
            pod_pub_->publish(std::move(pod_loaned_msg));

            // Similar as in the above case, we ask the middleware to loan a message.
            // As most likely the middleware won't be able to loan a message for a non-POD
            // data type, the memory for the message will be allocated on the heap within
            // the scope of the `LoanedMessage` instance.
            // After the call to `publish()`, the message will be correctly allocated.
            auto non_pod_loaned_msg = non_pod_pub_->borrow_loaned_message();
            auto non_pod_msg_data = "Hello World: " + std::to_string(count_);
            non_pod_loaned_msg.get().data = non_pod_msg_data;
            RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", non_pod_msg_data.c_str());
            non_pod_pub_->publish(std::move(non_pod_loaned_msg));
            count_++;
          };

        // Create a publisher with a custom Quality of Service profile.
        rclcpp::QoS qos(rclcpp::KeepLast(7));
        pod_pub_ = this->create_publisher<std_msgs::msg::Float64>("chatter_pod", qos);
        non_pod_pub_ = this->create_publisher<std_msgs::msg::String>("chatter", qos);

        // Use a timer to schedule periodic message publishing.
        timer_ = this->create_wall_timer(1s, publish_message);
      }

    private:
      size_t count_ = 1;
      rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pod_pub_;
      rclcpp::Publisher<std_msgs::msg::String>::SharedPtr non_pod_pub_;
      rclcpp::TimerBase::SharedPtr timer_;
    };

    }  // namespace demo_nodes_cpp

此示例通过调用 ``borrow_loaned_message()`` 尝试从 RMW 实现借出两种类型的消息。
一种是纯旧数据（POD）消息类型 ``std_msgs::msg::Float64``，另一种是非纯旧数据（POD）消息类型 ``std_msgs::msg::String``。
借出消息的要求是：对于 `rmw_fastrtps <https://github.com/ros2/rmw_fastrtps>`__ 而言，消息类型必须是纯旧数据（POD）类型，如下所示。

我们可以通过运行 ``ros2 run demo_nodes_cpp talker_loaned_message`` 可执行文件来运行该演示（别忘了先 source 安装文件）：

.. code-block:: console

    $ ros2 run demo_nodes_cpp talker_loaned_message
    [INFO] [1741063656.446278828] [loaned_message_talker]: Publishing: '1.000000'
    [INFO] [1741063656.446705580] [rclcpp]: Currently used middleware cannot loan messages. Local allocator will be used.
    [INFO] [1741063656.446754794] [loaned_message_talker]: Publishing: 'Hello World: 1'
    [INFO] [1741063657.446232119] [loaned_message_talker]: Publishing: '2.000000'
    [INFO] [1741063657.446401820] [loaned_message_talker]: Publishing: 'Hello World: 2'
    [INFO] [1741063658.446217220] [loaned_message_talker]: Publishing: '3.000000'
    [INFO] [1741063658.446383011] [loaned_message_talker]: Publishing: 'Hello World: 3'
    [...]

如果 RMW 实现不支持借出消息，所有消息都将使用发布者提供的分配器实例进行分配。
我们可以通过执行 ``RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ros2 run demo_nodes_cpp talker_loaned_message`` 来验证这一点。

.. code-block:: console

    $ RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ros2 run demo_nodes_cpp talker_loaned_message
    [INFO] [1741064109.676860153] [rclcpp]: Currently used middleware cannot loan messages. Local allocator will be used.
    [INFO] [1741064109.677043250] [loaned_message_talker]: Publishing: '1.000000'
    [INFO] [1741064109.677185724] [rclcpp]: Currently used middleware cannot loan messages. Local allocator will be used.
    [INFO] [1741064109.677224058] [loaned_message_talker]: Publishing: 'Hello World: 1'
    [INFO] [1741064110.676842111] [loaned_message_talker]: Publishing: '2.000000'
    [INFO] [1741064110.677008774] [loaned_message_talker]: Publishing: 'Hello World: 2'
    [INFO] [1741064111.676779850] [loaned_message_talker]: Publishing: '3.000000'
    [INFO] [1741064111.676937613] [loaned_message_talker]: Publishing: 'Hello World: 3'
    [...]

可以看到，两种消息都能成功发布，但由于该 RMW 实现不支持借出消息，消息是使用发布者提供的本地分配器实例进行分配的。

如何禁用借出消息
----------------

发布者
~~~~~~

默认情况下，如果底层中间件支持 *借出消息*，则 *借出消息* 会尝试从中借用内存。
可以使用 ``ROS_DISABLE_LOANED_MESSAGES`` 环境变量禁用 *借出消息*，并回退到发布者的常规行为，而无需修改任何代码或中间件配置。
你可以使用以下命令设置该环境变量：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ export ROS_DISABLE_LOANED_MESSAGES=1

      要在不同的 shell 会话之间保留此设置，可以将该命令添加到 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_DISABLE_LOANED_MESSAGES=1" >> ~/.bashrc

   .. group-tab:: macOS

      .. code-block:: console

        $ export ROS_DISABLE_LOANED_MESSAGES=1

      要在不同的 shell 会话之间保留此设置，可以将该命令添加到 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_DISABLE_LOANED_MESSAGES=1" >> ~/.bash_profile

   .. group-tab:: Windows

      .. code-block:: console

        $ set ROS_DISABLE_LOANED_MESSAGES=1

      如果你希望在不同的 shell 会话之间使其永久生效，还应运行：

      .. code-block:: console

        $ setx ROS_DISABLE_LOANED_MESSAGES 1


订阅
~~~~

目前在订阅端使用 *借出消息* 并不安全，详情请参见 `rmw issue <https://github.com/ros2/rmw_cyclonedds/issues/469>`_ 和 `rclcpp issue <https://github.com/ros2/rclcpp/issues/2401>`_。
因此，尽管底层中间件支持该功能，*借出消息* 在订阅端默认是 ``disabled`` 的，参见 `Set disable loan to on by default <https://github.com/ros2/rcl/pull/1110>`_。
要在订阅端启用 *借出消息*，你需要显式地将环境变量 ``ROS_DISABLE_LOANED_MESSAGES`` 设置为 ``0``。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ export ROS_DISABLE_LOANED_MESSAGES=0

      要在不同的 shell 会话之间保留此设置，可以将该命令添加到 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_DISABLE_LOANED_MESSAGES=0" >> ~/.bashrc

   .. group-tab:: macOS

      .. code-block:: console

        $ export ROS_DISABLE_LOANED_MESSAGES=0

      要在不同的 shell 会话之间保留此设置，可以将该命令添加到 shell 启动脚本中：

      .. code-block:: console

        $ echo "export ROS_DISABLE_LOANED_MESSAGES=0" >> ~/.bash_profile

   .. group-tab:: Windows

      .. code-block:: console

        $ set ROS_DISABLE_LOANED_MESSAGES=0

      如果你希望在不同的 shell 会话之间使其永久生效，还应运行：

      .. code-block:: console

        $ setx ROS_DISABLE_LOANED_MESSAGES 0
