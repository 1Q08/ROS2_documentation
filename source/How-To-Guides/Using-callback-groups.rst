使用回调组
==========

在多线程执行器（Multi-Threaded Executor）中运行节点时，ROS 2 提供回调组
（callback groups）作为控制不同回调执行的工具。
本页面旨在作为如何高效使用回调组的指南。
这里假设读者对 :doc:`执行器 <../Concepts/Intermediate/About-Executors>` 的概念有基本的了解。

.. contents:: 目录
   :local:

回调组基础
----------

在多线程执行器中运行节点时，
ROS 2 提供两种不同类型的回调组，用于控制回调的执行：

* 互斥回调组（Mutually Exclusive Callback Group）
* 可重入回调组（Reentrant Callback Group）

这些回调组以不同的方式限制其回调的执行。
简而言之：

* 互斥回调组防止其回调被并行执行——本质上使得组中的回调
  就像被单线程执行器（SingleThreadedExecutor）执行一样。
* 可重入回调组允许执行器以它认为合适的任何方式调度和执行
  该组的回调，而不受限制。
  这意味着，除了不同的回调可以并行运行之外，
  同一个回调的不同实例也可能被并发执行。
* 属于不同回调组（任何类型）的回调始终可以
  相互并行执行。

同样重要的是要记住，不同的 ROS 2 实体会将它们的回调组
传递给它们产生的所有回调。
例如，如果为动作客户端分配一个回调组，
那么该客户端创建的所有回调都会被分配到该回调组。

在 rclcpp 中，回调组可以通过节点的 ``create_callback_group``
函数创建，在 rclpy 中则通过调用组的构造函数创建。
然后，在创建订阅、定时器等时，可以将该回调组作为参数/选项传入。
应该保留对回调组的引用，否则与该回调组关联的回调
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

如果用户在创建订阅、定时器等时没有指定任何回调组，
该实体将被分配到节点的默认回调组。
默认回调组是一个互斥回调组，在 rclcpp 中可以通过
``NodeBaseInterface::get_default_callback_group()`` 查询，在 rclpy 中可以通过
``Node.default_callback_group`` 查询。

关于回调
^^^^^^^^

在 ROS 2 和执行器的上下文中，回调是指其
调度和执行由执行器处理的函数。
在此上下文中，回调的示例有

* 订阅回调（接收并处理来自话题的数据），
* 定时器回调，
* 服务回调（用于在服务器中执行服务请求），
* 动作服务器和客户端中的各种回调，
* Future 的完成回调（done-callbacks）。

下面是关于回调的一些要点，在使用回调组时应该牢记。

* ROS 2 中几乎一切都是回调！
  从定义上讲，每个由执行器运行的函数都是回调。
  ROS 2 系统中的非回调函数主要位于
  系统的边缘（用户和传感器输入等）。
* 有时回调是隐藏的，它们的存在在用户/开发者 API 中可能并不明显。
  对于任何类型的对服务或动作的“同步”调用（在 rclpy 中），情况尤其如此。
  例如，对服务的同步调用 ``Client.call(request)``
  会添加一个 Future 的完成回调，该回调需要在
  函数调用的执行期间被执行，但此回调对用户来说并不直接可见。


控制执行
--------

为了使用回调组控制执行，可以考虑以下准则。

对于单个回调与自身的交互：

* 如果它应该与自身并行执行，则将其注册到可重入回调组。
  一个示例情况可以是动作/服务服务器需要能够
  并行处理多个动作调用。

* 如果它应该\ **永不**\ 与自身并行执行，则将其注册到互斥回调组。
  一个示例情况可以是运行控制循环并发布控制命令的定时器回调。

对于不同回调彼此之间的交互：

* 如果它们应该\ **永不**\ 并行执行，则将它们注册到同一个互斥回调组。
  一个示例情况可以是回调正在访问共享的、关键的且非线程安全的资源。

如果它们应该并行执行，你有两种选择，
取决于单个回调是否应该能够与自身重叠：

* 将它们注册到不同的互斥回调组（单个回调不重叠）

* 将它们注册到可重入回调组（单个回调重叠）

并行运行不同回调的一个示例情况是，一个节点具有
一个同步服务客户端和一个调用该服务的定时器。
参见下面的详细示例。

避免死锁
--------

错误地设置节点的回调组可能导致死锁（或其他不希望的行为），
尤其是当希望使用对服务或动作的同步调用时。
事实上，甚至 ROS 2 的 API 文档也提到，
对动作或服务的同步调用不应在回调中进行，
因为这可能导致死锁。
虽然在这方面使用异步调用确实更安全，但同步
调用也可以使其正常工作。
另一方面，同步调用也有其优点，例如
使代码更简单、更易于理解。
因此，本节提供了一些关于如何正确设置节点的
回调组以避免死锁的准则。

这里要注意的第一点是，每个节点的默认回调组都是
互斥回调组。
如果用户在创建定时器、订阅、客户端等时没有指定任何其他回调组，
那么这些实体当时或之后创建的任何回调都将使用节点的默认回调组。
此外，如果节点中的所有内容都使用同一个互斥
回调组，那么该节点本质上表现得就像由
单线程执行器处理一样，即使指定了多线程执行器也是如此！
因此，每当决定使用多线程执行器时，
都应该始终指定一些回调组，以便
执行器的选择有意义。

牢记以上内容，以下是一些有助于避免死锁的准则：

* 如果你在任何类型的回调中进行同步调用，则该回调和
  发起调用的客户端需要属于

  * 不同的回调组（任何类型），或
  * 一个可重入回调组。

* 如果由于其他要求（例如线程安全性和/或在等待结果时阻塞其他回调）
  而无法使用上述配置（或者如果你希望绝对确保永远不存在
  死锁的可能性），请使用异步调用。

不满足第一点将总是导致死锁。
这种情况的一个示例是在定时器回调中进行同步服务调用
（参见下一节的示例）。


示例
----

让我们看一些不同回调组设置的简单示例。
下面的演示代码考虑在定时器回调中同步调用服务。

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
                auto service_callback = [this](
                    const std::shared_ptr<rmw_request_id_t> request_header,
                    const std::shared_ptr<std_srvs::srv::Empty::Request> request,
                    const std::shared_ptr<std_srvs::srv::Empty::Response> response)
                {
                    (void)request_header;
                    (void)request;
                    (void)response;
                    RCLCPP_INFO(this->get_logger(), "Received request, responding...");
                };
                service_ptr_ = this->create_service<std_srvs::srv::Empty>(
                        "test_service",
                        service_callback
                );
            }

        private:
            rclcpp::Service<std_srvs::srv::Empty>::SharedPtr service_ptr_;

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

另一个节点包含该服务的客户端，以及一个用于发起
服务调用的定时器：

.. tabs::

  .. group-tab:: C++

    *注意：* rclcpp 中的服务客户端 API 并不提供与 rclpy 中类似的
    同步调用方法，因此我们等待 future 对象来模拟
    同步调用的效果。

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

              auto timer_callback = [this](){
                  RCLCPP_INFO(this->get_logger(), "Sending request");
                  auto request = std::make_shared<std_srvs::srv::Empty::Request>();
                  auto result_future = client_ptr_->async_send_request(request);
                  std::future_status status = result_future.wait_for(10s);  // timeout to guarantee a graceful finish
                  if (status == std::future_status::ready) {
                      RCLCPP_INFO(this->get_logger(), "Received response");
                  }
              };

              timer_ptr_ = this->create_wall_timer(1s, timer_callback, timer_cb_group_);
          }

      private:
          rclcpp::CallbackGroup::SharedPtr client_cb_group_;
          rclcpp::CallbackGroup::SharedPtr timer_cb_group_;
          rclcpp::Client<std_srvs::srv::Empty>::SharedPtr client_ptr_;
          rclcpp::TimerBase::SharedPtr timer_ptr_;

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

客户端节点的构造函数中包含用于设置服务客户端和定时器
回调组的选项。
使用上面的默认设置（两者都为 ``nullptr`` / ``None``）时，
定时器和客户端都将使用节点的默认
互斥回调组。

问题所在
^^^^^^^^

由于我们使用 1 秒的定时器发起服务调用，预期的结果是
服务每秒被调用一次，客户端总是收到响应并打印
``Received response``。
如果我们尝试在终端中运行服务器和客户端节点，
会得到以下输出。

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

结果是，服务并没有被反复调用，
第一次调用的响应始终没有被收到，此后
客户端节点似乎卡住并且不再发起进一步的调用。
也就是说，执行在一个死锁处停止了！

原因在于定时器回调和客户端使用了
同一个互斥回调组（节点的默认回调组）。
当发起服务调用时，客户端会将其回调组传递给
Future 对象（在 Python 版本中隐藏在 call 方法内部），
该 Future 的完成回调需要执行之后，服务调用的结果
才能可用。
但由于这个完成回调和定时器回调位于同一个
互斥组中，并且定时器回调仍在执行
（等待服务调用的结果），因此完成回调永远无法执行。
被卡住的定时器回调也阻塞了它自身的任何其他执行，所以
定时器不会再第二次触发。

解决方案
^^^^^^^^

我们可以轻松地修复这个问题——例如——将定时器和客户端
分配到不同的回调组。
因此，让我们把客户端节点构造函数的前两行改为
如下所示（其余部分保持不变）：

.. tabs::

  .. group-tab:: C++

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
      timer_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

  .. group-tab:: Python

    .. code-block:: python

      client_cb_group = MutuallyExclusiveCallbackGroup()
      timer_cb_group = MutuallyExclusiveCallbackGroup()

现在我们得到了预期的结果，即定时器反复触发并且
每次服务调用都如预期般获得结果：

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

有人可能会想，仅仅避免使用节点的默认回调组是否
就足够了。
事实并非如此：将默认组替换为
不同的互斥组不会有任何改变。
因此，以下配置同样会导致之前
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

事实上，在这种情况下一功能正常的精确条件是：
定时器和客户端必须不属于同一个
互斥组。
因此，以下所有配置（以及一些其他配置）
都能产生期望的结果，即定时器反复触发
并且服务调用能够完成。

.. tabs::

  .. group-tab:: C++

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
      timer_cb_group_ = client_cb_group_;

    or

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
      timer_cb_group_ = nullptr;

    or

    .. code-block:: cpp

      client_cb_group_ = nullptr;
      timer_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

    or

    .. code-block:: cpp

      client_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
      timer_cb_group_ = nullptr;

  .. group-tab:: Python

    .. code-block:: python

      client_cb_group = ReentrantCallbackGroup()
      timer_cb_group = client_cb_group

    or

    .. code-block:: python

      client_cb_group = MutuallyExclusiveCallbackGroup()
      timer_cb_group = None

    or

    .. code-block:: python

      client_cb_group = None
      timer_cb_group = MutuallyExclusiveCallbackGroup()

    or

    .. code-block:: python

      client_cb_group = ReentrantCallbackGroup()
      timer_cb_group = None
