使用 Node Interfaces 模板类（C++）
==================================

**目标：** 学习如何使用 ``rclcpp::NodeInterfaces<>`` 访问 ``Node`` 信息

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:


概述
----

并非所有 ROS 节点都是生而平等的！
``rclcpp::Node`` 和 ``rclcpp_lifecycle::LifecycleNode`` 类不共享继承树，这意味着 ROS 开发者在编写接受 ROS 节点指针作为参数的函数时，可能会遇到编译时类型问题。
为解决此问题，``rclcpp`` 包含了 ``rclcpp::NodeInterfaces<>`` 模板类型，应将其作为将常规节点和 lifecycle 节点传递给函数的首选约定。
这个 `ROSCon 2023 闪电演讲 <https://vimeo.com/879001243#t=16m0s>`_ 简洁地总结了该问题及其解决方法。
以下教程将展示如何使用 ``rclcpp::NodeInterfaces<>`` 作为适用于所有 ROS 节点类型的可靠且紧凑的接口。

``rclcpp::NodeInterfaces<>`` 模板类提供了一种紧凑高效的方式来管理 ROS 2 中的 Node Interfaces。
当使用不同类型的 ``Nodes``（例如不共享同一继承树的 ``rclcpp::Node`` 和 ``rclcpp_lifecycle::LifecycleNode``）时，这尤其有用。

1 使用 ``SharedPtr`` 访问节点信息
---------------------------------

在下面的示例中，我们创建一个名为 ``Simple_Node`` 的简单 ``Node``，并定义一个接受指向该 ``Node`` 的 ``SharedPtr`` 的函数 ``node_info``。
该函数检索并打印 ``Node`` 的名称。

.. code-block:: c++

    #include <memory>
    #include "rclcpp/rclcpp.hpp"

    void node_info(rclcpp::Node::SharedPtr node)
    {
      RCLCPP_INFO(node->get_logger(), "Node name: %s", node->get_name());
    }

    class SimpleNode : public rclcpp::Node
    {
    public:
      SimpleNode(const std::string & node_name)
      : Node(node_name)
      {
      }
    };

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<SimpleNode>("Simple_Node");
      node_info(node);
    }

输出：

.. code-block:: console

    [INFO] [Simple_Node]: Node name: Simple_Node

虽然这种方法对于 ``rclcpp::Node`` 类型的参数很有效，但对于 ``rclcpp_lifecycle::LifecycleNode`` 等其他节点类型则不适用。

2 显式传递 ``rclcpp::node_interfaces``
--------------------------------------

一种更健壮、适用于所有节点类型的方法是显式传递 ``rclcpp::node_interfaces`` 作为函数参数，如下例所示。
在接下来的示例中，我们创建一个名为 ``node_info`` 的函数，它接受两个 ``rclcpp::node_interfaces`` 参数：``NodeBaseInterface`` 和 ``NodeLoggingInterface``，并打印 ``Node`` 名称。
然后我们创建两个类型为 ``rclcpp_lifecycle::LifecycleNode`` 和 ``rclcpp::Node`` 的节点，并将它们的接口传入 ``node_info``。

.. code-block:: c++

    void node_info(std::shared_ptr<rclcpp::node_interfaces::NodeBaseInterface> base_interface,
                   std::shared_ptr<rclcpp::node_interfaces::NodeLoggingInterface> logging_interface)
    {
      RCLCPP_INFO(logging_interface->get_logger(), "Node name: %s", base_interface->get_name());
    }

    class SimpleNode : public rclcpp::Node
    {
    public:
      SimpleNode(const std::string & node_name)
      : Node(node_name)
      {
      }
    };

    class LifecycleTalker : public rclcpp_lifecycle::LifecycleNode
    {
    public:
      explicit LifecycleTalker(const std::string & node_name, bool intra_process_comms = false)
      : rclcpp_lifecycle::LifecycleNode(node_name,
          rclcpp::NodeOptions().use_intra_process_comms(intra_process_comms))
      {}
    }

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::executors::SingleThreadedExecutor exe;
      auto node = std::make_shared<SimpleNode>("Simple_Node");
      auto lc_node = std::make_shared<LifecycleTalker>("Simple_LifeCycle_Node");
      node_info(node->get_node_base_interface(),node->get_node_logging_interface());
      node_info(lc_node->get_node_base_interface(),lc_node->get_node_logging_interface());
    }

输出：

.. code-block:: console

    [INFO] [Simple_Node]: Node name: Simple_Node
    [INFO] [Simple_LifeCycle_Node]: Node name: Simple_LifeCycle_Node

随着函数复杂度的增加，``rclcpp::node_interfaces`` 参数的数量也会增加，从而带来可读性和紧凑性问题。
为了使代码更灵活并与不同节点类型兼容，我们使用 ``rclcpp::NodeInterfaces<>``。

3 使用 ``rclcpp::NodeInterfaces<>``
-----------------------------------

访问 ``Node`` 类型信息的推荐方式是通过 ``Node Interfaces``。

下面与上一个示例类似，创建了一个 ``rclcpp_lifecycle::LifecycleNode`` 和一个 ``rclcpp::Node``。

.. code-block:: c++

    #include <memory>
    #include <string>
    #include <thread>
    #include "lifecycle_msgs/msg/transition.hpp"
    #include "rclcpp/rclcpp.hpp"
    #include "rclcpp_lifecycle/lifecycle_node.hpp"
    #include "rclcpp_lifecycle/lifecycle_publisher.hpp"
    #include "rclcpp/node_interfaces/node_interfaces.hpp"

    using MyNodeInterfaces =
      rclcpp::node_interfaces::NodeInterfaces<rclcpp::node_interfaces::NodeBaseInterface, rclcpp::node_interfaces::NodeLoggingInterface>;

    void node_info(MyNodeInterfaces interfaces)
    {
      auto base_interface = interfaces.get_node_base_interface();
      auto logging_interface = interfaces.get_node_logging_interface();
      RCLCPP_INFO(logging_interface->get_logger(), "Node name: %s", base_interface->get_name());
    }

    class SimpleNode : public rclcpp::Node
    {
    public:
      SimpleNode(const std::string & node_name)
      : Node(node_name)
      {
      }
    };

    class LifecycleTalker : public rclcpp_lifecycle::LifecycleNode
    {
    public:
      explicit LifecycleTalker(const std::string & node_name, bool intra_process_comms = false)
      : rclcpp_lifecycle::LifecycleNode(node_name,
          rclcpp::NodeOptions().use_intra_process_comms(intra_process_comms))
      {}
    };

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::executors::SingleThreadedExecutor exe;
      auto node = std::make_shared<SimpleNode>("Simple_Node");
      auto lc_node = std::make_shared<LifecycleTalker>("Simple_LifeCycle_Node");
      node_info(*node);
      node_info(*lc_node);
    }

输出：

.. code-block:: console

    [INFO] [Simple_Node]: Node name: Simple_Node
    [INFO] [Simple_LifeCycle_Node]: Node name: Simple_LifeCycle_Node

3.1 检查代码
~~~~~~~~~~~~

.. code-block:: c++

    using MyNodeInterfaces =
      rclcpp::node_interfaces::NodeInterfaces<rclcpp::node_interfaces::NodeBaseInterface, rclcpp::node_interfaces::NodeLoggingInterface>;

    void node_info(MyNodeInterfaces interfaces)
    {
      auto base_interface = interfaces.get_node_base_interface();
      auto logging_interface = interfaces.get_node_logging_interface();
      RCLCPP_INFO(logging_interface->get_logger(), "Node name: %s", base_interface->get_name());
    }

此函数不是接受 ``SharedPtr`` 或节点接口，而是接受对一个 ``rclcpp::node_interfaces::NodeInterfaces`` 对象的引用。
使用这种方法的另一个优势是支持对类节点对象的隐式转换。
这意味着可以将任何类节点对象直接传递给期望 ``rclcpp::node_interfaces::NodeInterfaces`` 对象的函数。

它提取：

* ``NodeBaseInterface`` 提供基本节点功能。
* ``NodeLoggingInterface`` 启用日志记录。

然后，它检索并打印节点名称。

.. code-block:: c++

    class SimpleNode : public rclcpp::Node
    {
    public:
      SimpleNode(const std::string & node_name)
      : Node(node_name)
      {
      }
    };

    class LifecycleTalker : public rclcpp_lifecycle::LifecycleNode
    {
    public:
      explicit LifecycleTalker(const std::string & node_name, bool intra_process_comms = false)
      : rclcpp_lifecycle::LifecycleNode(node_name,
          rclcpp::NodeOptions().use_intra_process_comms(intra_process_comms))
      {}
    };

接下来，我们创建一个 ``rclcpp::Node`` 和一个 ``rclcpp_lifecycle::LifecycleNode`` 类。
``rclcpp_lifecycle::LifecycleNode`` 类通常包含状态转换 ``Unconfigured``、``Inactive``、``Active`` 和 ``Finalized`` 的函数。
但是，为了演示目的，这里没有包含它们。

.. code-block:: c++

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::executors::SingleThreadedExecutor exe;
      auto node = std::make_shared<SimpleNode>("Simple_Node");
      auto lc_node = std::make_shared<LifecycleTalker>("Simple_LifeCycle_Node");
      node_info(*node);
      node_info(*lc_node);
    }

在 main 函数中，创建了指向 ``rclcpp_lifecycle::LifecycleNode`` 和 ``rclcpp::Node`` 的 ``SharedPtr``。
上面声明的函数分别以每种节点类型作为参数调用一次。

.. note:: 需要解引用 ``SharedPtr``，因为模板接受对 ``NodeT`` 对象的引用。
