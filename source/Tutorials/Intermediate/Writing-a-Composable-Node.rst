编写一个可组合节点（C++）
=========================

.. contents:: 目录
   :depth: 2
   :local:

起点
----

假设你有一个常规的 ``rclcpp::Node`` 可执行文件，并且希望它与其他节点在同一进程中运行，以实现更高效的通信。

我们从拥有一个直接继承自 ``Node`` 的类开始，并且该类还定义了一个 main 方法。

.. code-block:: c++

    namespace palomino
    {
        class VincentDriver : public rclcpp::Node
        {
            // ...
        };
    }

    int main(int argc, char * argv[])
    {
        rclcpp::init(argc, argv);
        rclcpp::spin(std::make_shared<palomino::VincentDriver>());
        rclcpp::shutdown();
        return 0;
    }

这通常会在你的 Cmake 中被编译为可执行文件。

.. code-block:: cmake

    # ...
    add_executable(vincent_driver src/vincent_driver.cpp)
    # ...
    install(TARGETS vincent_driver
        DESTINATION lib/${PROJECT_NAME}
    )

代码更新
--------

添加包依赖
^^^^^^^^^^

你的 `package.xml <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/composition/package.xml>`__ 应该对 ``rclcpp_components`` 有依赖，就像这样

.. code-block:: xml

    <depend>rclcpp_components</depend>

或者，你也可以独立添加一个 ``build_depend/exec_depend``。

类定义
^^^^^^

你可能需要对类定义做的唯一改动是，确保 `类的构造函数 <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/composition/src/talker_component.cpp>`__ 接受一个 ``NodeOptions`` 参数。

.. code-block:: c++

    VincentDriver(const rclcpp::NodeOptions & options) : Node("vincent_driver", options)
    {
      // ...
    }

不再需要 main 方法
^^^^^^^^^^^^^^^^^^

将你的 main 方法替换为一个 ``pluginlib`` 风格的宏调用。

.. code-block:: c++

    #include <rclcpp_components/register_node_macro.hpp>
    RCLCPP_COMPONENTS_REGISTER_NODE(palomino::VincentDriver)

.. caution::
    如果你正在替换的 main 方法包含 ``MultiThreadedExecutor``，请务必留意并确保你的容器节点是多线程的。
    参见下文部分。

CMake 更改
^^^^^^^^^^
首先，在你的 CMakeLists.txt 中添加 ``rclcpp_components`` 作为依赖：

.. code-block:: cmake

    find_package(rclcpp_components REQUIRED)

其次，我们将用 ``add_library`` 替换我们的 ``add_executable``，并使用一个新的目标名称。

.. code-block:: cmake

    add_library(vincent_driver_component SHARED src/vincent_driver.cpp)

第三，替换其他使用旧目标的构建命令，使其作用于新目标。
别忘了在 ``ament_target_dependencies`` 中添加 ``rclcpp_components``。
即 ``ament_target_dependencies(vincent_driver ...)`` 变为 ``ament_target_dependencies(vincent_driver_component "rclcpp_components" ...)``

第四，添加一个新命令来声明你的组件。

.. code-block:: cmake

    rclcpp_components_register_node(
        vincent_driver_component
        PLUGIN "palomino::VincentDriver"
        EXECUTABLE vincent_driver
    )

第五，也是最后一步，将 CMake 中作用于旧目标的任何安装命令改为安装库版本。
例如，不要将任一个目标安装到 ``lib/${PROJECT_NAME}`` 中。
改为安装库。

.. code-block:: cmake

    ament_export_targets(export_vincent_driver_component)
    install(TARGETS vincent_driver_component
            EXPORT export_vincent_driver_component
            ARCHIVE DESTINATION lib
            LIBRARY DESTINATION lib
            RUNTIME DESTINATION bin
    )


运行你的节点
------------

参见 :doc:`Composition 教程 <Composition>` 以深入了解节点组合。
快速而粗略的版本是，如果你的 Python launch 文件中有以下内容，

.. code-block:: python

    from launch_ros.actions import Node

    # ..

    ld.add_action(Node(
        package='palomino',
        executable='vincent_driver',
        # ..
    ))

你可以将它替换为

.. code-block:: python

    from launch_ros.actions import ComposableNodeContainer
    from launch_ros.descriptions import ComposableNode

    # ..
    ld.add_action(ComposableNodeContainer(
        name='a_buncha_nodes',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='palomino',
                plugin='palomino::VincentDriver',
                name='vincent_driver',
                # ..
                extra_arguments=[{'use_intra_process_comms': True}],
            ),
        ]
    ))

.. caution::

    如果你需要多线程，不要将可执行文件设置为 ``component_container``，而是将其设置为 ``component_container_mt``
