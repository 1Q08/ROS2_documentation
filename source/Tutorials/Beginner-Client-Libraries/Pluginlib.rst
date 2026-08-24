.. redirect-from::

    Tutorials/Pluginlib

创建和使用插件（C++）
=====================

**目标：** 学习如何使用 ``pluginlib`` 创建和加载一个简单的插件。

**教程级别：** 入门

**时间：** 20 分钟

.. contents:: 目录
   :depth: 3
   :local:

背景
----

本教程源自 `<http://wiki.ros.org/pluginlib>`_ 以及 `编写和使用简单插件教程 <http://wiki.ros.org/pluginlib/Tutorials/Writing%20and%20Using%20a%20Simple%20Plugin>`_。

``pluginlib`` 是一个 C++ 库，用于在 ROS 包中加载和卸载插件。
插件是动态可加载的类，它们从运行时库（即共享对象、动态链接库）中加载。
使用 pluginlib，你不必显式地将你的应用程序与包含这些类的库链接——相反，``pluginlib`` 可以在任意时刻打开包含导出类的库，而应用程序事先并不知道该库或包含类定义的头文件。
插件对于在不需要应用程序源代码的情况下扩展/修改应用程序行为非常有用。

前置条件
--------

本教程假设你具备基本的 C++ 知识，并已成功 :doc:`安装 ROS 2 <../../Installation>`。

任务
----

在本教程中，你将创建两个新包，一个定义基类，另一个提供插件。
基类将定义一个通用的多边形类，然后我们的插件将定义具体的形状。

1 创建基类包
^^^^^^^^^^^^

使用以下命令在你的 ``ros2_ws/src`` 文件夹中创建一个新的空包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 --dependencies pluginlib --node-name area_node polygon_base


打开你喜欢的编辑器，编辑 ``ros2_ws/src/polygon_base/include/polygon_base/regular_polygon.hpp``，并将以下内容粘贴进去：

.. code-block:: C++

    #ifndef POLYGON_BASE_REGULAR_POLYGON_HPP
    #define POLYGON_BASE_REGULAR_POLYGON_HPP

    namespace polygon_base
    {
      class RegularPolygon
      {
        public:
          virtual void initialize(double side_length) = 0;
          virtual double area() = 0;
          virtual ~RegularPolygon(){}

        protected:
          RegularPolygon(){}
      };
    }  // namespace polygon_base

    #endif  // POLYGON_BASE_REGULAR_POLYGON_HPP

上面的代码创建了一个名为 ``RegularPolygon`` 的抽象类。
需要注意的一点是 initialize 方法的存在。
对于 ``pluginlib``，必须有一个无参构造函数，所以如果类需要任何参数，我们就使用 initialize 方法将它们传递给对象。

我们需要通过将这个头文件导出为接口库，使其对其他类可用。
为此，打开 ``~/ros2_ws/src/polygon_base/CMakeLists.txt`` 进行编辑，
并在 ``find_package(pluginlib REQUIRED)`` 命令之后添加以下几行：

.. code-block:: cmake

    # Library (this will be used as the base class for plugins)
    add_library(${PROJECT_NAME} INTERFACE)
    add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})
    target_compile_features(${PROJECT_NAME} INTERFACE c_std_99 cxx_std_17)
    target_include_directories(${PROJECT_NAME} INTERFACE
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/${PROJECT_NAME}>
    )
    target_link_libraries(${PROJECT_NAME} INTERFACE ${pluginlib_TARGETS})

    # Install headers
    install(DIRECTORY include/
      DESTINATION include/${PROJECT_NAME}
    )

    # Install library and export targets
    install(TARGETS ${PROJECT_NAME}
      EXPORT export_${PROJECT_NAME}
      ARCHIVE DESTINATION lib
      LIBRARY DESTINATION lib
      RUNTIME DESTINATION bin
    )
    install(EXPORT export_${PROJECT_NAME}
      NAMESPACE ${PROJECT_NAME}::
      DESTINATION share/${PROJECT_NAME}/cmake
    )

并在 ``ament_package`` 命令之前添加这些命令：

.. code-block:: cmake

    # Export old-style CMake variables
    ament_export_include_directories(
      include
    )

    # Export modern CMake targets
    ament_export_targets(
      export_${PROJECT_NAME}
    )

我们稍后会回到这个包来编写我们的测试节点。

2 创建插件包
^^^^^^^^^^^^

现在我们要编写抽象类的两个非虚实现。
使用以下命令在你的 ``ros2_ws/src`` 文件夹中创建第二个空包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 --dependencies polygon_base pluginlib --library-name polygon_plugins polygon_plugins

2.1 插件的源代码
~~~~~~~~~~~~~~~~

打开 ``ros2_ws/src/polygon_plugins/src/polygon_plugins.cpp`` 进行编辑，并将以下内容粘贴进去：

.. code-block:: C++

    #include <polygon_base/regular_polygon.hpp>
    #include <cmath>

    namespace polygon_plugins
    {
      class Square : public polygon_base::RegularPolygon
      {
        public:
          void initialize(double side_length) override
          {
            side_length_ = side_length;
          }

          double area() override
          {
            return side_length_ * side_length_;
          }

        protected:
          double side_length_;
      };

      class Triangle : public polygon_base::RegularPolygon
      {
        public:
          void initialize(double side_length) override
          {
            side_length_ = side_length;
          }

          double area() override
          {
            return 0.5 * side_length_ * getHeight();
          }

          double getHeight()
          {
            return sqrt((side_length_ * side_length_) - ((side_length_ / 2) * (side_length_ / 2)));
          }

        protected:
          double side_length_;
      };
    }

    #include <pluginlib/class_list_macros.hpp>

    PLUGINLIB_EXPORT_CLASS(polygon_plugins::Square, polygon_base::RegularPolygon)
    PLUGINLIB_EXPORT_CLASS(polygon_plugins::Triangle, polygon_base::RegularPolygon)

Square 和 Triangle 类的实现相当直接：保存边长，并用它来计算面积。
唯一与 pluginlib 相关的部分是最后三行，它们调用了一些“神奇的”宏，将这些类注册为真正的插件。
让我们来看看 ``PLUGINLIB_EXPORT_CLASS`` 宏的参数：

1. 插件类的完全限定类型，在本例中是 ``polygon_plugins::Square``。
2. 基类的完全限定类型，在本例中是 ``polygon_base::RegularPolygon``。

2.2 插件声明 XML
~~~~~~~~~~~~~~~~

上述步骤使得当包含库被加载时可以创建插件实例，但插件加载器仍然需要一种方法来找到该库，并知道在该库中引用什么。
为此，我们还要创建一个 XML 文件，它与包清单中的特殊导出行一起，将所有关于我们插件的必要信息提供给 ROS 工具链。

创建 ``ros2_ws/src/polygon_plugins/plugins.xml``，包含以下代码：

.. code-block:: XML

    <library path="polygon_plugins">
      <class type="polygon_plugins::Square" base_class_type="polygon_base::RegularPolygon">
        <description>This is a square plugin.</description>
      </class>
      <class type="polygon_plugins::Triangle" base_class_type="polygon_base::RegularPolygon" name="awesome_triangle">
        <description>This is a triangle plugin.</description>
      </class>
    </library>

有几点需要注意：

1. ``library`` 标签给出包含我们要导出的插件的库的相对路径。
   在 ROS 2 中，那只是库的名称。
   在 ROS 1 中，它包含前缀 ``lib`` 或有时是 ``lib/lib`` （即 ``lib/libpolygon_plugins``），但在这里更简单。
2. ``class`` 标签声明了一个我们要从库中导出的插件。
   让我们来看看它的参数：

  * ``type``：插件的完全限定类型。
    对我们来说，就是 ``polygon_plugins::Square``。
  * ``base_class``：插件的完全限定基类类型。
    对我们来说，就是 ``polygon_base::RegularPolygon``。
  * ``description``：插件及其功能的描述。
  * ``name`` （可选）：类加载器使用的查找名称（即魔术名称）。

2.3 CMake 插件声明
~~~~~~~~~~~~~~~~~~

最后一步是通过 ``CMakeLists.txt`` 导出你的插件。
这与 ROS 1 不同，在 ROS 1 中导出是通过 ``package.xml`` 完成的。
在 ``ros2_ws/src/polygon_plugins/CMakeLists.txt`` 中 ``find_package(pluginlib REQUIRED)`` 那一行之后添加以下行：

.. code-block:: cmake

    pluginlib_export_plugin_description_file(polygon_base plugins.xml)

``pluginlib_export_plugin_description_file`` 命令的参数是：

1. 包含基类的包，即 ``polygon_base``。
2. 插件声明 xml 的相对路径，即 ``plugins.xml``。

3 使用插件
^^^^^^^^^^

现在是时候使用插件了。
这可以在任何包中完成，但这里我们将在基类包中完成。
编辑 ``ros2_ws/src/polygon_base/src/area_node.cpp`` 使其包含以下内容：

.. code-block:: C++

    #include <pluginlib/class_loader.hpp>
    #include <polygon_base/regular_polygon.hpp>

    int main(int argc, char** argv)
    {
      // To avoid unused parameter warnings
      (void) argc;
      (void) argv;

      pluginlib::ClassLoader<polygon_base::RegularPolygon> poly_loader("polygon_base", "polygon_base::RegularPolygon");

      try
      {
        std::shared_ptr<polygon_base::RegularPolygon> triangle = poly_loader.createSharedInstance("awesome_triangle");
        triangle->initialize(10.0);

        std::shared_ptr<polygon_base::RegularPolygon> square = poly_loader.createSharedInstance("polygon_plugins::Square");
        square->initialize(10.0);

        printf("Triangle area: %.2f\n", triangle->area());
        printf("Square area: %.2f\n", square->area());
      }
      catch(pluginlib::PluginlibException& ex)
      {
        printf("The plugin failed to load for some reason. Error: %s\n", ex.what());
      }

      return 0;
    }

``ClassLoader`` 是需要理解的关键类，定义在 ``class_loader.hpp`` `头文件 <https://github.com/ros/pluginlib/blob/ros2/pluginlib/include/pluginlib/class_loader.hpp>`_ 中：

 * 它以基类为模板参数，即 ``polygon_base::RegularPolygon``。
 * 第一个参数是基类包名的字符串，即 ``polygon_base``。
 * 第二个参数是插件基类完全限定类型的字符串，即 ``polygon_base::RegularPolygon``。

有多种方式可以实例化类的实例。
在这个例子中，我们使用共享指针。
我们只需要用插件的引用调用 ``createSharedInstance``：这可以是插件类的完全限定类型（声明 XML 文件的 ``type`` 属性，例如 ``polygon_plugins::Square``），也可以是可选的魔术名称（声明 XML 文件的 ``name`` 属性，例如 ``awesome_triangle``）。

重要提示：定义此节点的 ``polygon_base`` 包并不依赖于 ``polygon_plugins`` 类。
插件将被动态加载，而无需声明任何依赖。
此外，我们使用硬编码的插件名称来实例化类，但你也可以使用参数等动态地完成此操作。

4 构建并运行
^^^^^^^^^^^^

返回到工作空间的根目录 ``ros2_ws``，并构建你的新包：

.. code-block:: console

    $ colcon build --packages-select polygon_base polygon_plugins

从 ``ros2_ws`` 出发，务必 source 安装文件：

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

``ros2 plugin`` 命令由 ``ros2plugin`` 包提供。
如果在 Debian 包安装上此命令不可用，请使用以下命令安装它：

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-ros2plugin

你可以通过列出它们来验证你的插件是否已成功注册：

.. code-block:: console

     $ ros2 plugin list
     polygon_plugins:
        Plugin(name='polygon_plugins::Square', type='polygon_plugins::Square', base='polygon_base::RegularPolygon')
        Plugin(name='polygon_plugins::Triangle', type='polygon_plugins::Triangle', base='polygon_base::RegularPolygon')

现在运行节点：

.. code-block:: console

     $ ros2 run polygon_base area_node
     Triangle area: 43.30
     Square area: 100.00

总结
----

恭喜你！
你刚刚编写并使用了你的第一个插件。
