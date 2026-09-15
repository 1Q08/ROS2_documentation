.. redirect-from::

   Alpha-Overview

Alpha 发行版
============

.. contents:: 目录
   :depth: 2
   :local:

这是此前分列的 8 个 ROS 2 alpha 发行版页面的合并版本。

我们希望你能试用它们并 `提供反馈 <../../Contact>`。

ROS 2 alpha8 发行版（代号 *Hook-and-Loop*；2016 年 10 月）
----------------------------------------------------------

受支持 DDS 供应商的变更
^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 支持多种中间件实现（更多详情请参阅 `此页面 <../../Concepts/Intermediate/About-Different-Middleware-Vendors>`）。
在 Alpha 8 之前，ROS 2 为 eProsima 的 Fast RTPS、RTI 的 Connext 和 PrismTech 的 OpenSplice 提供 ROS 中间件实现支持。
为了集中力量，从 Alpha 8 起，将支持 Fast RTPS 和 Connext（静态），并以 Fast RTPS（`现已采用 Apache 2.0 许可 <http://www.eprosima.com/index.php/company-all/news/61-eprosima-goes-apache>`__）作为默认实现发布。

范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未完成。
不应期望从 ROS 1 切换到 ROS 2，也不应期望用 ROS 2 构建新的机器人控制系统。
相反，你应该尝试一些演示、浏览代码，也许还可以编写自己的演示。

本次发行包含的改进有：


* Fast RTPS 及其 rmw 实现的若干改进

  * 在 Fast RTPS 中支持大型（图像）消息
  * Fast RTPS 中的 ``wait_for_service`` 功能

* 在 Python 和 C 中支持所有 ROS 2 消息类型
* 在 Python 中增加了对服务质量（QoS）设置的支持
* 修复了上一个 alpha 发行版中的多个缺陷

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。

ROS 2 alpha7 发行版（代号 *Glue Gun*\ ；2016 年 7 月）
------------------------------------------------------

.. contents:: 目录
   :local:

需要更新的 Ubuntu 版本
^^^^^^^^^^^^^^^^^^^^^^

在 Alpha 6 之前，ROS 2 面向 Ubuntu Trusty Tahr（14.04）。从本次 Alpha 起，ROS 2 面向 Ubuntu Xenial Xerus（16.04），以便受益于更新版本的编译器、CMake、Python 等。

范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未完成。
不应期望从 ROS 1 切换到 ROS 2，也不应期望用 ROS 2 构建新的机器人控制系统。
相反，你应该尝试一些演示、浏览代码，也许还可以编写自己的演示。

本次发行包含的主要特性有：


* 图 API 功能：wait_for_service

  * 在 rclcpp 中增加了接口，并在示例、演示和测试中使用它们

* 改进了 Connext 和 Fast-RTPS 中对大型消息的支持（Fast-RTPS 为部分支持）
* 使用从 ROS 1 移植的代码实现的 Turtlebot 演示

  * 参见：https://github.com/ros2/turtlebot2_demo

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。

ROS 2 alpha6 发行版（代号 *Fastener*；2016 年 6 月）
----------------------------------------------------

.. contents:: 目录
   :local:

范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未
完成。
不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该尝试一些演示、浏览代码，也许还可以编写
自己的演示。

本次发行包含的主要特性有：


* 图 API 功能：wait_for_service

  * 为节点增加了用于等待图变化的图保护条件
  * 增加了 ``rmw_service_server_is_available``，用于验证服务是否可用

* 重构了 ``rclcpp`` 以使用 ``rcl``
* 改进了 Python 中对复杂消息类型的支持

  * 嵌套消息
  * 数组
  * 字符串

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。

ROS 2 alpha5 发行版（代号 *Epoxy*；2016 年 4 月）
-------------------------------------------------

.. contents:: 目录
   :local:


范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未
完成。
不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该尝试一些演示、浏览代码，也许还可以编写
自己的演示。

本次发行包含的主要特性有：


* 在 Fast RTPS 和 Connext Dynamic rmw 实现中支持 C 数据结构。
* 在 C 中支持服务。
* 增加了对 32 位和 64 位 ARM 的实验性平台支持。

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。

ROS 2 alpha4 发行版（代号 *Duct tape*；2016 年 2 月）
-----------------------------------------------------

.. contents:: 目录
   :local:

背景
^^^^

正如 `设计文章 <https://design.ros2.org/articles/why_ros2.html>`__ 中所述，
我们正在开发 ROS 的一个新的主版本，称为 "ROS 2"。
虽然底层概念（例如发布/订阅消息传递）和目标
（例如灵活性与可重用性）与 ROS 1 相同，但我们借此
机会对系统进行重大改动，包括更改
一些核心 API。
有关这些改动及其理由的更深入论述，请参阅其他
`ROS 2 设计文章 <https://design.ros2.org>`__。

状态
^^^^

2016 年 2 月 17 日，我们发布 ROS 2 alpha4，
代号 **Duct tape**。
本次发行的主要目标是增加更多功能，同时处理此前各发行版收到的反馈。
为此，我们构建了一组 `演示 <../../Tutorials>`，用于
展示 ROS 2 的一些关键特性。
我们鼓励你尝试这些
演示、查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们尤其希望了解我们对那些
对你很重要的用例处理得有多好（或多差）。

目标读者
^^^^^^^^

虽然欢迎所有人尝试演示并浏览代码，但本次发行面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀少，系统的许多部分是通过与 ROS 1 的对比来解释的。

范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未
完成。
不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该尝试一些演示、浏览代码，也许还可以编写
自己的演示。

本次发行包含的主要特性有：


* 改进的类型支持基础设施，包括对 C 的支持
* 初步的 Python 客户端库，仅支持发布者和订阅。注意，该 API 可能会变化且远未完成！
* 在 C API 中增加了 ROS 时间结构（仍需要 C++ API）

  * 为 ROS 时间引入了可扩展“时间源”的新概念，默认时间源将与 ROS 1 类似（实现待完成）

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。

ROS 2 alpha3 发行版（代号 *Cement*；2015 年 12 月）
---------------------------------------------------

.. contents:: 目录
   :local:


背景
^^^^

正如 `设计文章 <https://design.ros2.org/articles/why_ros2.html>`__ 中所述，
我们正在开发 ROS 的一个新的主版本，称为 "ROS 2"。
虽然底层概念（例如发布/订阅消息传递）和目标
（例如灵活性与可重用性）与 ROS 1 相同，但我们借此
机会对系统进行重大改动，包括更改
一些核心 API。
有关这些改动及其理由的更深入论述，请参阅其他
`ROS 2 设计文章 <https://design.ros2.org>`__。

状态
^^^^

2015 年 12 月 18 日，我们发布 ROS 2 alpha3，
代号 **Cement**。
本次发行的主要目标是增加更多功能，同时处理此前各发行版收到的反馈。
为此，我们构建了一组 `演示 <../../Tutorials>`，用于
展示 ROS 2 的一些关键特性。
我们鼓励你尝试这些
演示、查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们尤其希望了解我们对那些
对你很重要的用例处理得有多好（或多差）。

目标读者
^^^^^^^^

虽然欢迎所有人尝试演示并浏览代码，但本次发行面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀少，系统的许多部分是通过与 ROS 1 的对比来解释的。

范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未
完成。
不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该尝试一些演示、浏览代码，也许还可以编写
自己的演示。

本次发行包含的主要特性有：


* 更新了 ``rcl`` 接口。

  * 将对该接口进行封装以创建语言绑定，例如 ``rclpy``。
  * 与我们目前现有的接口（例如 ``rmw`` 和 ``rclcpp``）相比，该接口具备更好的文档和测试覆盖率。
  * 参见 `rcl 头文件 <https://github.com/ros2/rcl/tree/release-alpha3/rcl/include/rcl>`__。

* 在 rclcpp 中增加了对使用 TLSF（两级隔离适配）分配器的支持，这是一种为嵌入式和实时系统设计的内存分配器。
* 提高了 MultiThreadedExecutor 的效率，并修复了多线程执行中的众多缺陷，现已在 CI 上进行测试。
* 增加了在 spin 中调用的回调内取消 Executor 的能力。
* 增加了定时器自我取消的能力，方法是支持定时器回调接受对其自身的引用作为函数参数。
* 增加了禁止多个线程进入 Executor::spin 的检查。
* 提高了众多此前偶发失败的测试的可靠性。
* 增加了对使用 Fast RTPS（而不是例如 OpenSplice 或 Connext）的支持。
* 部分移植了 tf2，包括核心库和核心命令行工具。

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。

ROS 2 alpha2 发行版（代号 *Baling wire*；2015 年 10 月）
--------------------------------------------------------

.. contents:: 目录
   :local:

背景
^^^^

正如 `设计
文章 <https://design.ros2.org/articles/why_ros2.html>`__ 中所述，我们正在
开发 ROS 的一个新的主版本，称为 "ROS 2"。虽然其
底层概念（例如发布/订阅消息传递）和目标（例如
灵活性与可重用性）与 ROS 1 相同，但我们借此
机会对系统进行重大改动，包括更改
一些核心 API。
有关这些改动及其
理由的更深入论述，请参阅其他 `ROS 2 设计
文章 <https://design.ros2.org>`__。


状态
^^^^

2015 年 11 月 3 日，我们发布 ROS 2 alpha2，
代号 **Baling wire**。
本次发行的主要目标是增加更多功能，同时处理此前 alpha 1 发行版收到的反馈。
为此，我们构建了一组 `演示 <../../Tutorials>`，用于
展示 ROS 2 的一些关键特性。
我们鼓励你尝试这些
演示、查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们尤其希望了解我们对那些
对你很重要的用例处理得有多好（或多差）。


目标读者
^^^^^^^^

虽然欢迎所有人尝试演示并浏览代码，但本次发行面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀少，系统的许多部分是通过与 ROS 1 的对比来解释的。


范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未
完成。
不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该尝试一些演示、浏览代码，也许还可以编写
自己的演示。

本次发行包含的主要特性有：


* 在 rclcpp 中支持自定义分配器，适用于实时消息传递
* Windows 与 Linux/OSX 的功能对等，包括工作空间管理、服务和参数
* rclcpp API 改进
* FreeRTPS 改进

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。

ROS 2 alpha1 发行版（代号 *Anchor*；2015 年 8 月）
--------------------------------------------------

.. contents:: 目录
   :local:

背景
^^^^

正如 `设计
文章 <https://design.ros2.org/articles/why_ros2.html>`__ 中所述，我们正在
开发 ROS 的一个新的主版本，称为 "ROS 2"。虽然其
底层概念（例如发布/订阅消息传递）和目标（例如
灵活性与可重用性）与 ROS 1 相同，但我们借此
机会对系统进行重大改动，包括更改
一些核心 API。
有关这些改动及其
理由的更深入论述，请参阅其他 `ROS 2 设计
文章 <https://design.ros2.org>`__。


状态
^^^^

2015 年 8 月 31 日，我们发布 ROS 2 alpha1，
代号 **Anchor**。
本次发行的主要目标是让你有机会理解 ROS 2 的工作方式，特别是它与 ROS 1 的差异。
为此，我们构建了一组 `演示 <../../Tutorials>`，用于
展示 ROS 2 的一些关键特性。
我们鼓励你尝试这些
演示、查看实现它们的代码，并 `提供
反馈 <../../Contact>`。
我们尤其希望了解我们对那些
对你很重要的用例处理得有多好（或多差）。


目标读者
^^^^^^^^

虽然欢迎所有人尝试演示并浏览代码，但本次发行面向已经具备 ROS 1 开发经验的人。
目前，ROS 2 文档还相当稀少，系统的许多部分是通过与 ROS 1 的对比来解释的。


范围
^^^^

正如 "alpha" 这一限定词所暗示的，此版本的 ROS 2 远未
完成。
不应期望从 ROS 1 切换到 ROS 2，也不应
期望用 ROS 2 构建新的机器人控制系统。
相反，你
应该尝试一些演示、浏览代码，也许还可以编写
自己的演示。

本次发行包含的主要特性有：


* 发现、传输和序列化 `使用 DDS <https://design.ros2.org/articles/ros_on_dds.html>`__
* 支持 `多种 DDS 供应商 <https://design.ros2.org/articles/ros_on_dds.html#vendors-and-licensing>`__
* 支持消息传递原语：话题（发布/订阅）、服务（请求/响应）和参数
* 支持 Linux（Ubuntu Trusty）、OS X（Yosemite）和 Windows（8）
* `使用服务质量设置处理有损网络 <../Tutorials/Demos/Quality-of-Service>`
* `使用相同的 API 进行进程间或进程内通信 <../Tutorials/Demos/Intra-Process-Communication>`
* `编写使用 ROS 2 API 的实时安全代码 <../Tutorials/Demos/Real-Time-Programming>`
* `在“裸机”微控制器（无操作系统）上运行 ROS 2 <https://github.com/ros2/freertps/wiki>`__
* `在 ROS 1 和 ROS 2 之间桥接通信 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__

除上面列出的内容外，本发行版基本不包含其他内容。
后续步骤在 `路线图 <../../The-ROS2-Project/Roadmap>` 中说明。
