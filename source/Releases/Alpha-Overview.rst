.. redirect-from::

   Alpha-Overview

Alpha 版本
==========

.. contents:: 目录
   :depth: 2
   :local:

这是 ROS 2 的 8 个 alpha 版本之前独立页面的合并版本。

我们希望你能试用它们并 `提供反馈 <../../Contact>`。

ROS 2 alpha8 版本（代号 *Hook-and-Loop*；2016 年 10 月）
--------------------------------------------------------

支持的 DDS 厂商变更
^^^^^^^^^^^^^^^^^^^

ROS 2 支持多个中间件实现（更多详情参见 `本页面 <../../Concepts/Intermediate/About-Different-Middleware-Vendors>`）。
在 Alpha 8 之前，ROS 2 支持 eProsima 的 Fast RTPS、RTI 的 Connext 和 PrismTech 的 OpenSplice 的 ROS 中间件实现。
为了集中精力，从 Alpha 8 开始，将支持 Fast RTPS 和 Connext（静态），并以 Fast RTPS（`现已采用 Apache 2.0 许可 <http://www.eprosima.com/index.php/company-all/news/61-eprosima-goes-apache>`__）作为默认实现。

范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应期望用 ROS 2 构建新的机器人控制系统。
相反，你应该期望尝试一些演示，探索代码，也许还可以编写自己的演示。

此版本中包含的改进有：


* 对 Fast RTPS 及其 rmw 实现的若干改进

  * 支持 Fast RTPS 中的大（图像）消息
  * Fast RTPS 中的 ``wait_for_service`` 功能

* 支持 Python 和 C 中的所有 ROS 2 消息类型
* 在 Python 中增加了对服务质量（QoS）设置的支持
* 修复了上一个 alpha 版本中的各种 bug

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。

ROS 2 alpha7 版本（代号 *Glue Gun*\ ；2016 年 7 月）
----------------------------------------------------

.. contents:: 目录
   :local:

需要新版本 Ubuntu
^^^^^^^^^^^^^^^^^

在 Alpha 6 之前，ROS 2 的目标平台是 Ubuntu Trusty Tahr (14.04)。从这个 Alpha 版本开始，ROS 2 的目标平台改为 Ubuntu Xenial Xerus (16.04)，以受益于更新版本的编译器、CMake、Python 等。

范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应期望用 ROS 2 构建新的机器人控制系统。
相反，你应该期望尝试一些演示，探索代码，也许还可以编写自己的演示。

此版本中包含的主要功能有：


* 图 API 功能：wait_for_service

  * 在 rclcpp 中添加了接口，并在示例、演示和测试中使用它们

* 改进了对 Connext 和 Fast-RTPS 中大消息的支持（Fast-RTPS 部分支持）
* 使用从 ROS 1 移植代码的 Turtlebot 演示

  * 参见：https://github.com/ros2/turtlebot2_demo

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。

ROS 2 alpha6 版本（代号 *Fastener*；2016 年 6 月）
--------------------------------------------------

.. contents:: 目录
   :local:

范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应期望用 ROS 2 构建新的机器人控制系统。
相反，你应该期望尝试一些演示，探索代码，也许还可以编写自己的演示。

此版本中包含的主要功能有：


* 图 API 功能：wait_for_service

  * 为节点添加了图守卫条件，用于等待图变更
  * 添加了 ``rmw_service_server_is_available``，用于验证服务是否可用

* 重构了 ``rclcpp`` 以使用 ``rcl``
* 改进了 Python 中对复杂消息类型的支持

  * 嵌套消息
  * 数组
  * 字符串

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。

ROS 2 alpha5 版本（代号 *Epoxy*；2016 年 4 月）
-----------------------------------------------

.. contents:: 目录
   :local:


范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应期望用 ROS 2 构建新的机器人控制系统。
相反，你应该期望尝试一些演示，探索代码，也许还可以编写自己的演示。

此版本中包含的主要功能有：


* 支持 Fast RTPS 和 Connext Dynamic rmw 实现中的 C 数据结构。
* 支持 C 中的服务。
* 将 32 位和 64 位 ARM 添加为实验性支持的平台。

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。

ROS 2 alpha4 版本（代号 *Duct tape*；2016 年 2 月）
---------------------------------------------------

.. contents:: 目录
   :local:

背景
^^^^

正如一篇 `设计文章 <https://design.ros2.org/articles/why_ros2.html>`__ 所解释的，
我们正在开发 ROS 的一个新主要版本，称为 "ROS 2"。
虽然底层概念（例如发布 / 订阅消息）和目标
（例如灵活性和可复用性）与 ROS 1 相同，但我们借此
机会对系统进行重大更改，包括更改
一些核心 API。
如需更深入地了解这些更改及其理由，请参阅其他
`ROS 2 设计文章 <https://design.ros2.org>`__。

状态
^^^^

2016 年 2 月 17 日，我们发布了 ROS 2 alpha4，
代号 **Duct tape**。
此版本的主要目标是添加更多功能，同时处理我们在之前版本中收到的反馈。
为此，我们构建了一组 `演示 <../../Tutorials>`，它们
展示了 ROS 2 的一些关键功能。
我们鼓励你尝试这些
演示，查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们特别想知道我们在多大程度上（或多差地）
满足了对你们重要的用例。

目标受众
^^^^^^^^

虽然欢迎大家尝试演示并浏览代码，但此版本面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀疏，系统的许多内容都是通过与 ROS 1 的对比来说明的。

范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未
完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该期望尝试一些演示，探索代码，也许还可以编写
自己的演示。

此版本中包含的主要功能有：


* 改进的类型支持基础设施，包括对 C 的支持
* 初步的 Python 客户端库，仅支持发布者和订阅者。请注意，API 可能会发生变化，且远未完成！
* 在 C API 中为 ROS 时间添加了结构（仍需要 C++ API）

  * 可扩展 "时间源" 的新概念，用于 ROS Time，默认时间源将类似于 ROS 1（实现待定）

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。

ROS 2 alpha3 版本（代号 *Cement*；2015 年 12 月）
-------------------------------------------------

.. contents:: 目录
   :local:


背景
^^^^

正如一篇 `设计文章 <https://design.ros2.org/articles/why_ros2.html>`__ 所解释的，
我们正在开发 ROS 的一个新主要版本，称为 "ROS 2"。
虽然底层概念（例如发布 / 订阅消息）和目标
（例如灵活性和可复用性）与 ROS 1 相同，但我们借此
机会对系统进行重大更改，包括更改
一些核心 API。
如需更深入地了解这些更改及其理由，请参阅其他
`ROS 2 设计文章 <https://design.ros2.org>`__。

状态
^^^^

2015 年 12 月 18 日，我们发布了 ROS 2 alpha3，
代号 **Cement**。
此版本的主要目标是添加更多功能，同时处理我们在之前版本中收到的反馈。
为此，我们构建了一组 `演示 <../../Tutorials>`，它们
展示了 ROS 2 的一些关键功能。
我们鼓励你尝试那些
演示，查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们特别想知道我们在多大程度上（或多差地）
满足了对你们重要的用例。

目标受众
^^^^^^^^

虽然欢迎大家尝试演示并浏览代码，但此版本面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀疏，系统的许多内容都是通过与 ROS 1 的对比来说明的。

范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未
完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该期望尝试一些演示，探索代码，也许还可以编写
自己的演示。

此版本中包含的主要功能有：


* 更新了 ``rcl`` 接口。

  * 此接口将被包装以创建语言绑定，例如 ``rclpy``。
  * 与我们目前已有的接口（例如 ``rmw`` 和 ``rclcpp``）相比，此接口改进了文档和测试覆盖率。
  * 参见 `rcl 头文件 <https://github.com/ros2/rcl/tree/release-alpha3/rcl/include/rcl>`__。

* 在 rclcpp 中增加了对 TLSF（两级分离适配）分配器的支持，这是一种面向嵌入式和实时系统的内存分配器设计。
* 提高了 MultiThreadedExecutor 的效率，并修复了多线程执行的众多 bug（现在已在 CI 上测试）。
* 增加了从 spin 中调用的回调内部取消执行器的能力。
* 增加了定时器自我取消的能力，方法是支持接受自身引用作为函数参数的定时器回调。
* 增加了禁止多个线程进入 Executor::spin 的检查。
* 提高了许多偶发失败测试的可靠性。
* 增加了对使用 Fast RTPS（而不是例如 OpenSplice 或 Connext）的支持。
* 部分移植了 tf2，包括核心库和核心命令行工具。

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。

ROS 2 alpha2 版本（代号 *Baling wire*；2015 年 10 月）
------------------------------------------------------

.. contents:: 目录
   :local:

背景
^^^^

正如一篇 `设计
文章 <https://design.ros2.org/articles/why_ros2.html>`__ 所解释的，我们正在开发
ROS 的一个新主要版本，称为 "ROS 2"。虽然
底层概念（例如发布 / 订阅消息）和目标（例如
灵活性和可复用性）与 ROS 1 相同，但我们借此
机会对系统进行重大更改，包括更改
一些核心 API。
如需更深入地了解这些更改及其
理由，请参阅其他 `ROS 2 设计
文章 <https://design.ros2.org>`__。


状态
^^^^

2015 年 11 月 3 日，我们发布了 ROS 2 alpha2，
代号 **Baling wire**。
此版本的主要目标是添加更多功能，同时处理我们在之前 alpha 1 版本中收到的反馈。
为此，我们构建了一组 `演示 <../../Tutorials>`，它们
展示了 ROS 2 的一些关键功能。
我们鼓励你尝试那些
演示，查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们特别想知道我们在多大程度上（或多差地）
满足了对你们重要的用例。


目标受众
^^^^^^^^

虽然欢迎大家尝试演示并浏览代码，但此版本面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀疏，系统的许多内容都是通过与 ROS 1 的对比来说明的。


范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未
完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该期望尝试一些演示，探索代码，也许还可以编写
自己的演示。

此版本中包含的主要功能有：


* 支持 rclcpp 中的自定义分配器，适用于实时消息传递
* Windows 与 Linux/OSX 的功能对等，包括工作区管理、服务和参数
* rclcpp API 改进
* FreeRTPS 改进

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。

ROS 2 alpha1 版本（代号 *Anchor*；2015 年 8 月）
------------------------------------------------

.. contents:: 目录
   :local:

背景
^^^^

正如一篇 `设计
文章 <https://design.ros2.org/articles/why_ros2.html>`__ 所解释的，我们正在开发
ROS 的一个新主要版本，称为 "ROS 2"。虽然
底层概念（例如发布 / 订阅消息）和目标（例如
灵活性和可复用性）与 ROS 1 相同，但我们借此
机会对系统进行重大更改，包括更改
一些核心 API。
如需更深入地了解这些更改及其
理由，请参阅其他 `ROS 2 设计
文章 <https://design.ros2.org>`__。


状态
^^^^

2015 年 8 月 31 日，我们发布了 ROS 2 alpha1，
代号 **Anchor**。
此版本的主要目标是给你
机会去了解 ROS 2 的工作原理，特别是它与
ROS 1 的区别。
为此，我们构建了一组 `演示 <../../Tutorials>`，它们
展示了 ROS 2 的一些关键功能。
我们鼓励你尝试那些
演示，查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们特别想知道我们在多大程度上（或多差地）
满足了对你们重要的用例。


目标受众
^^^^^^^^

虽然欢迎大家尝试演示并浏览代码，但此版本面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀疏，系统的许多内容都是通过与 ROS 1 的对比来说明的。


范围
^^^^

正如 "alpha" 限定词所暗示的，此版本的 ROS 2 远未
完成。
你不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该期望尝试一些演示，探索代码，也许还可以编写
自己的演示。

此版本中包含的主要功能有：


* 发现、传输和序列化 `使用 DDS <https://design.ros2.org/articles/ros_on_dds.html>`__
* 支持 `多个 DDS 厂商 <https://design.ros2.org/articles/ros_on_dds.html#vendors-and-licensing>`__
* 支持消息原语：话题（发布 / 订阅）、服务（请求 / 响应）和参数
* 支持 Linux (Ubuntu Trusty)、OS X (Yosemite) 和 Windows (8)
* `使用服务质量设置处理有损网络 <../Tutorials/Demos/Quality-of-Service>`
* `使用相同 API 进行进程间或进程内通信 <../Tutorials/Demos/Intra-Process-Communication>`
* `编写使用 ROS 2 API 的实时安全代码 <../Tutorials/Demos/Real-Time-Programming>`
* `在 "裸机" 微控制器（无操作系统）上运行 ROS 2 <https://github.com/ros2/freertps/wiki>`__
* `桥接 ROS 1 和 ROS 2 之间的通信 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__

上面未列出的任何内容基本上都不包含在此版本中。
下一步在 `路线图 <../../The-ROS2-Project/Roadmap>` 中描述。
