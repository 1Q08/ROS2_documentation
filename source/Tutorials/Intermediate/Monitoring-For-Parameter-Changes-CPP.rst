.. redirect-from::

    Tutorials/Monitoring-For-Parameter-Changes-CPP

监测参数变化（C++）
===================

**目标：** 学习使用 ParameterEventHandler 类来监测并响应参数变化。

**教程级别：** 中级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

节点通常需要响应其自身参数或其他节点参数的变化。
ParameterEventHandler 类可以方便地监听参数变化，从而使你的代码能够对其做出响应。
本教程将展示如何使用 C++ 版本的 ParameterEventHandler 类来监测节点自身参数的变化以及其他节点参数的变化。

前提条件
--------

开始本教程之前，你应该先完成以下教程：

- :doc:`../Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters`
- :doc:`../Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP`

任务
----

在本教程中，你将创建一个新软件包来包含一些示例代码，编写一些使用 ParameterEventHandler 类的 C++ 代码，并测试生成的代码。


1 创建软件包
^^^^^^^^^^^^

首先，打开一个新终端并 :doc:`source 你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，使 ``ros2`` 命令能够正常工作。

按照 :ref:`这些说明 <new-directory>` 创建一个名为 ``ros2_ws`` 的新工作空间。

请记住，软件包应创建在 ``src`` 目录中，而不是工作空间的根目录。
因此，进入 ``ros2_ws/src``，然后在其中创建一个新软件包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_parameter_event_handler --dependencies rclcpp

你的终端将返回一条消息，确认你的软件包 ``cpp_parameter_event_handler`` 及其所有必要文件和文件夹已创建。

``--dependencies`` 参数将自动向 ``package.xml`` 和 ``CMakeLists.txt`` 添加必要的依赖行。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

由于你在创建软件包时使用了 ``--dependencies`` 选项，因此无需手动向 ``package.xml`` 或 ``CMakeLists.txt`` 添加依赖项。
但像往常一样，请务必向 ``package.xml`` 添加描述、维护者邮箱和姓名以及许可证信息。

.. code-block:: xml

  <description>C++ parameter events client tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

2 编写 C++ 节点
^^^^^^^^^^^^^^^

在 ``ros2_ws/src/cpp_parameter_event_handler/src`` 目录内，创建一个名为 ``parameter_event_handler.cpp`` 的新文件，并将以下代码粘贴到其中：

.. code-block:: C++

    #include <memory>

    #include "rclcpp/rclcpp.hpp"

    class SampleNodeWithParameters : public rclcpp::Node
    {
    public:
      SampleNodeWithParameters()
      : Node("node_with_parameters")
      {
        this->declare_parameter("an_int_param", 0);

        // Create a parameter subscriber that can be used to monitor parameter changes
        // (for this node's parameters as well as other nodes' parameters)
        param_subscriber_ = std::make_shared<rclcpp::ParameterEventHandler>(this);

        // Set a callback for this node's integer parameter, "an_int_param"
        auto cb = [this](const rclcpp::Parameter & p) {
            RCLCPP_INFO(
              this->get_logger(), "cb: Received an update to parameter \"%s\" of type %s: \"%ld\"",
              p.get_name().c_str(),
              p.get_type_name().c_str(),
              p.as_int());
          };
        cb_handle_ = param_subscriber_->add_parameter_callback("an_int_param", cb);
      }

    private:
      std::shared_ptr<rclcpp::ParameterEventHandler> param_subscriber_;
      std::shared_ptr<rclcpp::ParameterCallbackHandle> cb_handle_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<SampleNodeWithParameters>());
      rclcpp::shutdown();

      return 0;
    }

2.1 检查代码
~~~~~~~~~~~~
第一条语句 ``#include <memory>`` 是为了让代码能够使用 std::make_shared 模板。
下一条语句 ``#include "rclcpp/rclcpp.hpp"`` 是为了让代码能够引用 rclcpp 接口提供的各种功能，包括 ParameterEventHandler 类。

类声明之后，代码定义了一个类 ``SampleNodeWithParameters``。
该类的构造函数声明了一个整数参数 ``an_int_param``，默认值为 0。
接下来，代码创建了一个 ``ParameterEventHandler``，用于监测参数的变化。
最后，代码创建了一个 lambda 函数，并将其设置为每当 ``an_int_param`` 更新时调用的回调。

.. note::

   保存 ``add_parameter_callback`` 返回的句柄非常重要；否则，回调将无法正确注册。

.. code-block:: C++

    SampleNodeWithParameters()
    : Node("node_with_parameters")
    {
      this->declare_parameter("an_int_param", 0);

      // Create a parameter subscriber that can be used to monitor parameter changes
      // (for this node's parameters as well as other nodes' parameters)
      param_subscriber_ = std::make_shared<rclcpp::ParameterEventHandler>(this);

      // Set a callback for this node's integer parameter, "an_int_param"
      auto cb = [this](const rclcpp::Parameter & p) {
          RCLCPP_INFO(
            this->get_logger(), "cb: Received an update to parameter \"%s\" of type %s: \"%ld\"",
            p.get_name().c_str(),
            p.get_type_name().c_str(),
            p.as_int());
        };
      cb_handle_ = param_subscriber_->add_parameter_callback("an_int_param", cb);
    }

在 ``SampleNodeWithParameters`` 之后是一个典型的 ``main`` 函数，它初始化 ROS，旋转示例节点以使其能够发送和接收消息，然后在用户在控制台输入 ^C 后关闭。

.. code-block:: C++

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<SampleNodeWithParameters>());
      rclcpp::shutdown();

      return 0;
    }


2.2 添加可执行文件
~~~~~~~~~~~~~~~~~~

要构建此代码，首先打开 ``CMakeLists.txt`` 文件，并在依赖项 ``find_package(rclcpp REQUIRED)`` 下方添加以下代码行

.. code-block:: console

    add_executable(parameter_event_handler src/parameter_event_handler.cpp)
    ament_target_dependencies(parameter_event_handler rclcpp)

    install(TARGETS
      parameter_event_handler
      DESTINATION lib/${PROJECT_NAME}
    )

3 构建并运行
^^^^^^^^^^^^

构建之前，最好在工作空间的根目录（``ros2_ws``）运行 ``rosdep`` 以检查缺失的依赖项：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y

   .. group-tab:: macOS

      rosdep 仅在 Linux 上运行，所以你可以跳到下一步。

   .. group-tab:: Windows

      rosdep 仅在 Linux 上运行，所以你可以跳到下一步。

返回到工作空间的根目录 ``ros2_ws``，并构建你的新软件包：

.. code-block:: console

    $ colcon build --packages-select cpp_parameter_event_handler

打开一个新终端，进入 ``ros2_ws``，并 source 安装文件：

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

现在运行节点：

.. code-block:: console

     $ ros2 run cpp_parameter_event_handler parameter_event_handler

节点现在处于活动状态，有一个参数，并且每当该参数更新时会打印一条消息。
为了测试这一点，打开另一个终端，像之前一样 source ROS 安装文件（``. install/setup.bash``），并执行以下命令：

.. code-block:: console

    $ ros2 param set node_with_parameters an_int_param 43

运行节点的终端将显示类似以下内容的消息：

.. code-block:: console

    [INFO] [1606950498.422461764] [node_with_parameters]: cb: Received an update to parameter "an_int_param" of type integer: "43"

我们之前在节点中设置的回调已被调用，并显示了更新后的值。
现在你可以使用 ^C 在终端中终止运行中的 parameter_event_handler 示例。

扩展
----

到目前为止，我们构建并测试了一个小节点，它监测节点自身拥有的单个参数。
以该节点为基础，下面展示 ParameterEventHandler 可以发挥作用的另外两种用例。

监测另一个节点的参数变化
^^^^^^^^^^^^^^^^^^^^^^^^

你还可以使用 ParameterEventHandler 来监测另一个节点参数的变化。
让我们更新 SampleNodeWithParameters 类，使其也能监测另一个节点中参数的变化。
我们将使用 parameter_blackboard 演示应用程序来托管一个我们将监测其更新的 double 参数。

首先更新构造函数，在现有代码之后添加以下代码：

.. code-block:: C++

    // Now, add a callback to monitor any changes to the remote node's parameter. In this
    // case, we supply the remote node name.
    auto cb2 = [this](const rclcpp::Parameter & p) {
        RCLCPP_INFO(
          this->get_logger(), "cb2: Received an update to parameter \"%s\" of type: %s: \"%.02lf\"",
          p.get_name().c_str(),
          p.get_type_name().c_str(),
          p.as_double());
      };
    auto remote_node_name = std::string("parameter_blackboard");
    auto remote_param_name = std::string("a_double_param");
    cb_handle2_ = param_subscriber_->add_parameter_callback(remote_param_name, cb2, remote_node_name);


然后为额外的回调句柄添加另一个成员变量 ``cb_handle2``：

.. code-block:: C++

  private:
    std::shared_ptr<rclcpp::ParameterEventHandler> param_subscriber_;
    std::shared_ptr<rclcpp::ParameterCallbackHandle> cb_handle_;
    std::shared_ptr<rclcpp::ParameterCallbackHandle> cb_handle2_;  // Add this
  };


在终端中，返回工作空间的根目录 ``ros2_ws``，并像之前一样构建更新后的软件包：

.. code-block:: console

    $ colcon build --packages-select cpp_parameter_event_handler

然后 source 安装文件：

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

现在，为了测试远程参数的监测，首先运行新构建的 parameter_event_handler 代码：

.. code-block:: console

     $ ros2 run cpp_parameter_event_handler parameter_event_handler

接下来，从另一个终端（已初始化 ROS），按如下方式运行 parameter_blackboard 演示应用程序：

.. code-block:: console

     $ ros2 run demo_nodes_cpp parameter_blackboard

最后，从第三个终端（已初始化 ROS），让我们在 parameter_blackboard 节点上设置一个参数：

.. code-block:: console

     $ ros2 param set parameter_blackboard a_double_param 3.45

执行此命令后，你应该在 parameter_event_handler 窗口中看到输出，表明回调函数在参数更新时被调用：

.. code-block:: console

    [INFO] [1606952588.237531933] [node_with_parameters]: cb2: Received an update to parameter "a_double_param" of type: double: "3.45"

同时监测所有节点参数
^^^^^^^^^^^^^^^^^^^^

如果你需要同时监测多个节点或参数，为每个参数分别调用 ``add_parameter_callback`` 会很繁琐。
在这种情况下，你可以使用 ``add_parameter_event_callback`` 注册一个单一回调，当 *任何* 节点的 *任何* 参数变化时触发。

为此，首先更新 SampleNodeWithParameters 构造函数，添加以下代码：

.. code-block:: C++

    this->declare_parameter("another_double_param", 0.0);

    ...

    auto event_cb = [this](const rcl_interfaces::msg::ParameterEvent & parameter_event) {
        RCLCPP_INFO(
          this->get_logger(), "Received parameter event from node \"%s\"",
          parameter_event.node.c_str());

        for (const auto& p : parameter_event.changed_parameters) {
          RCLCPP_INFO(
            this->get_logger(), "Inside event: \"%s\" changed to %s",
            p.name.c_str(),
            rclcpp::Parameter::from_parameter_msg(p).value_to_string().c_str());
        };
      };
    event_cb_handle_ = param_subscriber_->add_parameter_event_callback(event_cb);

这会声明一个新的 double 参数 ``another_double_param``，并添加一个将监测两个参数的事件回调。
请注意，``parameter_event`` 的类型为 {interface(rcl_interfaces/msg/ParameterEvent)}。
尽管本教程未展示，事件回调也可以用于监测参数何时被添加或删除。

最后，别忘了将事件回调句柄添加为私有成员：

.. code-block:: C++

    private:
      ...
      std::shared_ptr<rclcpp::ParameterEventCallbackHandle> event_cb_handle_;

返回工作空间的根目录 ``ros2_ws``，并像之前一样重新构建更新后的软件包：

.. code-block:: console

    $ colcon build --packages-select cpp_parameter_event_handler

然后 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install\setup.bat

要测试新的事件回调，首先运行 parameter_event_handler 节点：

.. code-block:: console

     $ ros2 run cpp_parameter_event_handler parameter_event_handler

然后，从第二个终端（已 source ROS），让我们设置原始的 int 参数：

.. code-block:: console

     $ ros2 param set node_with_parameters an_int_param 44

执行此命令后，你应该看到单参数回调和事件回调都被触发：

.. code-block:: console

      [INFO] [1747144403.418980063] [node_with_parameters]: cb: Received an update to parameter "an_int_param" of type integer: "44"
      [INFO] [1747144403.419086611] [node_with_parameters]: Received parameter event from node "/node_with_parameters"
      [INFO] [1747144403.419114103] [node_with_parameters]: Inside event: "an_int_param" changed to 44

现在设置新的 double 参数：

.. code-block:: console

     $ ros2 param set node_with_parameters another_double_param 4.4

由于没有为 double 参数添加单参数回调（通过 ``add_parameter_callback``），我们应该只看到事件回调被触发：

.. code-block:: console

      [INFO] [1747144452.917437113] [node_with_parameters]: Received parameter event from node "/node_with_parameters"
      [INFO] [1747144452.917591649] [node_with_parameters]: Inside event: "another_double_param" changed to 4.400000

.. note::

   一次性设置多个参数时，最好使用 ``set_parameters_atomically``，这在 :doc:`../../Concepts/Basic/About-Parameters` 中有解释。
   这样，事件回调只会被触发一次。

小结
----

你创建了一个带参数的节点，并使用 ParameterEventHandler 类设置了一个回调来监测该参数的变化。
你还使用同一个类来监测远程节点的变化，以及在单个事件回调中监测所有参数。
ParameterEventHandler 是监测参数变化以便你能响应更新值的便捷方式。

相关内容
--------

要了解如何为 ROS 2 改编 ROS 1 参数文件，请参阅 :doc:`将 YAML 参数文件从 ROS 1 迁移到 ROS2 <../../How-To-Guides/Migrating-from-ROS1/Migrating-Parameters>` 教程。


