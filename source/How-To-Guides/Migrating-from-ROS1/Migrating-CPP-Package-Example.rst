迁移 C++ 包示例
===============

.. contents:: 目录
   :depth: 2
   :local:

本示例展示如何将一个示例 C++ 包从 ROS 1 迁移到 ROS 2。

前提条件
--------

你需要一个可用的 ROS 2 安装，例如 :doc:`ROS {DISTRO} <../../Installation>`。

ROS 1 代码
----------

假设你有一个名为 ``talker`` 的 ROS 1 包，它在一个名为 ``talker`` 的节点中使用 ``roscpp``。
这个包位于一个 catkin 工作空间中，位置在 ``~/ros1_talker``。

你的 ROS 1 工作空间具有以下目录布局：

.. code-block:: console

   $ cd ~/ros1_talker
   $ find .
   .
   ./src
   ./src/talker
   ./src/talker/package.xml
   ./src/talker/CMakeLists.txt
   ./src/talker/talker.cpp

这些文件的内容如下：

``src/talker/package.xml``：

.. code-block:: xml

   <?xml version="1.0"?>
   <?xml-model href="http://download.ros.org/schema/package_format2.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
   <package format="2">
     <name>talker</name>
     <version>0.0.0</version>
     <description>talker</description>
     <maintainer email="gerkey@example.com">Brian Gerkey</maintainer>
     <license>Apache-2.0</license>
     <buildtool_depend>catkin</buildtool_depend>
     <depend>roscpp</depend>
     <depend>std_msgs</depend>
   </package>

``src/talker/CMakeLists.txt``：

.. code-block:: cmake

   cmake_minimum_required(VERSION 2.8.3)
   project(talker)
   find_package(catkin REQUIRED COMPONENTS roscpp std_msgs)
   catkin_package()
   include_directories(${catkin_INCLUDE_DIRS})
   add_executable(talker talker.cpp)
   target_link_libraries(talker ${catkin_LIBRARIES})
   install(TARGETS talker
     RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

``src/talker/talker.cpp``：

.. code-block:: cpp

   #include <sstream>
   #include "ros/ros.h"
   #include "std_msgs/String.h"
   int main(int argc, char **argv)
   {
     ros::init(argc, argv, "talker");
     ros::NodeHandle n;
     ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
     ros::Rate loop_rate(10);
     int count = 0;
     std_msgs::String msg;
     while (ros::ok())
     {
       std::stringstream ss;
       ss << "hello world " << count++;
       msg.data = ss.str();
       ROS_INFO("%s", msg.data.c_str());
       chatter_pub.publish(msg);
       ros::spinOnce();
       loop_rate.sleep();
     }
     return 0;
   }

迁移到 ROS 2
------------

首先创建一个新的工作空间来工作：

.. code-block:: console

   $ mkdir ~/ros2_talker
   $ cd ~/ros2_talker

我们将 ROS 1 包的源代码树复制到该工作空间中，以便对其进行修改：

.. code-block:: console

   $ mkdir src
   $ cp -a ~/ros1_talker/src/talker src

现在我们修改节点中的 C++ 代码。
ROS 2 C++ 库（称为 ``rclcpp``）提供的 API 与 ``roscpp`` 提供的不同。
这两个库的概念非常相似，这使得这些更改相当容易完成。

包含的头文件
~~~~~~~~~~~~

我们需要包含 ``rclcpp/rclcpp.hpp`` 来替代 ``ros/ros.h``\ （它让我们能够访问 ``roscpp`` 库 API），从而访问 ``rclcpp`` 库 API：

.. code-block:: cpp

   //#include "ros/ros.h"
   #include "rclcpp/rclcpp.hpp"

要获取 ``std_msgs/String`` 消息定义，我们需要包含 ``std_msgs/msg/string.hpp`` 来替代 ``std_msgs/String.h``：

.. code-block:: cpp

   //#include "std_msgs/String.h"
   #include "std_msgs/msg/string.hpp"

更改 C++ 库调用
~~~~~~~~~~~~~~~

我们不再将节点名称传递给库初始化调用，而是先进行初始化，然后将节点名称传递给节点对象的创建：

.. code-block:: cpp

   //  ros::init(argc, argv, "talker");
   //  ros::NodeHandle n;
       rclcpp::init(argc, argv);
       auto node = rclcpp::Node::make_shared("talker");

发布者和 rate 对象的创建看起来非常相似，只是命名空间和方法的名称有一些变化。

.. code-block:: cpp

   //  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
   //  ros::Rate loop_rate(10);
     auto chatter_pub = node->create_publisher<std_msgs::msg::String>("chatter",
       1000);
     rclcpp::Rate loop_rate(10);

为了进一步控制消息传递的处理方式，可以传入一个服务质量（``QoS``）配置文件。
默认配置文件是 ``rmw_qos_profile_default``。
更多详细信息请参见
`设计文档 <https://design.ros2.org/articles/qos.html>`__
和 :doc:`概念概述 <../../Concepts/Intermediate/About-Quality-of-Service-Settings>`。

传出消息的创建在命名空间上有所不同：

.. code-block:: cpp

   //  std_msgs::String msg;
     std_msgs::msg::String msg;

我们用 ``rclcpp::ok()`` 来替代 ``ros::ok()``：

.. code-block:: cpp

   //  while (ros::ok())
     while (rclcpp::ok())

在发布循环内部，我们像以前一样访问 ``data`` 字段：

.. code-block:: cpp

       msg.data = ss.str();

要打印控制台消息，我们使用 ``RCLCPP_INFO()`` 及其各种变体来替代 ``ROS_INFO()``。
关键区别在于 ``RCLCPP_INFO()`` 的第一个参数是一个 Logger 对象。

.. code-block:: cpp

   //    ROS_INFO("%s", msg.data.c_str());
       RCLCPP_INFO(node->get_logger(), "%s\n", msg.data.c_str());

将发布调用更改为使用 ``->`` 运算符而不是 ``.``。

.. code-block:: cpp

   //    chatter_pub.publish(msg);
       chatter_pub->publish(msg);

Spinning（即让通信系统处理任何待处理的传入/传出消息，直到没有更多工作可用）有所不同，因为该调用现在将节点和超时作为参数：

.. code-block:: cpp

   //    ros::spinOnce();
       rclcpp::spin_all(node, 0s);

使用 rate 对象进行休眠保持不变。

把它们放在一起，新的 ``talker.cpp`` 看起来像这样：

.. code-block:: cpp

   #include <chrono>
   #include <sstream>
   // #include "ros/ros.h"
   #include "rclcpp/rclcpp.hpp"
   // #include "std_msgs/String.h"
   #include "std_msgs/msg/string.hpp"

   using namespace std::chrono_literals;

   int main(int argc, char **argv)
   {
   //  ros::init(argc, argv, "talker");
   //  ros::NodeHandle n;
     rclcpp::init(argc, argv);
     auto node = rclcpp::Node::make_shared("talker");
   //  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
   //  ros::Rate loop_rate(10);
     auto chatter_pub = node->create_publisher<std_msgs::msg::String>("chatter", 1000);
     rclcpp::Rate loop_rate(10);
     int count = 0;
   //  std_msgs::String msg;
     std_msgs::msg::String msg;
   //  while (ros::ok())
     while (rclcpp::ok())
     {
       std::stringstream ss;
       ss << "hello world " << count++;
       msg.data = ss.str();
   //    ROS_INFO("%s", msg.data.c_str());
       RCLCPP_INFO(node->get_logger(), "%s\n", msg.data.c_str());
   //    chatter_pub.publish(msg);
       chatter_pub->publish(msg);
   //    ros::spinOnce();
       rclcpp::spin_all(node, 0s);
       loop_rate.sleep();
     }
     return 0;
   }

更改 ``package.xml``
~~~~~~~~~~~~~~~~~~~~

ROS 2 包使用来自 ``ament_cmake_ros`` 的 CMake 函数和宏，而不是 ``catkin``。
删除对 ``catkin`` 的依赖：

.. code-block::

   <!-- 删除这一行 -->
   <buildtool_depend>catkin</buildtool_depend>`

添加对 ``ament_cmake_ros`` 的新依赖：

.. code-block:: xml

     <buildtool_depend>ament_cmake_ros</buildtool_depend>

ROS 2 C++ 库使用 `rclcpp <https://index.ros.org/p/rclcpp/#{DISTRO}>`__ 而不是 `roscpp <https://index.ros.org/p/roscpp/#noetic>`__。

删除对 ``roscpp`` 的依赖：

.. code-block::

   <!-- 删除这一行 -->
   <depend>roscpp</depend>

添加对 ``rclcpp`` 的依赖：

.. code-block:: xml

     <depend>rclcpp</depend>


添加一个 ``<export>`` 部分，告诉 colcon 该包是一个 ``ament_cmake`` 包，而不是 ``catkin`` 包。

.. code-block:: xml

     <export>
       <build_type>ament_cmake</build_type>
     </export>

你的 ``package.xml`` 现在看起来像这样：

.. code-block:: xml

   <?xml version="1.0"?>
   <?xml-model href="http://download.ros.org/schema/package_format2.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
   <package format="2">
     <name>talker</name>
     <version>0.0.0</version>
     <description>talker</description>
     <maintainer email="gerkey@example.com">Brian Gerkey</maintainer>
     <license>Apache-2.0</license>
     <buildtool_depend>ament_cmake</buildtool_depend>
     <depend>rclcpp</depend>
     <depend>std_msgs</depend>
     <export>
       <build_type>ament_cmake</build_type>
     </export>
   </package>


更改 CMake 代码
~~~~~~~~~~~~~~~

要求更新版本的 CMake，以便 ``ament_cmake`` 函数正常工作。

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.14.4)

使用与 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`__ 中目标 ROS 发行版所使用版本相匹配的更新 C++ 标准。
如果你使用 C++17，那么在 ``project(talker)`` 调用之后用以下代码片段设置该版本。
还要添加额外的编译器检查，因为这是一个好习惯。

.. code-block:: cmake

   if(NOT CMAKE_CXX_STANDARD)
     set(CMAKE_CXX_STANDARD 17)
   endif()
   if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
     add_compile_options(-Wall -Wextra -Wpedantic)
   endif()

将 ``find_package(catkin ...)`` 调用替换为针对每个依赖的单独调用。

.. code-block:: cmake

   find_package(ament_cmake REQUIRED)
   find_package(rclcpp REQUIRED)
   find_package(std_msgs REQUIRED)

删除对 ``catkin_package()`` 的调用。
在 ``CMakeLists.txt`` 的底部添加对 ``ament_package()`` 的调用。

.. code-block:: cmake

   ament_package()

将 ``target_link_libraries`` 调用改为使用 ``rclcpp`` 和 ``std_msgs`` 提供的现代 CMake 目标。

.. code-block:: cmake

   target_link_libraries(talker PUBLIC
     rclcpp::rclcpp
     ${std_msgs_TARGETS})

删除对 ``include_directories()`` 的调用。
在 ``add_executable(talker talker.cpp)`` 下面添加对 ``target_include_directories()`` 的调用。
不要将 ``rclcpp_INCLUDE_DIRS`` 之类的变量传入 ``target_include_directories()``。
包含目录已经通过使用现代 CMake 目标调用 ``target_link_libraries()`` 处理了。

.. code-block:: cmake

   target_include_directories(talker PUBLIC
      "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
      "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>")

更改对 ``install()`` 的调用，使 ``talker`` 可执行文件被安装到项目特定的目录中。

.. code-block:: cmake

   install(TARGETS talker
     DESTINATION lib/${PROJECT_NAME})

新的 ``CMakeLists.txt`` 看起来像这样：

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.14.4)
   project(talker)
   if(NOT CMAKE_CXX_STANDARD)
     set(CMAKE_CXX_STANDARD 17)
   endif()
   if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
     add_compile_options(-Wall -Wextra -Wpedantic)
   endif()
   find_package(ament_cmake REQUIRED)
   find_package(rclcpp REQUIRED)
   find_package(std_msgs REQUIRED)
   add_executable(talker talker.cpp)
   target_include_directories(talker PUBLIC
      "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
      "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>")
   target_link_libraries(talker PUBLIC
     rclcpp::rclcpp
     ${std_msgs_TARGETS})
   install(TARGETS talker
     DESTINATION lib/${PROJECT_NAME})
   ament_package()

构建 ROS 2 代码
~~~~~~~~~~~~~~~

我们 source 一个环境设置文件（在本例中，是由 ROS 2 安装教程生成的文件，它在 ``~/ros2_ws`` 中构建），然后使用 ``colcon build`` 构建我们的包：

.. code-block:: console

   $ . ~/ros2_ws/install/setup.bash
   $ cd ~/ros2_talker
   $ colcon build

运行 ROS 2 节点
~~~~~~~~~~~~~~~

因为我们将 ``talker`` 可执行文件安装到了正确的目录，所以在 source 设置文件之后，我们可以从安装树中通过以下命令调用它：

.. code-block:: console

   $ . ~/ros2_ws/install/setup.bash
   $ ros2 run talker talker

结论
----

你已经学会了如何将一个示例 C++ ROS 1 包迁移到 ROS 2。
使用 :doc:`迁移 C++ 包参考页 <./Migrating-CPP-Packages>` 来帮助你将自己的 C++ 包从 ROS 1 迁移到 ROS 2。
