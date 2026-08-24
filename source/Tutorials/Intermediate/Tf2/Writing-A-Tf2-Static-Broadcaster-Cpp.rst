.. redirect-from::

    Tutorials/Tf2/Writing-A-Tf2-Static-Broadcaster-Cpp

编写静态广播器（C++）
=====================

**目标：** 学习如何将静态坐标帧广播到 tf2。

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

发布静态变换对于定义机器人基座与其传感器或非移动部件之间的关系很有用。
例如，在位于激光扫描仪中心的帧中推理激光扫描测量是最容易的。

这是一个独立的教程，涵盖静态变换的基础知识，由两部分组成。
在第一部分中，我们将编写代码将静态变换发布到 tf2。
在第二部分中，我们将解释如何使用 ``tf2_ros`` 中的命令行 ``static_transform_publisher`` 可执行工具。

在接下来的两个教程中，我们将编写代码来重现 :doc:`tf2 介绍 <./Introduction-To-Tf2>` 教程中的演示。
之后，后续教程将重点用更高级的 tf2 功能扩展演示。

先决条件
--------

在前面的教程中，你学习了如何 :doc:`创建工作区 <../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>`。

任务
----

1 创建包
^^^^^^^^

首先，我们将创建一个用于本教程和后续教程的包。
名为 ``learning_tf2_cpp`` 的包将依赖 ``geometry_msgs``、``rclcpp``、``tf2``、``tf2_ros`` 和 ``turtlesim``。
本教程的代码存储 `在这里 <https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/static_turtle_tf2_broadcaster.cpp>`_。

打开一个新终端并 :doc:`source 你的 ROS 2 安装 <../../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，以便 ``ros2`` 命令可以正常工作。
导航到工作区的 ``src`` 文件夹并创建一个新包：

.. code-block:: console

   $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 --dependencies geometry_msgs rclcpp tf2 tf2_ros turtlesim -- learning_tf2_cpp

你的终端将返回一条消息，验证你的包 ``learning_tf2_cpp`` 及其所有必要文件和文件夹的创建。

2 编写静态广播器节点
^^^^^^^^^^^^^^^^^^^^

让我们先创建源文件。
在 ``src/learning_tf2_cpp/src`` 目录中，通过输入以下命令下载示例静态广播器代码：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

          $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/static_turtle_tf2_broadcaster.cpp

   .. group-tab:: macOS

      .. code-block:: console

          $ wget https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/static_turtle_tf2_broadcaster.cpp

   .. group-tab:: Windows

      在 Windows 命令行提示符中：

      .. code-block:: console

          $ curl -sk https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/static_turtle_tf2_broadcaster.cpp -o static_turtle_tf2_broadcaster.cpp

      或者在 powershell 中：

      .. code-block:: console

          $ curl https://raw.githubusercontent.com/ros/geometry_tutorials/{DISTRO}/turtle_tf2_cpp/src/static_turtle_tf2_broadcaster.cpp -o static_turtle_tf2_broadcaster.cpp

使用你喜欢的文本编辑器打开该文件。

.. code-block:: C++

    #include <memory>

    #include "geometry_msgs/msg/transform_stamped.hpp"
    #include "rclcpp/rclcpp.hpp"
    #include "tf2/LinearMath/Quaternion.hpp"
    #include "tf2_ros/static_transform_broadcaster.hpp"

    class StaticFramePublisher : public rclcpp::Node
    {
    public:
      explicit StaticFramePublisher(char * transformation[])
      : Node("static_turtle_tf2_broadcaster")
      {
        tf_static_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

        // Publish static transforms once at startup
        this->make_transforms(transformation);
      }

    private:
      void make_transforms(char * transformation[])
      {
        geometry_msgs::msg::TransformStamped t;

        t.header.stamp = this->get_clock()->now();
        t.header.frame_id = "world";
        t.child_frame_id = transformation[1];

        t.transform.translation.x = atof(transformation[2]);
        t.transform.translation.y = atof(transformation[3]);
        t.transform.translation.z = atof(transformation[4]);
        tf2::Quaternion q;
        q.setRPY(
          atof(transformation[5]),
          atof(transformation[6]),
          atof(transformation[7]));
        t.transform.rotation.x = q.x();
        t.transform.rotation.y = q.y();
        t.transform.rotation.z = q.z();
        t.transform.rotation.w = q.w();

        tf_static_broadcaster_->sendTransform(t);
      }

      std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_static_broadcaster_;
    };

    int main(int argc, char * argv[])
    {
      auto logger = rclcpp::get_logger("logger");

      // Obtain parameters from command line arguments
      if (argc != 8) {
        RCLCPP_INFO(
          logger, "Invalid number of parameters\nusage: "
          "$ ros2 run learning_tf2_cpp static_turtle_tf2_broadcaster "
          "child_frame_name x y z roll pitch yaw");
        return 1;
      }

      // As the parent frame of the transform is `world`, it is
      // necessary to check that the frame name passed is different
      if (strcmp(argv[1], "world") == 0) {
        RCLCPP_INFO(logger, "Your static turtle name cannot be 'world'");
        return 1;
      }

      // Pass parameters and initialize node
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<StaticFramePublisher>(argv));
      rclcpp::shutdown();
      return 0;
    }

2.1 检查代码
~~~~~~~~~~~~

现在让我们看看与将静态 turtle 位姿发布到 tf2 相关的代码。
第一行包含所需的头文件。
首先我们包含 ``geometry_msgs/msg/transform_stamped.hpp`` 以访问 ``TransformStamped`` 消息类型，我们将把它发布到变换树。

.. code-block:: C++

    #include "geometry_msgs/msg/transform_stamped.hpp"

随后，包含 ``rclcpp``，以便使用它的 ``rclcpp::Node`` 类。

.. code-block:: C++

    #include "rclcpp/rclcpp.hpp"

``tf2::Quaternion`` 是一个四元数类，提供了方便的函数来将欧拉角转换为四元数，反之亦然。
我们还包含 ``tf2_ros/static_transform_broadcaster.h`` 以使用 ``StaticTransformBroadcaster``，使静态变换的发布变得容易。

.. code-block:: C++

    #include "tf2/LinearMath/Quaternion.hpp"
    #include "tf2_ros/static_transform_broadcaster.hpp"

``StaticFramePublisher`` 类构造函数用名称 ``static_turtle_tf2_broadcaster`` 初始化节点。
然后，创建 ``StaticTransformBroadcaster``，它将在启动时发送一个静态变换。

.. code-block:: C++

    tf_static_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    this->make_transforms(transformation);

这里我们创建一个 ``TransformStamped`` 对象，它将是填充后我们要发送的消息。
在传入实际变换值之前，我们需要给它适当的元数据。

#. 我们需要给要发布的变换一个时间戳，我们只用当前时间 ``this->get_clock()->now()`` 来标记它。

#. 然后我们需要设置我们正在创建的链接的父帧名称，在本例中是 ``world``。

#. 最后，我们需要设置我们正在创建的链接的子帧名称。

.. code-block:: C++

    geometry_msgs::msg::TransformStamped t;

    t.header.stamp = this->get_clock()->now();
    t.header.frame_id = "world";
    t.child_frame_id = transformation[1];

这里我们填充 turtle 的 6D 位姿（平移和旋转）。

.. code-block:: C++

    t.transform.translation.x = atof(transformation[2]);
    t.transform.translation.y = atof(transformation[3]);
    t.transform.translation.z = atof(transformation[4]);
    tf2::Quaternion q;
    q.setRPY(
      atof(transformation[5]),
      atof(transformation[6]),
      atof(transformation[7]));
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();

最后，我们使用 ``sendTransform()`` 函数广播静态变换。

.. code-block:: C++

    tf_static_broadcaster_->sendTransform(t);

2.2 更新 package.xml
~~~~~~~~~~~~~~~~~~~~

向上导航一级到 ``src/learning_tf2_cpp`` 目录，那里已经为你创建了 ``CMakeLists.txt`` 和 ``package.xml`` 文件。

用你的文本编辑器打开 ``package.xml``。

如 :doc:`创建包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>` 教程所述，确保填写 ``<description>``、``<maintainer>`` 和 ``<license>`` 标签：

.. code-block:: xml

    <description>Learning tf2 with rclcpp</description>
    <maintainer email="you@email.com">Your Name</maintainer>
    <license>Apache-2.0</license>

确保保存文件。

2.3 CMakeLists.txt
~~~~~~~~~~~~~~~~~~

将可执行文件添加到 CMakeLists.txt 并命名为 ``static_turtle_tf2_broadcaster``，你稍后将用 ``ros2 run`` 使用它。

.. code-block:: console

    add_executable(static_turtle_tf2_broadcaster src/static_turtle_tf2_broadcaster.cpp)
    ament_target_dependencies(
       static_turtle_tf2_broadcaster
       geometry_msgs
       rclcpp
       tf2
       tf2_ros
    )

最后，添加 ``install(TARGETS…)`` 部分，以便 ``ros2 run`` 能找到你的可执行文件：

.. code-block:: console

    install(TARGETS
       static_turtle_tf2_broadcaster
       DESTINATION lib/${PROJECT_NAME})

3 构建
^^^^^^

在构建之前，最好在工作区根目录运行 ``rosdep`` 检查缺少的依赖：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

          $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

      rosdep 仅在 Linux 上运行，因此你需要自己安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖

   .. group-tab:: Windows

      rosdep 仅在 Linux 上运行，因此你需要自己安装 ``geometry_msgs`` 和 ``turtlesim`` 依赖

仍然在工作区根目录，构建你的新包：

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

现在运行 ``static_turtle_tf2_broadcaster`` 节点：

.. code-block:: console

    $ ros2 run learning_tf2_cpp static_turtle_tf2_broadcaster mystaticturtle 0 0 1 0 0 0

这将为 ``mystaticturtle`` 设置一个 turtle 位姿广播，让它浮在地面上方 1 米处。

我们现在可以通过回显 ``tf_static`` 话题来检查静态变换是否已发布。
如果一切正常，你应该看到一个静态变换：

.. code-block:: console

    $ ros2 topic echo /tf_static
    transforms:
    - header:
       stamp:
          sec: 1622908754
          nanosec: 208515730
       frame_id: world
    child_frame_id: mystaticturtle
    transform:
       translation:
          x: 0.0
          y: 0.0
          z: 1.0
       rotation:
          x: 0.0
          y: 0.0
          z: 0.0
          w: 1.0

发布静态变换的正确方式
----------------------

本教程旨在展示如何使用 ``StaticTransformBroadcaster`` 发布静态变换。
在你实际的开发过程中，你不应该自己编写这些代码，而应使用专用的 ``tf2_ros`` 工具来完成。
``tf2_ros`` 提供了一个名为 ``static_transform_publisher`` 的可执行文件，既可以作为命令行工具使用，也可以作为可以添加到启动文件中的节点使用。

以下命令向 tf2 发布一个静态坐标变换，结果是在 ``world`` 和 ``mystaticturtle`` 两个帧之间产生 1 米的 z 偏移且无旋转。
在 ROS 2 中，roll/pitch/yaw 分别指绕 x/y/z 轴的旋转。

.. code-block:: console

    $ ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --yaw 0 --pitch 0 --roll 0 --frame-id world --child-frame-id mystaticturtle

以下命令向 tf2 发布相同的静态坐标变换，但旋转使用四元数表示。

.. code-block:: console

    $ ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --qx 0 --qy 0 --qz 0 --qw 1 --frame-id world --child-frame-id mystaticturtle

``static_transform_publisher`` 既被设计为手动使用的命令行工具，也被设计为可在 ``launch`` 文件中用于设置静态变换。
例如：

.. tabs::

   .. group-tab:: XML

      .. literalinclude:: launch/static_transform_publisher_launch.xml
         :language: xml

   .. group-tab:: YAML

      .. literalinclude:: launch/static_transform_publisher_launch.yaml
         :language: yaml

   .. group-tab:: Python

      .. literalinclude:: launch/static_transform_publisher_launch.py
         :language: python

注意，除 ``--frame-id`` 和 ``--child-frame-id`` 外，所有参数都是可选的；如果没有指定某个选项，则将假定为单位值。

总结
----

在本教程中，你学习了静态变换对于定义帧之间的静态关系（如 ``mystaticturtle`` 相对于 ``world`` 帧）是多么有用。
此外，你还学习了静态变换如何通过将传感器数据（如激光扫描仪的数据）关联到公共坐标帧来帮助理解这些数据。
最后，你编写了自己的节点来向 tf2 发布静态变换，并学习了如何使用 ``static_transform_publisher`` 可执行文件和启动文件发布所需的静态变换。
