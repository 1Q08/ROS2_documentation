.. redirect-from::

    Tutorials/Service-Introspection

配置服务内省
============

**目标：** 为服务客户端和服务器配置服务内省。

**教程级别：** 高级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 1
   :local:

概述
----

ROS 2 应用通常由服务组成，用于在远程节点中执行特定过程。
与任何人都可以订阅的话题不同，服务交互更加不透明。
默认情况下，你无法观察或监控服务何时被调用，也无法知道请求或响应是什么。

不过，仍然可以通过服务内省来内省服务数据通信。
为此，需要适当地配置相关服务。

在本演示中，我们将重点介绍如何为服务客户端和服务器配置服务内省状态，并用 ``ros2 service echo`` 监控服务通信。

安装演示
--------

有关安装 ROS 2 的详细信息，请参阅 :doc:`安装说明 <../../Installation>`。

如果你是通过 ROS 2 二进制软件包安装的，请确保已安装 ``ros-{DISTRO}-demo-nodes-cpp``。
如果你下载了归档文件或从源代码构建了 ROS 2，它将已经是安装的一部分。

内省配置状态
------------

服务内省有 3 种配置状态。

.. list-table::  服务内省配置状态
   :widths: 25 25

   * - RCL_SERVICE_INTROSPECTION_OFF
     - 已禁用
   * - RCL_SERVICE_INTROSPECTION_METADATA
     - 仅元数据，不含任何用户数据内容
   * - RCL_SERVICE_INTROSPECTION_CONTENTS
     - 含元数据的用户数据内容

内省演示
--------

本演示展示如何使用 ``ros2 service echo`` 管理服务内省并监控服务数据通信。

IntrospectionServiceNode:

https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/services/introspection_service.cpp

.. code-block:: c++

    namespace demo_nodes_cpp
    {

    class IntrospectionServiceNode : public rclcpp::Node
    {
    public:
      DEMO_NODES_CPP_PUBLIC
      explicit IntrospectionServiceNode(const rclcpp::NodeOptions & options)
      : Node("introspection_service", options)
      {
        auto handle_add_two_ints =
          [this](const std::shared_ptr<rmw_request_id_t> request_header,
            const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
            std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response) -> void
          {
            (void)request_header;
            RCLCPP_INFO(
              this->get_logger(), "Incoming request\na: %" PRId64 " b: %" PRId64,
              request->a, request->b);
            response->sum = request->a + request->b;
          };
        // Create a service that will use the callback function to handle requests.
        srv_ = create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", handle_add_two_ints);

        auto on_set_parameter_callback =
          [](std::vector<rclcpp::Parameter> parameters) {
            rcl_interfaces::msg::SetParametersResult result;
            result.successful = true;
            for (const rclcpp::Parameter & param : parameters) {
              if (param.get_name() != "service_configure_introspection") {
                continue;
              }

              if (param.get_type() != rclcpp::ParameterType::PARAMETER_STRING) {
                result.successful = false;
                result.reason = "must be a string";
                break;
              }

              if (param.as_string() != "disabled" && param.as_string() != "metadata" &&
                param.as_string() != "contents")
              {
                result.successful = false;
                result.reason = "must be one of 'disabled', 'metadata', or 'contents'";
                break;
              }
            }

            return result;
          };

        auto post_set_parameter_callback =
          [this](const std::vector<rclcpp::Parameter> & parameters) {
            for (const rclcpp::Parameter & param : parameters) {
              if (param.get_name() != "service_configure_introspection") {
                continue;
              }

              rcl_service_introspection_state_t introspection_state = RCL_SERVICE_INTROSPECTION_OFF;

              if (param.as_string() == "disabled") {
                introspection_state = RCL_SERVICE_INTROSPECTION_OFF;
              } else if (param.as_string() == "metadata") {
                introspection_state = RCL_SERVICE_INTROSPECTION_METADATA;
              } else if (param.as_string() == "contents") {
                introspection_state = RCL_SERVICE_INTROSPECTION_CONTENTS;
              }

              this->srv_->configure_introspection(
                this->get_clock(), rclcpp::SystemDefaultsQoS(), introspection_state);
              break;
            }
          };

        on_set_parameters_callback_handle_ = this->add_on_set_parameters_callback(
          on_set_parameter_callback);
        post_set_parameters_callback_handle_ = this->add_post_set_parameters_callback(
          post_set_parameter_callback);

        this->declare_parameter("service_configure_introspection", "disabled");
      }

    private:
      rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr srv_;
      rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr
        on_set_parameters_callback_handle_;
      rclcpp::node_interfaces::PostSetParametersCallbackHandle::SharedPtr
        post_set_parameters_callback_handle_;
    };

    }  // namespace demo_nodes_cpp

服务内省默认是禁用的，因此用户需要先启用它才能进行任何内省。
在本演示中，``IntrospectionServiceNode`` 使用一个名为 ``service_configure_introspection`` 的参数来配置服务内省状态。

首先我们需要启动 ``IntrospectionServiceNode``。

.. code-block:: console

    $ ros2 run demo_nodes_cpp introspection_service

要更改服务内省状态，我们需要如下设置 ``configure_introspection`` 参数。

将其更改为含元数据的用户数据内容：

.. code-block:: console

    $ ros2 param set /introspection_service service_configure_introspection contents

将其更改为仅元数据：

.. code-block:: console

    $ ros2 param set /introspection_service service_configure_introspection metadata

禁用：

.. code-block:: console

    $ ros2 param set /introspection_service service_configure_introspection disabled

IntrospectionClientNode:

https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/services/introspection_client.cpp

.. code-block:: c++

    namespace demo_nodes_cpp
    {
    class IntrospectionClientNode : public rclcpp::Node
    {
    public:
      DEMO_NODES_CPP_PUBLIC
      explicit IntrospectionClientNode(const rclcpp::NodeOptions & options)
      : Node("introspection_client", options)
      {
        client_ = create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");

        auto on_set_parameter_callback =
          [](std::vector<rclcpp::Parameter> parameters) {
            rcl_interfaces::msg::SetParametersResult result;
            result.successful = true;
            for (const rclcpp::Parameter & param : parameters) {
              if (param.get_name() != "client_configure_introspection") {
                continue;
              }

              if (param.get_type() != rclcpp::ParameterType::PARAMETER_STRING) {
                result.successful = false;
                result.reason = "must be a string";
                break;
              }

              if (param.as_string() != "disabled" && param.as_string() != "metadata" &&
                param.as_string() != "contents")
              {
                result.successful = false;
                result.reason = "must be one of 'disabled', 'metadata', or 'contents'";
                break;
              }
            }

            return result;
          };

        auto post_set_parameter_callback =
          [this](const std::vector<rclcpp::Parameter> & parameters) {
            for (const rclcpp::Parameter & param : parameters) {
              if (param.get_name() != "client_configure_introspection") {
                continue;
              }

              rcl_service_introspection_state_t introspection_state = RCL_SERVICE_INTROSPECTION_OFF;

              if (param.as_string() == "disabled") {
                introspection_state = RCL_SERVICE_INTROSPECTION_OFF;
              } else if (param.as_string() == "metadata") {
                introspection_state = RCL_SERVICE_INTROSPECTION_METADATA;
              } else if (param.as_string() == "contents") {
                introspection_state = RCL_SERVICE_INTROSPECTION_CONTENTS;
              }

              this->client_->configure_introspection(
                this->get_clock(), rclcpp::SystemDefaultsQoS(), introspection_state);
              break;
            }
          };

        on_set_parameters_callback_handle_ = this->add_on_set_parameters_callback(
          on_set_parameter_callback);
        post_set_parameters_callback_handle_ = this->add_post_set_parameters_callback(
          post_set_parameter_callback);

        this->declare_parameter("client_configure_introspection", "disabled");

        timer_ = this->create_wall_timer(
          std::chrono::milliseconds(500),
          [this]() {
            if (!client_->service_is_ready()) {
              return;
            }

            if (!request_in_progress_) {
              auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
              request->a = 2;
              request->b = 3;
              request_in_progress_ = true;
              client_->async_send_request(
                request,
                [this](rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture cb_f)
                {
                  request_in_progress_ = false;
                  RCLCPP_INFO(get_logger(), "Result of add_two_ints: %ld", cb_f.get()->sum);
                }
              );
              return;
            }
          });
      }

    private:
      rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
      rclcpp::TimerBase::SharedPtr timer_;
      rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr
        on_set_parameters_callback_handle_;
      rclcpp::node_interfaces::PostSetParametersCallbackHandle::SharedPtr
        post_set_parameters_callback_handle_;
      bool request_in_progress_{false};
    };

    }  // namespace demo_nodes_cpp

然后，我们以同样的方式启动并配置 ``IntrospectionClientNode``，它将周期性地向服务器发起服务调用。

.. code-block:: console

    $ ros2 run demo_nodes_cpp introspection_client

按如下方式更改服务内省状态，设置 ``configure_introspection`` 参数。

将其更改为含元数据的用户数据内容：

.. code-block:: console

    $ ros2 param set /introspection_client client_configure_introspection contents

将其更改为仅元数据：

.. code-block:: console

    $ ros2 param set /introspection_client client_configure_introspection metadata

禁用：

.. code-block:: console

    $ ros2 param set /introspection_client client_configure_introspection disabled

现在服务服务器和客户端都已配置好，我们可以使用 ``ros2 service echo`` 来监控客户端与服务器之间发生的交互。

在本教程中，以下是 ``IntrospectionServiceNode`` 上服务内省状态为 ``CONTENTS``、``IntrospectionClientNode`` 上为 ``METADATA`` 时的示例输出。

.. code-block:: console

    $ ros2 service echo --flow-style /add_two_ints
    info:
      event_type: REQUEST_SENT
      stamp:
        sec: 1709432402
        nanosec: 680094264
      client_gid: [1, 15, 0, 18, 86, 208, 115, 86, 0, 0, 0, 0, 0, 0, 21, 3]
      sequence_number: 247
    request: []
    response: []
    ---
    info:
      event_type: REQUEST_RECEIVED
      stamp:
        sec: 1709432402
        nanosec: 680459568
      client_gid: [1, 15, 0, 18, 86, 208, 115, 86, 0, 0, 0, 0, 0, 0, 20, 4]
      sequence_number: 247
    request: [{a: 2, b: 3}]
    response: []
    ---
    info:
      event_type: RESPONSE_SENT
      stamp:
        sec: 1709432402
        nanosec: 680765280
      client_gid: [1, 15, 0, 18, 86, 208, 115, 86, 0, 0, 0, 0, 0, 0, 20, 4]
      sequence_number: 247
    request: []
    response: [{sum: 5}]
    ---
    info:
      event_type: RESPONSE_RECEIVED
      stamp:
        sec: 1709432402
        nanosec: 681027998
      client_gid: [1, 15, 0, 18, 86, 208, 115, 86, 0, 0, 0, 0, 0, 0, 21, 3]
      sequence_number: 247
    request: []
    response: []
    ---
    ...

你可以看到 ``event_type: REQUEST_SENT`` 和 ``event_type: RESPONSE_RECEIVED``，这些内省服务事件发生在 ``IntrospectionClientNode`` 中。
由于 ``IntrospectionClientNode`` 的服务内省状态被设置为 ``METADATA``，这些事件的 ``request`` 和 ``response`` 字段不包含任何内容。
另一方面，来自 ``IntrospectionServiceNode`` 的 ``event_type: REQUEST_RECEIVED`` 和 ``event_type: RESPONSE_SENT`` 事件包含 ``request: [{a: 2, b: 3}]`` 和 ``response: [{sum: 5}]``，因为其内省状态被设置为 ``CONTENTS``。

相关内容
--------

- `服务内省客户端示例（rclcpp） <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/services/introspection_client.cpp>`__ 和 `服务内省服务端示例（rclcpp） <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/services/introspection_service.cpp>`__。
- `服务内省客户端和服务端示例（rclpy） <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_py/demo_nodes_py/services/introspection.py>`__。
- `服务内省 REP-2012 <https://github.com/ros-infrastructure/rep/pull/360>`__。
