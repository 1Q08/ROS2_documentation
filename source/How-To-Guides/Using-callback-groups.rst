使用回调组
==========

在多线程执行器中运行节点时，ROS 2 提供了回调组这一工具，
用于控制不同回调的执行。
本页旨在作为如何高效使用回调组的指南。
假定读者对 :doc:`执行器 <../Concepts/Intermediate/About-Executors>` 的概念有基本了解。

.. contents:: 目录
   :local:

回调组基础
----------

在多线程执行器中运行节点时，
ROS 2 提供了两种不同类型的回调组，用于控制
回调的执行：

* 互斥回调组
* 可重入回调组

这两类回调组以不同的方式限制其回调的执行。
简而言之：

* 互斥回调组会阻止其回调并行执行——实际上
  相当于该组中的回调由 SingleThreadedExecutor 执行。
* 可重入回调组允许执行器以它认为合适的任何方式
  调度和执行该组的回调，不受限制。
  这意味着，除了不同的回调可以彼此并行运行之外，
  同一个回调的不同实例也可以并发执行。
* 属于不同回调组（任意类型）的回调始终可以
  彼此并行执行。

同样重要的是要记住，不同的 ROS 2 实体会把它们的回调组
传递给它们创建的所有回调。
例如，如果为某个动作客户端指定了回调组，
那么该客户端创建的所有回调都会被分配到该回调组。

回调组可以通过节点在 rclcpp 中的 ``create_callback_group``
函数创建，也可以在 rclpy 中通过调用该组的构造函数创建。
随后，在创建订阅、定时器等时，可以把回调组作为参数/选项传入。
应当保留对回调组的引用，否则与该回调组关联的回调
将不会被执行器调用。

.. tabs::

  .. group-tab:: C++

    .. code-block:: cpp

      my_callback_group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

      rclcpp::SubscriptionOptions options;
      options.callback_group = my_callback_group;

      my_subscription = create_subscription<Int32>("/topic", rclcpp::SensorDataQoS(),
                                                    callback, options);

  .. group-tab:: Python

    .. code-block:: python

      my_callback_group = MutuallyExclusiveCallbackGroup()
      my_subscription = self.create_subscription(Int32, "/topic", self.callback, qos_profile=1,
                                                  callback_group=my_callback_group)

如果用户在创建订阅、定时器等时未指定任何回调组，
该实体将被分配到节点的默认回调组。
默认回调组是一个互斥回调组，可以通过 rclcpp 中的
``NodeBaseInterface::get_default_callback_group()`` 查询，
也可以通过 rclpy 中的 ``Node.default_callback_group`` 查询。

关于回调
^^^^^^^^

在 ROS 2 和执行器的语境中，回调是指其调度和执行
由执行器处理的函数。
在此语境下，回调的例子有

* 订阅回调（接收并处理来自话题的数据），
* 定时器回调，
* 服务回调（在服务端执行服务请求），
* 动作服务端和客户端中的各种回调，
* Futures 的完成回调。

下面是关于回调的几个要点，在使用回调组时
应当牢记。

* ROS 2 中几乎一切都是回调！
  按照定义，由执行器运行的每个函数都是回调。
  ROS 2 系统中的非回调函数主要出现在
  系统的边缘（用户输入和传感器输入等）。
* 有时回调是隐藏的，从用户/开发者 API 上可能
  看不出它们的存在。
  对于以任何形式“同步”调用服务或动作
  （在 rclpy 中）的情况尤其如此。
  例如，对服务的同步调用 ``Client.call(request)``
  会添加一个 Future 完成回调，它需要在该函数调用
  执行期间被执行，但这个回调对用户
  并非直接可见。


控制执行
--------

为了用回调组控制执行，可以考虑
以下准则。

关于单个回调与自身的交互：

* 如果它需要与自身并行执行，就把它注册到可重入回调组。
  一个例子是需要能够彼此并行处理
  多个动作调用的动作/服务服务端。

* 如果它 **绝不** 应与自身并行执行，就把它注册到互斥回调组。
  一个例子是运行控制循环并发布控制命令的定时器回调。

关于不同回调之间的交互：

* 如果它们 **绝不** 应并行执行，就把它们注册到同一个互斥回调组。
  一个例子是这些回调正在访问共享的关键且非线程安全的资源。

如果它们应当并行执行，你有两种选择，
取决于单个回调是否需要能够与自身重叠：

* 把它们注册到不同的互斥回调组（单个回调之间不重叠）

* 把它们注册到一个可重入回调组（单个回调之间可以重叠）

让不同回调并行运行的一个例子是这样一个节点：
它有一个同步服务客户端和一个调用该服务的定时器。
详见下面的示例。

避免死锁
--------

不正确地为节点设置回调组可能导致死锁（或
其他不期望的行为），尤其是在希望同步调用
服务或动作的情况下。
事实上，就连 ROS 2 的 API 文档也提到，
不应当在回调中同步调用动作或服务，
因为这可能导致死锁。
虽然在这一点上使用异步调用确实更安全，但同步
调用也可以做到正确工作。
另一方面，同步调用也有其优点，例如
让代码更简单、更易理解。
因此，本节提供一些关于如何正确设置节点
回调组以避免死锁的准则。

这里首先要注意的是，每个节点的默认回调组都是
一个互斥回调组。
如果用户在创建定时器、订阅、客户端等时未指定任何其他回调组，
那么这些实体当时或之后创建的任何回调
都将使用节点的默认回调组。
此外，如果节点中的所有内容都使用同一个互斥
回调组，那么该节点实际上就相当于由
单线程执行器处理，即使指定了多线程执行器也是如此！
因此，只要决定使用多线程执行器，
就总应当指定一些回调组，这样
执行器的选择才有意义。

考虑到以上内容，下面给出几条有助于避免死锁的准则：

* 如果在任何类型的回调中进行同步调用，那么该回调
  与发起调用的客户端必须属于

  * 不同的回调组（任意类型），或
  * 一个可重入回调组。

* 如果由于其他要求而无法采用上述配置——例如
  线程安全和/或在等待结果时阻塞其他回调
  （或者如果你想要绝对确保永远
  不存在死锁的可能），请使用异步调用。

不满足第一点总会导致死锁。
这种情况的一个例子是在定时器回调中进行同步服务调用
（参见下一节的示例）。


示例
----

让我们看几个不同回调组设置的简单示例。
下面的演示代码考虑在定时器回调中
同步调用服务。

演示代码
^^^^^^^^

我们有两个节点——一个提供简单的服务：

.. tabs::

   .. group-tab:: C++

      .. code-block:: cpp

        #include <memory>
        #include "rclcpp/rclcpp.hpp"
        #include "std_srvs/srv/empty.hpp"

        using namespace std::placeholders;

        namespace cb_group_demo
        {
        class ServiceNode : public rclcpp::Node
        {
        public:
            ServiceNode() : Node("service_node")
            {
                service_ptr_ = this->create_service<std_srvs::srv::Empty>(
                        "test_service",
                        std::bind(&ServiceNode::service_callback, this, _1, _2, _3)
                );
            }

        private:
            rclcpp::Service<std_srvs::srv::Empty>::SharedPtr service_ptr_;

            void service_callback(
                    const std::shared_ptr<rmw_request_id_t> request_header,
                    const std::shared_ptr<std_srvs::srv::Empty::Request> request,
                    const std::shared_ptr<std_srvs::srv::Empty::Response> response)
            {
                (void)request_header;
                (void)request;
                (void)response;
                RCLCPP_INFO(this->get_logger(), "Received request, responding...");
            }
        };  // class ServiceNode
        }   // namespace cb_group_demo

        int main(int argc, char* argv[])
        {
            rclcpp::init(argc, argv);
            auto service_node = std::make_shared<cb_group_demo::ServiceNode>();

            RCLCPP_INFO(service_node->get_logger(), "Starting server node, shut down with CTRL-C");
            rclcpp::spin(service_node);
            RCLCPP_INFO(service_node->get_logger(), "Keyboard interrupt, shutting down.\n");

            rclcpp::shutdown();
            return 0;
        }

   .. group-tab:: Python

      .. code-block:: python

        import rclpy
        from rclpy.node import Node
        from std_srvs.srv import Empty

        class ServiceNode(Node):
            def __init__(self):
                super().__init__('service_node')
                self.srv = self.create_service(Empty, 'test_service', callback=self.service_callback)

            def service_callback(self, request, result):
                self.get_logger().info('Received request, responding...')
                return result


        if __name__ == '__main__':
            rclpy.init()
            node = ServiceNode()
            try:
                node.get_logger().info("Starting server node, shut down with CTRL-C")
                rclpy.spin(node)
            except KeyboardInterrupt:
                node.get_logger().info('Keyboard interrupt, shutting down.\n')
            node.destroy_node()
            rclpy.shutdown()

另一个包含该服务的客户端，以及一个用于发起
服务调用的定时器：

.. tabs::

  .. group-tab:: C++

    *注意：* rclcpp 中服务客户端的 API 并不提供
    与 rclpy 中类似的同步调用方法，因此我们
    在 future 对象上等待，以模拟同步调用的
    效果。

    .. code-block:: cpp

      #include <chrono>
      #include <memory>
      #include "rclcpp/rclcpp.hpp"
      #include "std_srvs/srv/empty.hpp"

      using namespace std::chrono_literals;

      namespace cb_group_demo
      {
      class DemoNode : public rclcpp::Node
      {
      public:
          DemoNode() : Node("client_node")
          {
              client_cb_group_ = nullptr;
              timer_cb_group_ = nullptr;
              client_ptr_ = this->create_client<std_srvs::srv::Empty>("test_service", rmw_qos_profile_services_default,
                                                                      client_cb_group_);
              timer_ptr_ = this->create_wall_timer(1s, std::bind(&DemoNode::timer_callback, this),
                                                  timer_cb_group_);
          }

      private:
          rclcpp::CallbackGroup::SharedPtr client_cb_group_;
          rclcpp::CallbackGroup::SharedPtr timer_cb_group_;
          rclcpp::Client<std_srvs::srv::Empty>::SharedPtr client_ptr_;
          rclcpp::TimerBase::SharedPtr timer_ptr_;

          void timer_callback()
          {
              RCLCPP_INFO(this->get_logger(), "Sending request");
              auto request = std::make_shared<std_srvs::srv::Empty::Request>();
              auto result_future = client_ptr_->async_send_request(request);
              std::future_status status = result_future.wait_for(10s);  // timeout to guarantee a graceful finish
              if (status == std::future_status::ready) {
                  RCLCPP_INFO(this->get_logger(), "Received response");
              }
          }
      };  // class DemoNode
      }   // namespace cb_group_demo

      int main(int argc, char* argv[])
      {
          rclcpp::init(argc, argv);
          auto client_node = std::make_shared<cb_group_demo::DemoNode>();
          rclcpp::executors::MultiThreadedExecutor executor;
          executor.add_node(client_node);

          RCLCPP_INFO(client_node->get_logger(), "Starting client node, shut down with CTRL-C");
          executor.spin();
          RCLCPP_INFO(client_node->get_logger(), "Keyboard interrupt, shutting down.\n");

          rclcpp::shutdown();
          return 0;
      }

  .. group-tab:: Python

    .. code-block:: python

      import rclpy
      from rclpy.executors import MultiThreadedExecutor
      from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
      from rclpy.node import Node
      from std_srvs.srv import Empty


      class CallbackGroupDemo(Node):
          def __init__(self):
              super().__init__('client_node')

              client_cb_group = None
              timer_cb_group = None
              self.client = self.create_client(Empty, 'test_service', callback_group=client_cb_group)
              self.call_timer = self.create_timer(1, self._timer_cb, callback_group=timer_cb_group)

          def _timer_cb(self):
              self.get_logger().info('Sending request')
              _ = self.client.call(Empty.Request())
              self.get_logger().info('Received response')


      if __name__ == '__main__':
          rclpy.init()
          node = CallbackGroupDemo()
          executor = MultiThreadedExecutor()
          executor.add_node(node)

          try:
              node.get_logger().info('Beginning client, shut down with CTRL-C')
              executor.spin()
          except KeyboardInterrupt:
              node.get_logger().info('Keyboard interrupt, shutting down.\n')
          node.destroy_node()
          rclpy.shutdown()

客户端节点的构造函数包含用于设置
服务客户端和定时器回调组的选项。
使用上面的默认设置（两者都是 ``nullptr`` / ``None``）时，
定时器和客户端都将使用节点的默认
互斥回调组。

问题
^^^^

由于我们使用 1 秒的定时器发起服务调用，预期的
结果是服务每秒被调用一次，
客户端总能得到响应并打印 ``Received response``。
如果在终端中运行服务端和客户端节点，
我们会得到如下输出。

.. tabs::

  .. group-tab:: Client

    .. code-block:: console

      [INFO] [1653034371.758739131] [client_node]: Starting client node, shut down with CTRL-C
      [INFO] [1653034372.755865649] [client_node]: Sending request
      ^C[INFO] [1653034398.161674869] [client_node]: Keyboard interrupt, shutting down.

  .. group-tab:: Server

    .. code-block:: console

      [INFO] [1653034355.308958238] [service_node]: Starting server node, shut down with CTRL-C
      [INFO] [1653034372.758197320] [service_node]: Received request, responding...
      ^C[INFO] [1653034416.021962246] [service_node]: Keyboard interrupt, shutting down.

因此，结果是服务并没有被反复调用，
第一次调用的响应始终没有收到，之后
客户端节点似乎卡住了，不再发起后续调用。
也就是说，执行停在了死锁处！

原因在于定时器回调和客户端使用了
同一个互斥回调组（节点的默认回调组）。
发起服务调用时，客户端会把它的回调组
传给 Future 对象（在 Python 版本中隐藏在
call 方法内部），而必须执行该对象的完成回调，
服务调用的结果才可用。
但由于这个完成回调和定时器回调处于
同一个互斥组中，而定时器回调仍在
执行（正在等待服务调用的结果），
所以完成回调永远无法执行。
被卡住的定时器回调还会阻塞它自身的其他执行，因此
定时器不会第二次触发。

解决方案
^^^^^^^^

我们可以轻松解决这个问题——例如——
把定时器和客户端分配到不同的回调组。
因此，让我们把客户端节点构造函数的前两行
修改如下（其他内容保持不变）：

.. tabs::

  .. group-tab:: C++

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
      timer_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

  .. group-tab:: Python

    .. code-block:: python

      client_cb_group = MutuallyExclusiveCallbackGroup()
      timer_cb_group = MutuallyExclusiveCallbackGroup()

现在我们得到了预期的结果，即定时器反复触发，
每次服务调用都能如期拿到结果：

.. tabs::

  .. group-tab:: Client

    .. code-block:: console

      [INFO] [1653067523.431731177] [client_node]: Starting client node, shut down with CTRL-C
      [INFO] [1653067524.431912821] [client_node]: Sending request
      [INFO] [1653067524.433230445] [client_node]: Received response
      [INFO] [1653067525.431869330] [client_node]: Sending request
      [INFO] [1653067525.432912803] [client_node]: Received response
      [INFO] [1653067526.431844726] [client_node]: Sending request
      [INFO] [1653067526.432893954] [client_node]: Received response
      [INFO] [1653067527.431828287] [client_node]: Sending request
      [INFO] [1653067527.432848369] [client_node]: Received response
      ^C[INFO] [1653067528.400052749] [client_node]: Keyboard interrupt, shutting down.

  .. group-tab:: Server

    .. code-block:: console

      [INFO] [1653067522.052866001] [service_node]: Starting server node, shut down with CTRL-C
      [INFO] [1653067524.432577720] [service_node]: Received request, responding...
      [INFO] [1653067525.432365009] [service_node]: Received request, responding...
      [INFO] [1653067526.432300261] [service_node]: Received request, responding...
      [INFO] [1653067527.432272441] [service_node]: Received request, responding...
      ^C[INFO] [1653034416.021962246] [service_node]: KeyboardInterrupt, shutting down.

有人可能会想，仅仅避开节点的默认回调组
是否就够了。
事实并非如此：用一个不同的互斥组替换默认组
并不会改变任何情况。
因此，下面的配置也会导致前面
发现的死锁。

.. tabs::

  .. group-tab:: C++

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
      timer_cb_group_ = client_cb_group_;

  .. group-tab:: Python

    .. code-block:: python

      client_cb_group = MutuallyExclusiveCallbackGroup()
      timer_cb_group = client_cb_group

事实上，在这种情况下一切都能正常工作的确切条件是
定时器和客户端不能属于同一个
互斥组。
因此，以下所有配置（以及其他一些配置）
都能产生期望的结果：定时器反复
触发，服务调用得以完成。

.. tabs::

  .. group-tab:: C++

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
      timer_cb_group_ = client_cb_group_;

    或

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
      timer_cb_group_ = nullptr;

    或

    .. code-block:: cpp

      client_cb_group_ = nullptr;
      timer_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

    或

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
      timer_cb_group_ = nullptr;

  .. group-tab:: Python

    .. code-block:: python

      client_cb_group = ReentrantCallbackGroup()
      timer_cb_group = client_cb_group

    或

    .. code-block:: python

      client_cb_group = MutuallyExclusiveCallbackGroup()
      timer_cb_group = None

    或

    .. code-block:: python

      client_cb_group = None
      timer_cb_group = MutuallyExclusiveCallbackGroup()

    或

    .. code-block:: python

      client_cb_group = ReentrantCallbackGroup()
      timer_cb_group = None
