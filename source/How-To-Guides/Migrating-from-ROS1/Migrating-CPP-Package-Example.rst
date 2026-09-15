迁移 C++ 软件包示例
===================

.. contents:: 目录
   :depth: 2
   :local:

本示例演示如何把一个示例 C++ 软件包从 ROS 1 迁移到 ROS 2。

前提条件
--------

你需要一个可用的 ROS 2 安装环境，例如 :doc:`ROS {DISTRO} <../../Installation>`。

ROS 1 代码
----------

假设你有一个名为 ``talker`` 的 ROS 1 软件包，它在一个名为 ``talker`` 的节点中使用了 ``roscpp``。
该软件包位于一个 catkin 工作空间中，路径为 ``~/ros1_talker``。

你的 ROS 1 工作空间具有以下目录结构：

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

``src/talker/package.xml``:

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

``src/talker/CMakeLists.txt``:

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

``src/talker/talker.cpp``:

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

我们先创建一个新的工作空间来开展迁移工作：

.. code-block:: console

   $ mkdir ~/ros2_talker
   $ cd ~/ros2_talker

把 ROS 1 软件包的源码树复制到该工作空间中，然后在其中进行修改：

.. code-block:: console

   $ mkdir src
   $ cp -a ~/ros1_talker/src/talker src

现在我们修改节点中的 C++ 代码。
ROS 2 的 C++ 库名为 ``rclcpp``，它提供的 API 与 ``roscpp`` 不同。
两个库的概念非常相似，因此这些改动实现起来相当直接。

包含的头文件
~~~~~~~~~~~~

``ros/ros.h`` 让我们可以使用 ``roscpp`` 库的 API，
现在需要改为包含 ``rclcpp/rclcpp.hpp``，它让我们可以使用 ``rclcpp`` 库的 API：

.. code-block:: cpp

   //#include "ros/ros.h"
   #include "rclcpp/rclcpp.hpp"

要获得 ``std_msgs/String`` 消息定义，需要把 ``std_msgs/String.h``
替换为包含 ``std_msgs/msg/string.hpp``：

.. code-block:: cpp

   //#include "std_msgs/String.h"
   #include "std_msgs/msg/string.hpp"

修改 C++ 库调用
~~~~~~~~~~~~~~~

不再把节点名称传给库的初始化调用，而是先做初始化，
再把节点名称传给节点对象的创建：

.. code-block:: cpp

   //  ros::init(argc, argv, "talker");
   //  ros::NodeHandle n;
       rclcpp::init(argc, argv);
       auto node = rclcpp::Node::make_shared("talker");

发布者对象和频率对象的创建看起来非常相似，只是命名空间和方法的名称有一些变化。

.. code-block:: cpp

   //  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
   //  ros::Rate loop_rate(10);
     auto chatter_pub = node->create_publisher<std_msgs::msg::String>("chatter",
       1000);
     rclcpp::Rate loop_rate(10);

要进一步控制消息的传递方式，可以传入一个服务质量（``QoS``）配置文件。
默认配置文件是 ``rmw_qos_profile_default``。
更多细节请参阅
`设计文档 <https://design.ros2.org/articles/qos.html>`__
和 :doc:`概念概述 <../../Concepts/Intermediate/About-Quality-of-Service-Settings>`。

待发送消息的创建在命名空间上有所不同：

.. code-block:: cpp

   //  std_msgs::String msg;
     std_msgs::msg::String msg;

把 ``ros::ok()`` 替换为调用 ``rclcpp::ok()``：

.. code-block:: cpp

   //  while (ros::ok())
     while (rclcpp::ok())

在发布循环内部，访问 ``data`` 字段的方式与之前相同：

.. code-block:: cpp

       msg.data = ss.str();

要打印控制台消息，不再使用 ``ROS_INFO()``，而是使用
``RCLCPP_INFO()`` 及其各种同类宏。
关键区别在于 ``RCLCPP_INFO()`` 需要一个 Logger 对象作为第一个参数。

.. code-block:: cpp

   //    ROS_INFO("%s", msg.data.c_str());
       RCLCPP_INFO(node->get_logger(), "%s\n", msg.data.c_str());

把发布调用改为使用 ``->`` 运算符而不是 ``.``。

.. code-block:: cpp

   //    chatter_pub.publish(msg);
       chatter_pub->publish(msg);

自旋（即让通信系统处理所有待处理的收发消息，直到没有更多工作可做）有所不同，
区别在于该调用现在把节点和超时时间作为参数：

.. code-block:: cpp

   //    ros::spinOnce();
       rclcpp::spin_all(node, 0s);

使用频率对象休眠的方式没有变化。

综合以上改动，新的 ``talker.cpp`` 如下：

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

修改 ``package.xml``
~~~~~~~~~~~~~~~~~~~~

ROS 2 软件包使用来自 ``ament_cmake_ros`` 的 CMake 函数和宏，而不是 ``catkin``。
删除对 ``catkin`` 的依赖：

.. code-block::

   <!-- delete this -->
   <buildtool_depend>catkin</buildtool_depend>`

添加对 ``ament_cmake_ros`` 的新依赖：

.. code-block:: xml

     <buildtool_depend>ament_cmake_ros</buildtool_depend>

ROS 2 的 C++ 库使用 `rclcpp <https://index.ros.org/p/rclcpp/#{DISTRO}>`__，而不是 `roscpp <https://index.ros.org/p/roscpp/#noetic>`__。

删除对 ``roscpp`` 的依赖：

.. code-block::

   <!-- delete this -->
   <depend>roscpp</depend>

添加对 ``rclcpp`` 的依赖：

.. code-block:: xml

     <depend>rclcpp</depend>


添加一个 ``<export>`` 小节，告诉 colcon 该软件包是 ``ament_cmake`` 软件包，而不是 ``catkin`` 软件包。

.. code-block:: xml

     <export>
       <build_type>ament_cmake</build_type>
     </export>

现在你的 ``package.xml`` 如下：

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


修改 CMake 代码
~~~~~~~~~~~~~~~

要求使用更新版本的 CMake，以便 ``ament_cmake`` 的函数能正确工作。

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.14.4)

使用更新的 C++ 标准，与 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`__ 中你的目标 ROS 发行版所用的版本保持一致。
如果你使用 C++17，则在 ``project(talker)`` 调用之后用下面的片段设置该版本。
同时添加额外的编译器检查，这是一个好习惯。

.. code-block:: cmake

   if(NOT CMAKE_CXX_STANDARD)
     set(CMAKE_CXX_STANDARD 17)
   endif()
   if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
     add_compile_options(-Wall -Wextra -Wpedantic)
   endif()

把 ``find_package(catkin ...)`` 调用替换为针对每个依赖项单独调用。

.. code-block:: cmake

   find_package(ament_cmake REQUIRED)
   find_package(rclcpp REQUIRED)
   find_package(std_msgs REQUIRED)

删除对 ``catkin_package()`` 的调用。
在 ``CMakeLists.txt`` 的末尾添加对 ``ament_package()`` 的调用。

.. code-block:: cmake

   ament_package()

让 ``target_link_libraries`` 调用 ``rclcpp`` 和 ``std_msgs`` 提供的现代 CMake 目标。

.. code-block:: cmake

   target_link_libraries(talker PUBLIC
     rclcpp::rclcpp
     ${std_msgs_TARGETS})

删除对 ``include_directories()`` 的调用。
在 ``add_executable(talker talker.cpp)`` 下方添加对 ``target_include_directories()`` 的调用。
不要把 ``rclcpp_INCLUDE_DIRS`` 之类的变量传给 ``target_include_directories()``。
使用现代 CMake 目标调用 ``target_link_libraries()`` 时，包含目录已经处理好了。

.. code-block:: cmake

   target_include_directories(talker PUBLIC
      "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
      "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>")

修改 ``install()`` 调用，把 ``talker`` 可执行文件安装到项目专属目录中。

.. code-block:: cmake

   install(TARGETS talker
     DESTINATION lib/${PROJECT_NAME})

新的 ``CMakeLists.txt`` 如下：

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

我们先 source 一个环境配置脚本（这里是按照 ROS 2 安装教程生成的脚本，构建目录为 ``~/ros2_ws``），
然后用 ``colcon build`` 构建我们的软件包：

.. code-block:: console

   $ . ~/ros2_ws/install/setup.bash
   $ cd ~/ros2_talker
   $ colcon build

运行 ROS 2 节点
~~~~~~~~~~~~~~~

由于我们把 ``talker`` 可执行文件安装到了正确的目录，在 source 配置脚本之后，
就可以从安装目录树中这样调用它：

.. code-block:: console

   $ . ~/ros2_ws/install/setup.bash
   $ ros2 run talker talker

总结
----

你已经学会了如何把一个示例 C++ ROS 1 软件包迁移到 ROS 2。
可以使用 :doc:`迁移 C++ 软件包参考页 <./Migrating-CPP-Packages>` 来帮助你把自己的 C++ 软件包从 ROS 1 迁移到 ROS 2。
