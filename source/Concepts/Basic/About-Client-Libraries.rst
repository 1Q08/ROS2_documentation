.. redirect-from::

   Concepts/About-Client-Interfaces
   Concepts/About-ROS-2-Client-Libraries

.. include:: ../../../global_substitutions.txt

客户端库
========

.. contents:: 目录
   :local:

概述
----

客户端库是允许用户实现其 ROS 2 代码的 API。
通过使用客户端库，用户可以访问 ROS 2 的概念，例如节点、话题、服务等。
客户端库有多种编程语言版本，因此用户可以用最适合其应用的语言编写 ROS 2 代码。
例如，你可能更喜欢用 Python 编写可视化工具，因为它能让原型迭代更快；而对于系统中关注效率的部分，节点用 C++ 实现可能更好。

使用不同客户端库编写的节点能够互相共享消息，因为所有客户端库都实现了代码生成器，使用户能够在相应语言中与 ROS 2 接口文件进行交互。

除了特定语言的通信工具外，客户端库还向用户暴露了使 ROS 成为“ROS”的核心功能。
例如，以下是通常可以通过客户端库访问的功能列表：

* 名称与命名空间
* 时间（真实或仿真）
* 参数
* 控制台日志记录
* 线程模型
* 进程内通信

受支持的客户端库
----------------

C++ 客户端库（``rclcpp``）和 Python 客户端库（``rclpy``）都是利用 ``rcl`` 中通用功能的客户端库。

``rclcpp`` 包
~~~~~~~~~~~~~

ROS C++ 客户端库（``rclcpp``）是面向用户的、符合 C++ 习惯的接口，它提供了所有 ROS 客户端功能，例如创建节点、发布者和订阅。
``rclcpp`` 构建在 ``rcl`` 和 ``rosidl`` |API| 之上，并且设计用于与 ``rosidl_generator_cpp`` 生成的 C++ 消息配合使用。

``rclcpp`` 利用了 C++ 和 C++17 的所有特性，使接口尽可能易用，但由于它复用了 ``rcl`` 中的实现，因此能够与使用 ``rcl`` |API| 的其他客户端库保持一致的行为。

``rclcpp`` 仓库位于 GitHub 上的 `ros2/rclcpp <https://github.com/ros2/rclcpp>`_，其中包含 |package| ``rclcpp``。
生成的 |API| 文档位于 {package_link(rclcpp)}。

``rclpy`` 包
~~~~~~~~~~~~

ROS Python 客户端库（``rclpy``）是 C++ 客户端库的 Python 对应版本。
与 C++ 客户端库一样，``rclpy`` 的实现也构建在 ``rcl`` C API 之上。
该接口提供了符合 Python 习惯的体验，使用原生 Python 类型和模式，例如列表和上下文对象。
通过在实现中使用 ``rcl`` |API|，它在功能对等和行为方面与其他客户端库保持一致。
除了围绕 ``rcl`` |API| 提供符合 Python 习惯的绑定、以及为每条消息提供 Python 类之外，Python 客户端库还负责执行模型，使用 ``threading.Thread`` 或类似机制来运行 ``rcl`` |API| 中的函数。

与 C++ 一样，它为用户交互的每条 ROS 消息生成自定义的 Python 代码；但与 C++ 不同的是，它最终会将原生的 Python 消息对象转换为 C 版本的消息。
所有操作都在 Python 版本的消息上进行，直到需要将其传入 ``rcl`` 层时，才将其转换为普通 C 版本的消息，以便传入 ``rcl`` C |API|。
在同一进程中的发布者和订阅之间通信时，会尽可能避免这种转换，以减少 Python 进出转换的开销。

``rclpy`` 仓库位于 GitHub 上的 `ros2/rclpy <https://github.com/ros2/rclpy>`_，其中包含 |package| ``rclpy``。
生成的 |API| 文档位于 {package_link(rclpy)}。

社区维护的客户端库
~~~~~~~~~~~~~~~~~~

虽然 C++ 和 Python 客户端库由 ROS 2 核心团队维护，但 ROS 2 社区的成员也维护了额外的客户端库：

* `Ada <https://github.com/ada-ros/ada4ros2>`__  这是一组包（绑定 ``rcl``、消息生成器、绑定 ``tf2``、示例和教程），允许使用 Ada 编写 ROS 2 应用程序。
* `C <https://github.com/ros2/rclc>`__  ``rclc`` 不在 rcl 之上再加一层，而是对 rcl 进行补充，使 rcl+rclc 成为一个功能完整的 C 语言客户端库。教程请参阅 `micro.ros.org <https://micro.ros.org/>`__。
* `JVM 与 Android <https://github.com/ros2-java>`__ 用于 ROS 2 的 Java 和 Android 绑定。
* `.NET Core、UWP 与 C# <https://github.com/esteve/ros2_dotnet>`__ 这是一组项目（绑定、代码生成器、示例等），用于为 .NET Core 和 .NET Standard 编写 ROS 2 应用程序。
* `Node.js <https://www.npmjs.com/package/rclnodejs>`__ rclnodejs 是一个用于 ROS 2 的 Node.js 客户端。
  它为 ROS 2 编程提供了简单易用的 JavaScript API。
* `Rust <https://github.com/ros2-rust/ros2_rust>`__ 这是一组项目（rclrs 客户端库、代码生成器、示例等），使开发者能够用 Rust 编写 ROS 2 应用程序。
* `Flutter 与 Dart <https://github.com/rcldart>`__ 用于 ROS 2 的 Flutter 和 Dart 绑定。

较旧、不再维护的客户端库有：

* `C# <https://github.com/firesurfer/rclcs>`__
* `Objective C 与 iOS <https://github.com/esteve/ros2_objc>`__
* `Zig <https://github.com/jacobperron/rclzig>`__


通用功能：``rcl``
-----------------

客户端库中的大部分功能并非特定于客户端库的编程语言。
例如，参数的行为和命名空间的逻辑理想情况下应在所有编程语言中保持一致。
因此，客户端库不是从头实现通用功能，而是使用一个通用的核心 ROS 客户端库（RCL）接口，该接口实现了 ROS 概念中与语言无关的逻辑和行为。
这样一来，客户端库只需用外部函数接口包装 RCL 中的通用功能。
这使得客户端库更轻薄、更易于开发。
出于这个原因，通用 RCL 功能通过 C 接口暴露，因为 C 语言通常是客户端库最容易包装的语言。

除了使客户端库更轻量之外，拥有通用核心的另一个优点是各语言之间的行为更加一致。
如果对核心 RCL 中功能的逻辑/行为进行了任何更改——例如命名空间——所有使用该 RCL 的客户端库都会反映这些更改。
此外，拥有通用核心意味着在修复 bug 时，维护多个客户端库的工作量更少。

``rcl`` 的 API 文档可以在 `这里 <{package_link(rcl)}>`__ 找到。

特定语言的功能
--------------

需要特定语言特性/属性的客户端库概念不在 RCL 中实现，而是在每个客户端库中实现。
例如，“spin”函数使用的线程模型会有特定于客户端库语言的实现。

演示
----

要了解使用 ``rclpy`` 的发布者与使用 ``rclcpp`` 的订阅之间消息交换的完整过程，我们鼓励你观看 `这个 ROSCon 演讲 <https://vimeo.com/187696091>`__，从 17:25 开始（`幻灯片见这里 <https://roscon.ros.org/2016/presentations/ROSCon%202016%20-%20ROS%202%20Update.pdf>`__）。

与 ROS 1 的比较
---------------

在 ROS 1 中，所有客户端库都是“从零开始”开发的。
例如，这使得 ROS 1 的 Python 客户端库可以纯粹用 Python 实现，从而带来诸如无需编译代码等好处。
然而，各客户端库之间的命名约定和行为并不总是一致，bug 修复必须在多个地方进行，而且有大量功能只在一个客户端库中实现过（例如 UDPROS）。

总结
----

通过利用通用的核心 ROS 客户端库，用各种编程语言编写的客户端库更容易编写，且行为更加一致。
