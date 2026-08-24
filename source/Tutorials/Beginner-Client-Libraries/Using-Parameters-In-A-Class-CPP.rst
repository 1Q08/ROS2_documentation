.. redirect-from::

    Tutorials/Using-Parameters-In-A-Class-CPP

.. _CppParamNode:

在类中使用参数（C++）
=====================

**目标：** 使用 C++ 创建并运行一个带 ROS 参数的类。

**教程级别：** 入门

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在创建你自己的 :doc:`节点 <../Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>` 时，有时你需要添加可以从 launch 文件设置的参数。

本教程将向你展示如何在 C++ 类中创建这些参数，以及如何在 launch 文件中设置它们。

前置条件
--------

在之前的教程中，你学习了如何 :doc:`创建工作空间 <./Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <./Creating-Your-First-ROS2-Package>`。
你还学习了 :doc:`参数 <../Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters>` 及其在 ROS 2 系统中的功能。

任务
----

1 创建一个包
^^^^^^^^^^^^

打开一个新终端并 :doc:`source 你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，以便 ``ros2`` 命令能够工作。

按照 :ref:`这些说明 <new-directory>` 创建一个名为 ``ros2_ws`` 的新工作空间。

回想一下，包应该创建在 ``src`` 目录中，而不是工作空间的根目录中。
进入 ``ros2_ws/src`` 并创建一个新包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_parameters --dependencies rclcpp

你的终端将返回一条消息，验证你的包 ``cpp_parameters`` 及其所有必需文件和文件夹已创建。

``--dependencies`` 参数会自动将必要的依赖行添加到 ``package.xml`` 和 ``CMakeLists.txt``。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

因为在包创建期间你使用了 ``--dependencies`` 选项，所以你不必手动向 ``package.xml`` 或 ``CMakeLists.txt`` 添加依赖。

不过，一如既往，请务必向 ``package.xml`` 添加描述、维护者邮箱和姓名，以及许可信息。

.. code-block:: xml

  <description>C++ parameter tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

2 编写 C++ 节点
^^^^^^^^^^^^^^^

在 ``ros2_ws/src/cpp_parameters/src`` 目录中，创建一个名为 ``cpp_parameters_node.cpp`` 的新文件，并在其中粘贴以下代码：

.. code-block:: C++

    #include <chrono>
    #include <functional>
    #include <string>

    #include <rclcpp/rclcpp.hpp>

    using namespace std::chrono_literals;

    class MinimalParam : public rclcpp::Node
    {
    public:
      MinimalParam()
      : Node("minimal_param_node")
      {
        this->declare_parameter("my_parameter", "world");

        auto timer_callback = [this](){
          std::string my_param = this->get_parameter("my_parameter").as_string();

          RCLCPP_INFO(this->get_logger(), "Hello %s!", my_param.c_str());

          std::vector<rclcpp::Parameter> all_new_parameters{rclcpp::Parameter("my_parameter", "world")};
          this->set_parameters(all_new_parameters);
        };
        timer_ = this->create_wall_timer(1000ms, timer_callback);
      }

    private:
      rclcpp::TimerBase::SharedPtr timer_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<MinimalParam>());
      rclcpp::shutdown();
      return 0;
    }

2.1 检查代码
~~~~~~~~~~~~
顶部的 ``#include`` 语句是包依赖。

下一段代码创建了类和构造函数。
构造函数的第一行创建了一个名为 ``my_parameter``、默认值为 ``world`` 的参数。
参数类型由默认值推断，因此在这种情况下它会被设置为字符串类型。
接下来，声明了一个名为 ``timer_callback`` 的 `lambda 函数 <https://en.cppreference.com/w/cpp/language/lambda>`_。
它对当前对象 ``this`` 进行引用捕获，不接受输入参数并返回 void。
我们的 ``timer_callback`` 函数的第一行从节点获取参数 ``my_parameter``，并将其存储在 ``my_param`` 中。
然后 ``RCLCPP_INFO`` 函数确保事件被记录。
``set_parameters`` 函数将参数 ``my_parameter`` 设置回默认字符串值 ``world``。
如果用户从外部更改了参数，这可以确保它总是被重置回原始值。
最后，``timer_`` 被初始化为 1000ms 的周期，这会导致 ``timer_callback`` 函数每秒执行一次。

.. code-block:: C++

    class MinimalParam : public rclcpp::Node
    {
    public:
      MinimalParam()
      : Node("minimal_param_node")
      {
        this->declare_parameter("my_parameter", "world");

        auto timer_callback = [this](){
          std::string my_param = this->get_parameter("my_parameter").as_string();

          RCLCPP_INFO(this->get_logger(), "Hello %s!", my_param.c_str());

          std::vector<rclcpp::Parameter> all_new_parameters{rclcpp::Parameter("my_parameter", "world")};
          this->set_parameters(all_new_parameters);
        };
        timer_ = this->create_wall_timer(1000ms, timer_callback);
      }

最后是 ``timer_`` 的声明。

.. code-block:: C++

    private:
      rclcpp::TimerBase::SharedPtr timer_;

在我们的 ``MinimalParam`` 之后是 ``main``。
这里初始化了 ROS 2，构造了一个 ``MinimalParam`` 类的实例，并且 ``rclcpp::spin`` 开始处理来自节点的数据。

.. code-block:: C++

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<MinimalParam>());
      rclcpp::shutdown();
      return 0;
    }

2.1.1 （可选）添加 ParameterDescriptor
""""""""""""""""""""""""""""""""""""""
可选地，你可以为参数设置一个描述符。
描述符允许你指定参数的文本描述及其约束，例如将其设为只读、指定范围等。
为此，构造函数中的代码必须更改为：

.. code-block:: C++

    // ...

    class MinimalParam : public rclcpp::Node
    {
    public:
      MinimalParam()
      : Node("minimal_param_node")
      {
        auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
        param_desc.description = "This parameter is mine!";

        this->declare_parameter("my_parameter", "world", param_desc);

        auto timer_callback = [this](){
          std::string my_param = this->get_parameter("my_parameter").as_string();

          RCLCPP_INFO(this->get_logger(), "Hello %s!", my_param.c_str());

          std::vector<rclcpp::Parameter> all_new_parameters{rclcpp::Parameter("my_parameter", "world")};
          this->set_parameters(all_new_parameters);
        };
        timer_ = this->create_wall_timer(1000ms, timer_callback);

      }

其余代码保持不变。
一旦你运行节点，就可以运行 ``ros2 param describe /minimal_param_node my_parameter`` 来查看类型和描述。


2.2 添加可执行文件
~~~~~~~~~~~~~~~~~~

现在打开 ``CMakeLists.txt`` 文件。
在依赖 ``find_package(rclcpp REQUIRED)`` 下面添加以下几行代码。

.. code-block:: cmake

    add_executable(minimal_param_node src/cpp_parameters_node.cpp)
    ament_target_dependencies(minimal_param_node rclcpp)

    install(TARGETS
        minimal_param_node
      DESTINATION lib/${PROJECT_NAME}
    )


3 构建并运行
^^^^^^^^^^^^

在构建之前，最好在工作空间的根目录（``ros2_ws``）运行 ``rosdep`` 来检查缺失的依赖：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

   .. group-tab:: Windows

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

返回到工作空间的根目录 ``ros2_ws``，并构建你的新包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select cpp_parameters

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select cpp_parameters

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select cpp_parameters

打开一个新终端，进入 ``ros2_ws``，然后 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在运行节点。
终端应该每秒返回一次 ``Hello World`` 消息：

.. code-block:: console

     $ ros2 run cpp_parameters minimal_param_node
    [INFO] [minimal_param_node]: Hello world!

现在你可以看到参数的默认值，但你想能够自己设置它。
有两种方法可以实现这一点。

3.1 通过控制台更改
~~~~~~~~~~~~~~~~~~

这部分将使用你从 :doc:`关于参数的教程 <../Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters>` 中获得的知识，并将其应用到你刚刚创建的节点上。

确保节点正在运行：

.. code-block:: console

     $ ros2 run cpp_parameters minimal_param_node

打开另一个终端，再次从 ``ros2_ws`` 内 source 安装文件，然后输入以下行：

.. code-block:: console

    $ ros2 param list

在那里你会看到自定义参数 ``my_parameter``。
要更改它，只需在控制台中运行以下行：

.. code-block:: console

    $ ros2 param set /minimal_param_node my_parameter earth

如果你得到了输出 ``Set parameter successful``，你就知道它成功了。
如果你查看另一个终端，你应该会看到输出变为 ``[INFO] [minimal_param_node]: Hello earth!``

3.2 通过 launch 文件更改
~~~~~~~~~~~~~~~~~~~~~~~~
你也可以在 launch 文件中设置参数，但首先你需要添加 launch 目录。
在 ``ros2_ws/src/cpp_parameters/`` 目录中，创建一个名为 ``launch`` 的新目录。
在其中，创建一个名为 ``cpp_parameters_launch.py`` 的新文件。


.. literalinclude:: launch/cpp_parameters_launch.py
  :language: python

在这里你可以看到，当我们启动节点 ``minimal_param_node`` 时，我们将 ``my_parameter`` 设置为 ``earth``。
通过添加下面两行，我们确保输出打印在我们的控制台中。

.. code-block:: python

          output="screen",
          emulate_tty=True,

现在打开 ``CMakeLists.txt`` 文件。
在你之前添加的行下面，添加以下几行代码。

.. code-block:: cmake

    install(
      DIRECTORY launch
      DESTINATION share/${PROJECT_NAME}
    )

打开一个控制台，进入工作空间的根目录 ``ros2_ws``，然后构建你的新包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select cpp_parameters

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select cpp_parameters

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select cpp_parameters

然后在一个新终端中 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在使用我们刚刚创建的 launch 文件运行节点。
终端第一次应该返回以下消息：

.. code-block:: console

     $ ros2 launch cpp_parameters cpp_parameters_launch.py
     [INFO] [custom_minimal_param_node]: Hello earth!

后续输出应该每秒显示一次 ``[INFO] [minimal_param_node]: Hello world!``。

总结
----

你创建了一个带有自定义参数的节点，该参数可以从 launch 文件或命令行设置。
你向包配置文件添加了依赖、可执行文件和 launch 文件，这样你就可以构建并运行它们，并看到参数的实际效果。

后续步骤
--------

既然你已经有了自己的包和 ROS 2 系统，:doc:`下一个教程 <./Getting-Started-With-Ros2doctor>` 将向你展示如何在你遇到问题时检查你的环境和系统中的问题。
