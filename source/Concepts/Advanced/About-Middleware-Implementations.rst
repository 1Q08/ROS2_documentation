.. redirect-from::

   Concepts/About-Middleware-Implementations

ROS 2 中间件实现
================

.. contents:: 目录
   :local:

.. include:: ../../../global_substitutions.txt

ROS 中间件实现是一组 |packages|，它们实现了某些内部 ROS 接口，例如 ``rmw``、``rcl`` 和 ``rosidl`` |APIs|。

关于 ROS 2 如何与不同中间件实现集成的更实用的深入概览，请参阅 :doc:`中间件实现教程 <../../Tutorials/Advanced/Creating-An-RMW-Implementation>`。

DDS 中间件包的公共包
--------------------

当前所有 ROS 中间件实现都基于完整或部分的 DDS 实现。
例如，有一个中间件实现使用 RTI 的 Connext DDS，还有一个实现使用 eProsima 的 Fast DDS。
因此，在大多数基于 DDS 的中间件实现中，存在一些共享的 |packages|。

在 |GitHub|_ 上的 `ros2/rosidl_dds <https://github.com/ros2/rosidl_dds>`_ 仓库中，有以下 |package|：

-  ``rosidl_generator_dds_idl``：提供从 ``rosidl`` 文件（例如 ``.msg`` 文件、``.srv`` 文件等）生成 DDS ``.idl`` 文件的工具。

``rosidl_generator_dds_idl`` |package| 会为包含消息的 |packages| 所定义的每个 ``rosidl`` 文件（例如 ``.msg`` 文件）生成一个 DDS ``.idl`` 文件。
目前，基于 DDS 的 ROS 中间件实现会利用该生成器输出的 ``.idl`` 文件，来生成特定于厂商的预编译类型支持。

.. _about-middleware-impls_struct_dds:

ROS 中间件实现的结构
--------------------

一个 ROS 中间件实现通常由单个仓库中的几个 |packages| 组成：

- ``<implementation_name>_cmake_module``：包含用于发现和暴露所需依赖项的 CMake 模块
- ``rmw_<implementation_name>_<language>``：包含用特定语言（通常是 C++）实现的 ``rmw`` |API|
- ``rosidl_typesupport_<implementation_name>_<language>``：包含为 ``rosidl`` 文件生成静态类型支持代码的工具，这些代码针对特定语言（通常是 C 或 C++）的实现而定制

``<implementation_name>_cmake_module`` |package| 包含查找该中间件实现所需支撑依赖项时用到的任何 CMake 模块和函数。
例如，``rti_connext_dds_cmake_module`` 围绕 RTI Connext DDS 随附的 CMake 模块提供了包装逻辑，以确保所有依赖它的包都会选择同一个 RTI Connext DDS 安装。
类似地，``fastrtps_cmake_module`` 包含一个用于查找 eProsima 的 Fast DDS 的 CMake 模块，而 ``gurumdds_cmake_module`` 包含一个用于查找 GurumNetworks GurumDDS 的 CMake 模块。
并非所有实现都会有这样的包：例如，Eclipe 的 Cyclone DDS 已经提供了一个 CMake 模块，其 RMW 实现直接使用它，无需额外的包装器。

``rmw_<implementation_name>_<language>`` |package| 用特定语言实现 ``rmw`` C |API|。
实现本身可以是 C++，只是必须以 ``extern "C"`` 形式暴露头文件中的符号，以便 C 应用可以链接它。

``rosidl_typesupport_<implementation_name>_<language>`` |package| 提供一个生成器，用于生成特定语言的 DDS 代码。
这是利用 ``rosidl_generator_dds_idl`` |package| 生成的 ``.idl`` 文件以及 DDS 厂商提供的 DDS IDL 代码生成器来完成的。
它还会生成用于在 ROS 消息结构与 DDS 消息结构之间相互转换的代码。
该生成器还负责为使用它的消息包创建一个共享库，该共享库特定于该消息包中的消息以及所使用的 DDS 厂商。

如上所述，如果某个 rmw 实现支持在运行时解释消息，则可以使用 ``rosidl_typesupport_introspection_<language>`` 来替代厂商特定的类型支持包。
这种无需预先生成代码即可在话题上以编程方式收发类型的能力，是通过支持 `DDS X-Types 动态数据标准 <https://www.omg.org/spec/DDS-XTypes/>`_ 来实现的。
因此，rmw 实现可以提供对 X-Types 标准的支持，和/或提供一个针对其 DDS 实现在编译时生成的类型支持包。

作为一个 rmw 实现仓库的例子，``Eclipse Cyclone DDS`` ROS 中间件实现在 |GitHub|_ 上的地址是 `ros2/rmw_cyclonedds <https://github.com/ros2/rmw_cyclonedds>`_。

``Fast DDS`` 的 rmw 实现在 |GitHub|_ 上的地址是 `ros2/rmw_fastrtps_cpp <https://github.com/ros2/rmw_fastrtps_cpp>`_。

``Connext DDS`` 的 rmw 实现在 |GitHub|_ 上的地址是 `ros2/rmw_connextdds <https://github.com/ros2/rmw_connextdds>`_。

``GurumDDS`` 的 rmw 实现在 |GitHub|_ 上的地址是 `ros/rmw_gurumdds <https://github.com/ros2/rmw_gurumdds>`_。
