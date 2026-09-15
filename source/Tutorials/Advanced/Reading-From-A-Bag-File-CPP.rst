从 bag 文件中读取（C++）
========================

**目标：** 不使用 CLI 从 bag 中读取数据。

**教程级别：** 高级

**预计用时：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``rosbag2`` 不仅仅提供 ``ros2 bag`` 命令行工具。
它还提供了一个 C++ API，用于从你自己的源代码中读取和写入 bag。
这允许你在不必播放 bag 的情况下读取其内容，这在某些情况下很有用。

前置条件
--------

你应该已经在常规的 ROS 2 安装中安装了 ``rosbag2`` 包。

如果你需要安装 ROS 2，请参阅 :doc:`安装说明 <../../Installation>`。

你应该已经完成了 :doc:`基础的 ROS 2 bag 教程 <../Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data>`，我们将使用你在那里创建的 ``subset`` bag。

任务
----

1 创建包
^^^^^^^^

打开一个新终端，并 :doc:`source 你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，使 ``ros2`` 命令能够正常工作。

在一个新的或已有的 :ref:`工作空间 <new-directory>` 中，导航到 ``src`` 目录并创建一个新包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 bag_reading_cpp --dependencies rclcpp rosbag2_transport turtlesim

你的终端将返回一条消息，确认包 ``bag_reading_cpp`` 及其所有必要文件和文件夹已创建。
``--dependencies`` 参数会自动将必要的依赖行添加到 ``package.xml`` 和 ``CMakeLists.txt``。
在这种情况下，该包将使用 ``rosbag2_transport`` 包和 ``rclcpp`` 包。
还需要依赖 ``turtlesim`` 包来处理自定义的 turtlesim 消息。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

由于你在创建包时使用了 ``--dependencies`` 选项，因此无需手动向 ``package.xml`` 或 ``CMakeLists.txt`` 添加依赖。
不过，和往常一样，请确保向 ``package.xml`` 添加描述、维护者邮箱和姓名以及许可证信息。

.. code-block:: xml

  <description>C++ bag reading tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

2 编写 C++ 读取器
^^^^^^^^^^^^^^^^^

在你的包的 ``src`` 目录中，创建一个名为 ``simple_bag_reader.cpp`` 的新文件，并将以下代码粘贴进去。

.. code-block:: C++

    #include <chrono>
    #include <functional>
    #include <iostream>
    #include <memory>
    #include <string>

    #include "rclcpp/rclcpp.hpp"
    #include "rclcpp/serialization.hpp"
    #include "rosbag2_transport/reader_writer_factory.hpp"
    #include "turtlesim/msg/pose.hpp"

    using namespace std::chrono_literals;

    class PlaybackNode : public rclcpp::Node
    {
      public:
        PlaybackNode(const std::string & bag_filename)
        : Node("playback_node")
        {
          publisher_ = this->create_publisher<turtlesim::msg::Pose>("/turtle1/pose", 10);

          timer_ = this->create_wall_timer(100ms,
              [this](){return this->timer_callback();}
          );

          rosbag2_storage::StorageOptions storage_options;
          storage_options.uri = bag_filename;
          reader_ = rosbag2_transport::ReaderWriterFactory::make_reader(storage_options);
          reader_->open(storage_options);
        }

      private:
        void timer_callback()
        {
          while (reader_->has_next()) {
            rosbag2_storage::SerializedBagMessageSharedPtr msg = reader_->read_next();

            if (msg->topic_name != "/turtle1/pose") {
              continue;
            }

            rclcpp::SerializedMessage serialized_msg(*msg->serialized_data);
            turtlesim::msg::Pose::SharedPtr ros_msg = std::make_shared<turtlesim::msg::Pose>();

            serialization_.deserialize_message(&serialized_msg, ros_msg.get());

            publisher_->publish(*ros_msg);
            std::cout << '(' << ros_msg->x << ", " << ros_msg->y << ")\n";

            break;
          }
        }

        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<turtlesim::msg::Pose>::SharedPtr publisher_;

        rclcpp::Serialization<turtlesim::msg::Pose> serialization_;
        std::unique_ptr<rosbag2_cpp::Reader> reader_;
    };

    int main(int argc, char ** argv)
    {
      if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <bag>" << std::endl;
        return 1;
      }

      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<PlaybackNode>(argv[1]));
      rclcpp::shutdown();

      return 0;
    }

2.1 分析代码
~~~~~~~~~~~~

顶部的 ``#include`` 语句是包依赖。
注意包含了来自 ``rosbag2_transport`` 包的头文件，这些头文件提供了处理 bag 文件所需的函数和结构。

下一行创建了将读取 bag 文件并回放数据的节点。

.. code-block:: C++

    class PlaybackNode : public rclcpp::Node

现在，我们可以创建一个以 10 Hz 运行的回调定时器。
我们的目标是每次运行回调时，向 ``/turtle1/pose`` 主题回放一条消息。
注意构造函数接收 bag 文件的路径作为参数。

.. code-block:: C++

    public:
      PlaybackNode(const std::string & bag_filename)
      : Node("playback_node")
      {
        publisher_ = this->create_publisher<turtlesim::msg::Pose>("/turtle1/pose", 10);

        timer_ = this->create_wall_timer(100ms,
          [this](){return this->timer_callback();}
        );

我们还在构造函数中打开 bag。
``rosbag2_transport::ReaderWriterFactory`` 是一个类，可以根据存储选项构造压缩或未压缩的读取器或写入器。

.. code-block:: C++

      rosbag2_storage::StorageOptions storage_options;
      storage_options.uri = bag_filename;
      reader_ = rosbag2_transport::ReaderWriterFactory::make_reader(storage_options);
      reader_->open(storage_options);

现在，在我们的定时器回调中，我们遍历 bag 中的消息，直到读取到一条从我们期望的主题录制的消息。
请注意，序列化消息除了主题名之外还带有时间戳元数据。

.. code-block:: C++

    void timer_callback()
    {
      while (reader_->has_next()) {
        rosbag2_storage::SerializedBagMessageSharedPtr msg = reader_->read_next();

        if (msg->topic_name != "/turtle1/pose") {
          continue;
        }

然后，我们从刚读取的序列化数据构造一个 ``rclcpp::SerializedMessage`` 对象。
此外，我们需要创建一个 ROS 2 反序列化消息，用于保存反序列化的结果。
然后，我们可以将这两个对象都传给 ``rclcpp::Serialization::deserialize_message`` 方法。

.. code-block:: C++

    rclcpp::SerializedMessage serialized_msg(*msg->serialized_data);
    turtlesim::msg::Pose::SharedPtr ros_msg = std::make_shared<turtlesim::msg::Pose>();

    serialization_.deserialize_message(&serialized_msg, ros_msg.get());

最后，我们发布反序列化后的消息，并将 xy 坐标打印到终端。
我们还跳出循环，以便在下一次定时器回调中发布下一条消息。

.. code-block:: C++

      publisher_->publish(*ros_msg);
      std::cout << '(' << ros_msg->x << ", " << ros_msg->y << ")\n";

      break;
    }

我们还需要声明整个节点中使用的私有变量。

.. code-block:: C++

      rclcpp::TimerBase::SharedPtr timer_;
      rclcpp::Publisher<turtlesim::msg::Pose>::SharedPtr publisher_;

      rclcpp::Serialization<turtlesim::msg::Pose> serialization_;
      std::unique_ptr<rosbag2_cpp::Reader> reader_;
    };

最后，我们创建主函数，用于检查用户是否为 bag 文件路径传入了参数，并旋转我们的节点。

.. code-block:: C++

    int main(int argc, char ** argv)
    {
      if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <bag>" << std::endl;
        return 1;
      }

      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<PlaybackNode>(argv[1]));
      rclcpp::shutdown();

      return 0;
    }

2.2 添加可执行文件
~~~~~~~~~~~~~~~~~~

现在打开 ``CMakeLists.txt`` 文件。

在包含 ``find_package(rosbag2_transport REQUIRED)`` 的依赖块下面，添加以下代码行。

.. code-block:: console

    add_executable(simple_bag_reader src/simple_bag_reader.cpp)
    ament_target_dependencies(simple_bag_reader rclcpp rosbag2_transport turtlesim)

    install(TARGETS
      simple_bag_reader
      DESTINATION lib/${PROJECT_NAME}
    )

3 构建并运行
^^^^^^^^^^^^

导航回工作空间的根目录，并构建你的新包。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select bag_reading_cpp

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select bag_reading_cpp

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select bag_reading_cpp

接下来，source 安装文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install/setup.bat

现在，运行该脚本。
确保将 ``/path/to/subset`` 替换为你的 ``subset`` bag 的路径。

.. code-block:: console

    $ ros2 run bag_reading_cpp simple_bag_reader /path/to/subset

你应该会看到乌龟的 (x, y) 坐标打印到控制台。

总结
----

你创建了一个从 bag 中读取数据的 C++ 可执行文件。
然后你编译并运行了该可执行文件，它将 bag 中的一些信息打印到了控制台。
