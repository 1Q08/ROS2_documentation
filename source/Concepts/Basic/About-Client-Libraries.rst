.. redirect-from::

   Concepts/About-Client-Interfaces
   Concepts/About-ROS-2-Client-Libraries

.. include:: ../../../global_substitutions.txt

客户端库
========

.. contents:: 目录
   :local:

概览
----

客户端库是允许用户实现 ROS 2 代码的 API。
通过客户端库，用户可以访问 ROS 2 的核心概念，例如节点、主题、服务等。
客户端库支持多种编程语言，因此用户可以用最适合自己应用场景的语言来编写 ROS 2 代码。
例如，您可能更喜欢在 Python 中编写可视化工具，因为这能更快完成原型迭代；而对于系统中对效率更敏感的部分，节点可能更适合用 C++ 实现。

使用不同客户端库编写的节点能够相互共享消息，因为所有客户端库都会实现代码生成器，让用户能够以各自语言与 ROS 2 接口文件进行交互。

除了语言特定的通信工具外，客户端库还向用户暴露 ROS 之所以为 ROS 的核心功能。
例如，下面是一组通常可以通过客户端库访问的功能：

* 名称与命名空间
* 时间（真实时间或仿真时间）
* 参数
* 控制台日志
* 线程模型
* 进程内通信

支持的客户端库
--------------

C++ 客户端库（``rclcpp``）和 Python 客户端库（``rclpy``）都属于利用 ``rcl`` 中公共功能的客户端库。

``rclcpp`` 包
~~~~~~~~~~~~~

ROS C++ 客户端库（``rclcpp``）是面向用户的、符合 C++ 风格的接口，提供了创建节点、发布者和订阅者等全部 ROS 客户端功能。
``rclcpp`` 建立在 ``rcl`` 和 ``rosidl`` |API| 之上，并且设计为与 ``rosidl_generator_cpp`` 生成的 C++ 消息一起使用。

``rclcpp`` 充分使用了 C++ 与 C++17 的特性，以尽可能让接口更易用；但由于它复用了 ``rcl`` 中的实现，因此能够与其他使用 ``rcl`` |API| 的客户端库保持一致的行为。

``rclcpp`` 仓库位于 GitHub 上的 `ros2/rclcpp <https://github.com/ros2/rclcpp>`_，包含 |package| ``rclcpp``。
生成的 |API| 文档位于 {package_link(rclcpp)}。

``rclpy`` 包
~~~~~~~~~~~~

ROS Python 客户端库（``rclpy``）是 C++ 客户端库在 Python 中的对应实现。
与 C++ 客户端库一样，``rclpy`` 同样建立在 ``rcl`` 的 C API 之上来实现。
该接口提供了原生 Python 体验，使用了 Python 原生类型与模式，例如列表和上下文对象。
通过在实现中复用 ``rcl`` |API|，它在功能一致性和行为表现上能保持与其他客户端库一致。
除了围绕 ``rcl`` |API| 提供 Python 风格绑定，以及为每条消息生成 Python 类外，Python 客户端库还负责执行模型，使用 ``threading.Thread`` 或类似机制来运行 ``rcl`` |API| 中的函数。

与 C++ 一样，它会为用户与之交互的每条 ROS 消息生成自定义 Python 代码，但与 C++ 不同的是，最终会将原生 Python 消息对象转换为消息的 C 版本。
所有操作都会先在 Python 版本的消息对象上进行，直到需要传入 ``rcl`` 层时，才会再转换为普通的 C 版本消息对象，以便通过 ``rcl`` C |API| 传递。
在同一进程内的发布者与订阅者通信时，若可能则会避免这种来回转换，以减少 Python 和 C 之间的转换开销。

``rclpy`` 仓库位于 GitHub 上的 `ros2/rclpy <https://github.com/ros2/rclpy>`_，包含 |package| ``rclpy``。
生成的 |API| 文档位于 {package_link(rclpy)}。

社区维护版
~~~~~~~~~~

尽管 C++ 和 Python 客户端库由 ROS 2 核心团队维护，但 ROS 2 社区成员也维护着额外的客户端库：

* `Ada <https://github.com/ada-ros/ada4ros2>`__  这是一个软件包集合（绑定 ``rcl``、消息生成器、绑定 ``tf2``，以及示例与教程），用于编写 Ada 应用程序来使用 ROS 2。
* `C <https://github.com/ros2/rclc>`__  ``rclc`` 不会在 ``rcl`` 之上再放一层抽象，而是与 ``rcl`` 互补，形成一个功能完整的 C 客户端库。相关教程可见 `micro.ros.org <https://micro.ros.org/>`__。
* `JVM 和 Android <https://github.com/ros2-java>`__ Java 和 Android 绑定。
* `.NET Core, UWP 和 C# <https://github.com/esteve/ros2_dotnet>`__ 这是一个项目集合（绑定、代码生成器、示例和更多内容），用于用 .NET Core 和 .NET Standard 编写 ROS 2 应用。
* `Node.js <https://www.npmjs.com/package/rclnodejs>`__ rclnodejs 是 ROS 2 的 Node.js 客户端。
  它提供了简单易用的 JavaScript API 来编写 ROS 2 程序。
* `Rust <https://github.com/ros2-rust/ros2_rust>`__ 这是一个项目集合（rclrs 客户端库、代码生成器、示例和更多内容），用于让开发者用 Rust 编写 ROS 2 应用。
* `Flutter 和 Dart <https://github.com/rcldart>`__ Flutter 与 Dart 绑定。

旧版、已不再维护的客户端库包括：

* `C# <https://github.com/firesurfer/rclcs>`__
* `Objective C 和 iOS <https://github.com/esteve/ros2_objc>`__
* `Zig <https://github.com/jacobperron/rclzig>`__


公共功能：``rcl``
-----------------

客户端库中大部分功能并不特定于某种编程语言。
例如，参数的行为与命名空间的逻辑理想上应该在所有编程语言中保持一致。
因此，客户端库并不会从零开始实现这些公共功能，而是利用一个共享的核心 ROS 客户端库（RCL）接口来实现语言无关的 ROS 概念逻辑与行为。
结果就是，客户端库只需用外部函数接口（FFI）把这些公共功能包起来即可。
这使得客户端库更轻量、也更容易开发。
因此，公共的 RCL 功能以 C 接口暴露出来，因为 C 语言通常是客户端库最容易包装的语言。

除了使客户端库轻量化之外，公共核心的另一个优势是不同语言间的行为会更一致。
如果对核心 RCL 中功能的逻辑/行为做出改动——比如命名空间——那么所有使用该 RCL 的客户端库都会反映出这些变化。
此外，拥有公共核心意味着在修复 bug 时，维护多个客户端库的成本也会更低。

``rcl`` 的 API 文档可在 `这里 <{package_link(rcl)}>`__ 查阅。

语言特定功能
------------

那些需要语言特定特性/属性的客户端库概念并不在 RCL 中实现，而是由各个客户端库分别实现。
例如，用于 ``spin`` 函数的线程模型，会有与客户端库语言相匹配的实现。

示例
----

若要了解使用 ``rclpy`` 的发布者与使用 ``rclcpp`` 的订阅者之间消息交换的演示过程，建议观看 `这场 ROSCon 演讲 <https://vimeo.com/187696091>`__，从 17:25 开始（可在 `此处查看幻灯片 <https://roscon.ros.org/2016/presentations/ROSCon%202016%20-%20ROS%202%20Update.pdf>`__）。

与 ROS 1 的比较
---------------

在 ROS 1 中，所有客户端库都是“从零开始”开发的。
这让 ROS 1 的 Python 客户端库能够纯粹用 Python 实现，例如无需编译代码。
然而，命名约定和行为在不同客户端库之间并不总是保持一致，bug 修复必须在多个地方做，而且有大量功能只在一个客户端库中实现过（例如 UDPROS）。

总结
----

通过复用公共核心 ROS 客户端库，不同编程语言编写的客户端库会更容易实现，并具有更一致的行为。
