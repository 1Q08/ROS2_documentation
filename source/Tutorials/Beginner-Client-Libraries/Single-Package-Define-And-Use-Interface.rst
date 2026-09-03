.. _SinglePkgInterface:

.. redirect-from::

    Rosidl-Tutorial
    Tutorials/Single-Package-Define-And-Use-Interface

实现自定义接口
==============

**目标：** 学习在 ROS 2 中实现自定义接口的更多方式。

**教程级别：** 入门

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在 :doc:`之前的教程 <./Custom-ROS2-Interfaces>` 中，你学习了如何创建自定义的 msg 和 srv 接口。

虽然最佳实践是在专门的接口包中声明接口，但有时在一个包中声明、创建和使用接口会很方便。

回想一下，接口目前只能在 CMake 包中定义。
不过，可以在 CMake 包中拥有 Python 库和节点（使用 `ament_cmake_python <https://github.com/ament/ament_cmake/tree/{REPOS_FILE_BRANCH}/ament_cmake_python>`_），因此你可以在一个包中同时定义接口和 Python 节点。
为了简单起见，这里我们将使用 CMake 包和 C++ 节点。

本教程将重点关注 msg 接口类型，但这里的步骤适用于所有接口类型。

前置条件
--------

我们假设你在学习本教程之前已经复习了 :doc:`./Custom-ROS2-Interfaces` 教程中的基础知识。

你应该已经 :doc:`安装了 ROS 2 <../../Installation>`，有一个 :doc:`工作空间 <./Creating-A-Workspace/Creating-A-Workspace>`，并且理解了 :doc:`创建包 <./Creating-Your-First-ROS2-Package>`。

一如既往，不要忘记在每个新打开的终端中 :doc:`source ROS 2 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`。

任务
----

1 创建一个包
^^^^^^^^^^^^

在你的工作空间 ``src`` 目录中，创建一个包 ``more_interfaces``，并在其中为 msg 文件创建一个目录：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 more_interfaces
  $ mkdir more_interfaces/msg

2 创建一个 msg 文件
^^^^^^^^^^^^^^^^^^^

在 ``more_interfaces/msg`` 中，创建一个新文件 ``AddressBook.msg``，并粘贴以下代码，以创建一个用于携带个人信息的消息：

::

   uint8 PHONE_TYPE_HOME=0
   uint8 PHONE_TYPE_WORK=1
   uint8 PHONE_TYPE_MOBILE=2

   string first_name
   string last_name
   string phone_number
   uint8 phone_type

此消息由以下字段组成：

* first_name：string 类型
* last_name：string 类型
* phone_number：string 类型
* phone_type：uint8 类型，定义了几个具名常量值

请注意，可以在消息定义中为字段设置默认值。
参见 :doc:`../../Concepts/Basic/About-Interfaces` 了解自定义接口的更多方式。

接下来，我们需要确保 msg 文件被转换成 C++、Python 和其他语言的源代码。

2.1 构建一个 msg 文件
~~~~~~~~~~~~~~~~~~~~~

打开 ``package.xml`` 并添加以下行：

.. code-block:: xml

     <buildtool_depend>rosidl_default_generators</buildtool_depend>

     <exec_depend>rosidl_default_runtime</exec_depend>

     <member_of_group>rosidl_interface_packages</member_of_group>

请注意，在构建时需要 ``rosidl_default_generators``，而在运行时只需要 ``rosidl_default_runtime``。

打开 ``CMakeLists.txt`` 并添加以下行：

找到从 msg/srv 文件生成消息代码的包：

.. code-block:: cmake

   find_package(rosidl_default_generators REQUIRED)

声明你想要生成的消息列表：

.. code-block:: cmake

   set(msg_files
     "msg/AddressBook.msg"
   )

通过手动添加 .msg 文件，我们确保在添加其他 .msg 文件后，CMake 知道何时必须重新配置项目。

生成消息：

.. code-block:: cmake

   rosidl_generate_interfaces(${PROJECT_NAME}
     ${msg_files}
   )

还要确保导出消息运行时依赖：

.. code-block:: cmake

   ament_export_dependencies(rosidl_default_runtime)

现在你已准备好从 msg 定义生成源文件。
我们暂时跳过编译步骤，因为稍后会在步骤 4 中一起完成。

3 从同一个包中使用接口
^^^^^^^^^^^^^^^^^^^^^^

现在我们可以开始编写使用此消息的代码了。

在 ``more_interfaces/src`` 中创建一个名为 ``publish_address_book.cpp`` 的文件，并粘贴以下代码：

.. code-block:: c++

  #include <chrono>
  #include <memory>

  #include "rclcpp/rclcpp.hpp"
  #include "more_interfaces/msg/address_book.hpp"

  using namespace std::chrono_literals;

  class AddressBookPublisher : public rclcpp::Node
  {
  public:
    AddressBookPublisher()
    : Node("address_book_publisher")
    {
      address_book_publisher_ =
        this->create_publisher<more_interfaces::msg::AddressBook>("address_book", 10);

      auto publish_msg = [this]() -> void {
          auto message = more_interfaces::msg::AddressBook();

          message.first_name = "John";
          message.last_name = "Doe";
          message.phone_number = "1234567890";
          message.phone_type = message.PHONE_TYPE_MOBILE;

          std::cout << "Publishing Contact\nFirst:" << message.first_name <<
            "  Last:" << message.last_name << std::endl;

          this->address_book_publisher_->publish(message);
        };
      timer_ = this->create_wall_timer(1s, publish_msg);
    }

  private:
    rclcpp::Publisher<more_interfaces::msg::AddressBook>::SharedPtr address_book_publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
  };


  int main(int argc, char * argv[])
  {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<AddressBookPublisher>());
    rclcpp::shutdown();

    return 0;
  }

3.1 代码解释
~~~~~~~~~~~~

包含我们新建的 ``AddressBook.msg`` 的头文件。

.. code-block:: c++

   #include "more_interfaces/msg/address_book.hpp"

创建一个节点和一个 ``AddressBook`` 发布者。

.. code-block:: c++

   using namespace std::chrono_literals;

   class AddressBookPublisher : public rclcpp::Node
   {
   public:
     AddressBookPublisher()
     : Node("address_book_publisher")
     {
       address_book_publisher_ =
         this->create_publisher<more_interfaces::msg::AddressBook>("address_book");

创建一个回调以定期发布消息。

.. code-block:: c++

    auto publish_msg = [this]() -> void {

创建一个稍后将发布的 ``AddressBook`` 消息实例。

.. code-block:: c++

    auto message = more_interfaces::msg::AddressBook();

填充 ``AddressBook`` 字段。

.. code-block:: c++

    message.first_name = "John";
    message.last_name = "Doe";
    message.phone_number = "1234567890";
    message.phone_type = message.PHONE_TYPE_MOBILE;

最后定期发送消息。

.. code-block:: c++

    std::cout << "Publishing Contact\nFirst:" << message.first_name <<
      "  Last:" << message.last_name << std::endl;

    this->address_book_publisher_->publish(message);

创建一个 1 秒的定时器，每秒调用一次我们的 ``publish_msg`` 函数。

.. code-block:: c++

       timer_ = this->create_wall_timer(1s, publish_msg);

3.2 构建发布者
~~~~~~~~~~~~~~

我们需要在 ``CMakeLists.txt`` 中为这个节点创建一个新的目标：

.. code-block:: cmake

   find_package(rclcpp REQUIRED)

   add_executable(publish_address_book src/publish_address_book.cpp)
   ament_target_dependencies(publish_address_book rclcpp)

   install(TARGETS
       publish_address_book
     DESTINATION lib/${PROJECT_NAME})

3.3 链接到接口
~~~~~~~~~~~~~~

为了使用在同一包中生成的消息，我们需要使用以下 CMake 代码：

.. code-block:: cmake

  rosidl_get_typesupport_target(cpp_typesupport_target
    ${PROJECT_NAME} rosidl_typesupport_cpp)

  target_link_libraries(publish_address_book "${cpp_typesupport_target}")

这会从 ``AddressBook.msg`` 找到相关的已生成 C++ 代码，并允许你的目标链接到它。

你可能已经注意到，当使用的接口来自独立构建的不同包时，这一步是不必要的。
只有在你想在定义接口的同一个包中使用接口时，才需要这段 CMake 代码。

4 试一试
^^^^^^^^

返回到工作空间的根目录来构建该包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ cd ~/ros2_ws
      $ colcon build --packages-up-to more_interfaces

  .. group-tab:: macOS

    .. code-block:: console

      $ cd ~/ros2_ws
      $ colcon build --packages-up-to more_interfaces

  .. group-tab:: Windows

    .. code-block:: console

      $ cd /ros2_ws
      $ colcon build --merge-install --packages-up-to more_interfaces

然后 source 工作空间并运行发布者：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/local_setup.bash
      $ ros2 run more_interfaces publish_address_book

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/local_setup.bash
      $ ros2 run more_interfaces publish_address_book

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/local_setup.bat
      $ ros2 run more_interfaces publish_address_book

    或者使用 Powershell：

    .. code-block:: console

      $ install/local_setup.ps1
      $ ros2 run more_interfaces publish_address_book

你应该会看到发布者中继了你定义的 msg，包括你在 ``publish_address_book.cpp`` 中设置的值。

要确认消息正在 ``address_book`` 话题上发布，打开另一个终端，source 工作空间，然后调用 ``topic echo``：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash
      $ ros2 topic echo /address_book

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash
      $ ros2 topic echo /address_book

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat
      $ ros2 topic echo /address_book

    或者使用 Powershell：

    .. code-block:: console

      $ install/setup.ps1
      $ ros2 topic echo /address_book

在本教程中我们不会创建订阅者，但你可以尝试自己编写一个作为练习（可以借助 :doc:`./Writing-A-Simple-Cpp-Publisher-And-Subscriber`）。

5 （额外）使用已有的接口定义
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

  你可以在新的接口定义中使用已有的接口定义。
  例如，假设有一个名为 ``Contact.msg`` 的消息，它属于一个名为 ``rosidl_tutorials_msgs`` 的现有 ROS 2 包。
  假设它的定义与我们之前自定义的 ``AddressBook.msg`` 接口完全相同。

  在这种情况下，你可以把 ``AddressBook.msg``\ （*你的*\ 节点所在包中的一个接口）定义为类型 ``Contact``\ （一个\ *独立*\ 包中的接口）。
  你甚至可以将 ``AddressBook.msg`` 定义为类型 ``Contact`` 的\ *数组*，像这样：

  ::

     rosidl_tutorials_msgs/Contact[] address_book

  要生成此消息，你需要在 ``package.xml`` 中声明对 ``Contact.msg`` 的包 ``rosidl_tutorials_msgs`` 的依赖：

  .. code-block:: xml

       <build_depend>rosidl_tutorials_msgs</build_depend>

       <exec_depend>rosidl_tutorials_msgs</exec_depend>

  并且在 ``CMakeLists.txt`` 中：

  .. code-block:: cmake

     find_package(rosidl_tutorials_msgs REQUIRED)

     rosidl_generate_interfaces(${PROJECT_NAME}
       ${msg_files}
       DEPENDENCIES rosidl_tutorials_msgs
     )

  你还需要在发布者节点中包含 ``Contact.msg`` 的头文件，以便能够将 ``contacts`` 添加到你的 ``address_book`` 中。

  .. code-block:: c++

     #include "rosidl_tutorials_msgs/msg/contact.hpp"

  你可以将回调改成类似这样的代码：

  .. code-block:: c++

    auto publish_msg = [this]() -> void {
       auto msg = std::make_shared<more_interfaces::msg::AddressBook>();
       {
         rosidl_tutorials_msgs::msg::Contact contact;
         contact.first_name = "John";
         contact.last_name = "Doe";
         contact.phone_number = "1234567890";
         contact.phone_type = contact.PHONE_TYPE_MOBILE;
         msg->address_book.push_back(contact);
       }
       {
         rosidl_tutorials_msgs::msg::Contact contact;
         contact.first_name = "Jane";
         contact.last_name = "Doe";
         contact.phone_number = "4254242424";
         contact.phone_type = contact.PHONE_TYPE_HOME;
         msg->address_book.push_back(contact);
       }

       std::cout << "Publishing address book:" << std::endl;
       for (auto contact : msg->address_book) {
         std::cout << "First:" << contact.first_name << "  Last:" << contact.last_name <<
           std::endl;
       }

       address_book_publisher_->publish(*msg);
     };

  构建并运行这些更改后，将显示按预期定义的 msg，以及上面定义的 msg 数组。

总结
----

在本教程中，你尝试了定义接口的不同字段类型，然后在正在使用它的同一个包中构建了一个接口。

你还学习了如何使用另一个接口作为字段类型，以及使用该功能所需的 ``package.xml``、``CMakeLists.txt`` 和 ``#include`` 语句。

后续步骤
--------

接下来，你将创建一个简单的 ROS 2 包，其中包含一个自定义参数，你将学习如何从 launch 文件设置它。
同样，你可以选择用 :doc:`C++ <./Using-Parameters-In-A-Class-CPP>` 或 :doc:`Python <./Using-Parameters-In-A-Class-Python>` 来编写它。

相关内容
--------

关于 ROS 2 接口和 IDL（接口定义语言），有 `几篇设计文章 <https://design.ros2.org/#interfaces>`_。
