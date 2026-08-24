.. redirect-from::

    Tutorials/Tf2/Writing-A-Tf2-Listener-Cpp

编写监听器（C++）
=================

**目标：** 学习如何使用 tf2 获取帧变换。

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在之前的教程中，我们创建了一个 tf2 广播器，将 turtle 的位姿发布到 tf2。

在本教程中，我们将创建一个 tf2 监听器来开始使用 tf2。

先决条件
--------

本教程假设你已经完成 :doc:`tf2 静态广播器教程（C++） <./Writing-A-Tf2-Static-Broadcaster-Cpp>` 和 :doc:`tf2 广播器教程（C++） <./Writing-A-Tf2-Broadcaster-Cpp>`。
在上一教程中，我们创建了一个 ``learning_tf2_cpp`` 包，我们将继续在该包的基础上工作。

任务
----

1 编写监听器节点
^^^^^^^^^^^^^^^^

让我们先创建源文件。
转到我们在上一个教程中创建的 ``learning_tf2_cpp`` 包。
在 ``src`` 目录中，通过输入以下命令下载示例监听器代码：

.. tabs::

    .. group-tab:: Linux

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/turtle_tf2_listener.cpp

    .. group-tab:: macOS

        .. code-block:: console

            $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/turtle_tf2_listener.cpp

    .. group-tab:: Windows

        在 Windows 命令行提示符中：

        .. code-block:: console

              $ curl -sk https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/turtle_tf2_listener.cpp -o turtle_tf2_listener.cpp

        或者在 powershell 中：

        .. code-block:: console

              $ curl https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/turtle_tf2_listener.cpp -o turtle_tf2_listener.cpp

使用你喜欢的文本编辑器打开该文件。

.. code-block:: C++

    #include <chrono>
    #include <functional>
    #include <memory>
    #include <string>

    #include "geometry_msgs/msg/transform_stamped.hpp"
    #include "geometry_msgs/msg/twist.hpp"
    #include "rclcpp/rclcpp.hpp"
    #include "tf2/exceptions.hpp"
    #include "tf2_ros/transform_listener.hpp"
    #include "tf2_ros/buffer.hpp"
    #include "turtlesim/srv/spawn.hpp"

    using namespace std::chrono_literals;

    class FrameListener : public rclcpp::Node
    {
    public:
      FrameListener()
      : Node("turtle_tf2_frame_listener"),
        turtle_spawning_service_ready_(false),
        turtle_spawned_(false)
      {
        // Declare and acquire `target_frame` parameter
        target_frame_ = this->declare_parameter<std::string>("target_frame", "turtle1");

        tf_buffer_ =
          std::make_unique<tf2_ros::Buffer>(this->get_clock());
        tf_listener_ =
          std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

        // Create a client to spawn a turtle
        spawner_ =
          this->create_client<turtlesim::srv::Spawn>("spawn");

        // Create turtle2 velocity publisher
        publisher_ =
          this->create_publisher<geometry_msgs::msg::Twist>("turtle2/cmd_vel", 1);

        // Call on_timer function every second
        timer_ = this->create_wall_timer(
          1s, [this]() {return this->on_timer();});
      }

    private:
      void on_timer()
      {
        // Store frame names in variables that will be used to
        // compute transformations
        std::string fromFrameRel = target_frame_.c_str();
        std::string toFrameRel = "turtle2";

        if (turtle_spawning_service_ready_) {
          if (turtle_spawned_) {
            geometry_msgs::msg::TransformStamped t;

            // Look up for the transformation between target_frame and turtle2 frames
            // and send velocity commands for turtle2 to reach target_frame
            try {
              t = tf_buffer_->lookupTransform(
                toFrameRel, fromFrameRel,
                tf2::TimePointZero);
            } catch (const tf2::TransformException & ex) {
              RCLCPP_INFO(
                this->get_logger(), "Could not transform %s to %s: %s",
                toFrameRel.c_str(), fromFrameRel.c_str(), ex.what());
              return;
            }

            geometry_msgs::msg::Twist msg;

            static const double scaleRotationRate = 1.0;
            msg.angular.z = scaleRotationRate * atan2(
              t.transform.translation.y,
              t.transform.translation.x);

            static const double scaleForwardSpeed = 0.5;
            msg.linear.x = scaleForwardSpeed * sqrt(
              pow(t.transform.translation.x, 2) +
              pow(t.transform.translation.y, 2));

            publisher_->publish(msg);
          } else {
            RCLCPP_INFO(this->get_logger(), "Successfully spawned");
            turtle_spawned_ = true;
          }
        } else {
          // Check if the service is ready
          if (spawner_->service_is_ready()) {
            // Initialize request with turtle name and coordinates
            // Note that x, y and theta are defined as floats in turtlesim/srv/Spawn
            auto request = std::make_shared<turtlesim::srv::Spawn::Request>();
            request->x = 4.0;
            request->y = 2.0;
            request->theta = 0.0;
            request->name = "turtle2";

            // Call request
            using ServiceResponseFuture =
              rclcpp::Client<turtlesim::srv::Spawn>::SharedFuture;
            auto response_received_callback = [this](ServiceResponseFuture future) {
                auto result = future.get();
                if (strcmp(result->name.c_str(), "turtle2") == 0) {
                  turtle_spawning_service_ready_ = true;
                } else {
                  RCLCPP_ERROR(this->get_logger(), "Service callback result mismatch");
                }
              };
            auto result = spawner_->async_send_request(request, response_received_callback);
          } else {
            RCLCPP_INFO(this->get_logger(), "Service is not ready");
          }
        }
      }

      // Boolean values to store the information
      // if the service for spawning turtle is available
      bool turtle_spawning_service_ready_;
      // if the turtle was successfully spawned
      bool turtle_spawned_;
      rclcpp::Client<turtlesim::srv::Spawn>::SharedPtr spawner_{nullptr};
      rclcpp::TimerBase::SharedPtr timer_{nullptr};
      rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_{nullptr};
      std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};
      std::unique_ptr<tf2_ros::Buffer> tf_buffer_;
      std::string target_frame_;
    };

    int main(int argc, char * argv[])
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<FrameListener>());
      rclcpp::shutdown();
      return 0;
    }

1.1 检查代码
~~~~~~~~~~~~

要了解生成 turtle 背后的服务如何工作，请参考 :doc:`编写简单的服务与客户端（C++） <../../Beginner-Client-Libraries/Writing-A-Simple-Cpp-Service-And-Client>` 教程。

现在，让我们看看与获取帧变换相关的代码。
``tf2_ros`` 包含一个 ``TransformListener`` 类，它使接收变换的任务更简单。

.. code-block:: C++

    #include "tf2_ros/transform_listener.hpp"

这里，我们创建一个 ``TransformListener`` 对象。
监听器创建后，它开始通过网络接收 tf2 变换，并缓冲它们最多 10 秒。

.. code-block:: C++

    tf_listener_ =
      std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

.. note::

   上面的构造函数（``TransformListener(*tf_buffer_)``）是一个简化的构造函数，它在幕后创建一个单独的内部节点来管理订阅。

   如果你正在编写**可组合节点**（组件），或者需要变换监听器遵循节点特定的选项和话题重映射（例如 ``/tf`` 的命名空间或话题重映射），请改为将 ``this``（或你的节点的 ``NodeInterfaces``）传递给构造函数：

   .. code-block:: C++

      tf_listener_ =
        std::make_shared<tf2_ros::TransformListener>(*tf_buffer_, this);

   这确保订阅在现有节点上创建，并继承所有参数和话题配置。

最后，我们向监听器查询特定的变换。
我们使用以下参数调用 ``lookup_transform`` 方法：

#. 目标帧

#. 源帧

#. 我们想要变换的时间

提供 ``tf2::TimePointZero`` 只会给我们最新的可用变换。
所有这些都包在 try-catch 块中，以处理可能的异常。

.. code-block:: C++

    t = tf_buffer_->lookupTransform(
      toFrameRel, fromFrameRel,
      tf2::TimePointZero);

结果变换表示目标 turtle 相对于 ``turtle2`` 的位置和方向。
然后使用两只 turtle 之间的角度来计算跟随目标 turtle 的速度命令。
有关 tf2 的更多一般信息，另请参见 :doc:`概念部分中的 tf2 页面 <../../../Concepts/Intermediate/About-Tf2>`。

1.2 CMakeLists.txt
~~~~~~~~~~~~~~~~~~

返回上一级目录 ``learning_tf2_cpp``，那里有 ``CMakeLists.txt`` 和 ``package.xml`` 文件。

现在打开 ``CMakeLists.txt``，添加可执行文件并将其命名为 ``turtle_tf2_listener``，你稍后将用 ``ros2 run`` 使用它。

.. code-block:: console

    add_executable(turtle_tf2_listener src/turtle_tf2_listener.cpp)
    ament_target_dependencies(
        turtle_tf2_listener
        geometry_msgs
        rclcpp
        tf2
        tf2_ros
        turtlesim
    )

最后，添加 ``install(TARGETS…)`` 部分，以便 ``ros2 run`` 能找到你的可执行文件：

.. code-block:: console

    install(TARGETS
        turtle_tf2_listener
        DESTINATION lib/${PROJECT_NAME})

2 更新启动文件
^^^^^^^^^^^^^^

用文本编辑器打开 ``src/learning_tf2_cpp/launch`` 目录中名为 ``turtle_tf2_demo_launch`` 的启动文件（扩展名为 ``.py``、``.xml`` 或 ``.yaml``），向启动描述添加两个新节点，添加一个启动参数，并添加导入。
最终文件应如下所示：

.. tabs::

  .. group-tab:: Python

    .. literalinclude:: launch/listener_cpp_launch.py
        :language: python

  .. group-tab:: XML

    .. literalinclude:: launch/listener_cpp_launch.xml
        :language: xml

  .. group-tab:: YAML

    .. literalinclude:: launch/listener_cpp_launch.yaml
        :language: yaml

这将声明一个 ``target_frame`` 启动参数，为我们将要生成的第二只 turtle 启动一个广播器，并启动一个监听器来订阅这些变换。

3 构建
^^^^^^

在工作区根目录运行 ``rosdep`` 以检查缺少的依赖。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

          $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

        rosdep 仅在 Linux 上运行，因此你需要自己安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖

   .. group-tab:: Windows

        rosdep 仅在 Linux 上运行，因此你需要自己安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖

仍然在工作区根目录，构建你的包：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

          $ colcon build --packages-select learning_tf2_cpp

   .. group-tab:: macOS

      .. code-block:: console

          $ colcon build --packages-select learning_tf2_cpp

   .. group-tab:: Windows

      .. code-block:: console

          $ colcon build --merge-install --packages-select learning_tf2_cpp

打开一个新终端，导航到工作区根目录，并 source 设置文件：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

          $ . install/setup.bash

   .. group-tab:: macOS

      .. code-block:: console

          $ . install/setup.bash

   .. group-tab:: Windows

      在 Windows 命令行提示符中：

      .. code-block:: console

          $ call install\setup.bat

      或者在 powershell 中：

      .. code-block:: console

          $ .\install\setup.ps1

4 运行
^^^^^^

现在你已准备好启动完整的 turtle 演示：

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.xml

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.yaml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.py

你应该会看到有两只 turtle 的 turtle sim。
在第二个终端窗口中输入以下命令：

.. code-block:: console

    $ ros2 run turtlesim turtle_teleop_key

要查看是否正常工作，只需使用方向键驾驶第一只 turtle（确保你的终端窗口是活动的，而不是仿真器窗口），你会看到第二只 turtle 跟着第一只！

总结
----

在本教程中，你学习了如何使用 tf2 获取帧变换。
你也完成了自己的 turtlesim 演示，也就是你在 :doc:`tf2 介绍 <./Introduction-To-Tf2>` 教程中首次尝试的那个演示。
