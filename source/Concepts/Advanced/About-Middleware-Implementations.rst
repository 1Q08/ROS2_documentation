.. redirect-from::

   Concepts/About-Middleware-Implementations

ROS 2 中间件实现
================

.. contents:: 目录
   :local:

.. include:: ../../../global_substitutions.txt

ROS 中间件实现是实现部分内部 ROS 接口（例如 ``rmw``、``rcl`` 和 ``rosidl`` |APIs|）的一组 |packages|。

有关 ROS 2 如何与不同中间件实现集成的更实用的深入概述，请参见 :doc:`中间件实现教程 <../../Tutorials/Advanced/Creating-An-RMW-Implementation>`。

DDS 中间件包的通用包
--------------------

目前所有 ROS 中间件实现都基于完整或部分的 DDS 实现。
例如，有一个使用 RTI 的 Connext DDS 的中间件实现，还有一个使用 eProsima 的 Fast DDS 的实现。
因此，在大多数基于 DDS 的中间件实现中存在一些共享的 |packages|。

在 |GitHub|_ 上的 `ros2/rosidl_dds <https://github.com/ros2/rosidl_dds>`_ 仓库中，有以下 |package|：

-  ``rosidl_generator_dds_idl``：提供工具，用于从 ``rosidl`` 文件（例如 ``.msg`` 文件、``.srv`` 文件等）生成 DDS ``.idl`` 文件。

``rosidl_generator_dds_idl`` |package| 为由包含消息的 |packages| 所定义的每个 ``rosidl`` 文件（例如 ``.msg`` 文件）生成一个 DDS ``.idl`` 文件。
目前基于 DDS 的 ROS 中间件实现利用该生成器输出的 ``.idl`` 文件来生成供应商特定的预编译类型支持。

.. _about-middleware-impls_struct_dds:

ROS 中间件实现的结构
--------------------

一个 ROS 中间件实现通常由单个仓库中的几个 |packages| 组成：

- ``<implementation_name>_cmake_module``：包含用于发现和暴露所需依赖项的 CMake 模块
- ``rmw_<implementation_name>_<language>``：包含特定语言（通常是 C++）的 ``rmw`` |API| 实现
- ``rosidl_typesupport_<implementation_name>_<language>``：包含为 ``rosidl`` 文件生成静态类型支持代码的工具，针对特定语言（通常是 C 或 C++）的实现定制

``<implementation_name>_cmake_module`` |package| 包含查找中间件实现支持依赖项所需的任何 CMake 模块和函数。
例如，``rti_connext_dds_cmake_module`` 围绕 RTI Connext DDS 附带的 CMake 模块提供包装逻辑，以确保所有依赖它的包都会选择相同的 RTI Connext DDS 安装。
类似地，``fastrtps_cmake_module`` 包含一个用于查找 eProsima 的 Fast DDS 的 CMake 模块，而 ``gurumdds_cmake_module`` 包含一个用于查找 GurumNetworks GurumDDS 的 CMake 模块。
并非所有实现都会有这样的包：例如，Eclipse 的 Cyclone DDS 已经提供了一个 CMake 模块，其 RMW 实现直接使用该模块，而无需额外的包装器。

``rmw_<implementation_name>_<language>`` |package| 以特定语言实现 ``rmw`` C |API|。
实现本身可以是 C++，但必须以 ``extern "C"`` 方式暴露头文件的符号，以便 C 应用程序可以链接到它。

``rosidl_typesupport_<implementation_name>_<language>`` |package| 提供一个生成器，以特定语言生成 DDS 代码。
这是使用 ``rosidl_generator_dds_idl`` |package| 生成的 ``.idl`` 文件以及 DDS 供应商提供的 DDS IDL 代码生成器来完成的。
它还生成用于在 ROS 消息结构和 DDS 消息结构之间进行转换的代码。
该生成器还负责为其所在的消息包创建一个共享库，该共享库特定于消息包中的消息以及所使用的 DDS 供应商。

如上所述，如果 rmw 实现支持消息的运行时解释，则可以使用 ``rosidl_typesupport_introspection_<language>`` 来代替供应商特定的类型支持包。
这种无需预先生成代码就能以编程方式在话题上发送和接收类型的能力，是通过支持 `DDS X-Types 动态数据标准 <https://www.omg.org/spec/DDS-XTypes/>`_ 来实现的。
因此，rmw 实现可以提供对 X-Types 标准的支持，和/或提供针对其 DDS 实现在编译时生成的类型支持的包。

作为 rmw 实现仓库的一个示例，``Eclipse Cyclone DDS`` ROS 中间件实现在 |GitHub|_ 上的 `ros2/rmw_cyclonedds <https://github.com/ros2/rmw_cyclonedds>`_。

``Fast DDS`` 的 rmw 实现在 |GitHub|_ 上的 `ros2/rmw_fastrtps_cpp <https://github.com/ros2/rmw_fastrtps_cpp>`_。

``Connext DDS`` 的 rmw 实现在 |GitHub|_ 上的 `ros2/rmw_connextdds <https://github.com/ros2/rmw_connextdds>`_。

``GurumDDS`` 的 rmw 实现在 |GitHub|_ 上的 `ros/rmw_gurumdds <https://github.com/ros2/rmw_gurumdds>`_。
