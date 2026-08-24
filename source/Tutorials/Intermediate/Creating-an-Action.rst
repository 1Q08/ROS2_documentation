.. redirect-from::

    Tutorials/Actions/Creating-an-Action

.. _ActionCreate:

创建一个 action
===============

**目标：** 在 ROS 2 软件包中定义一个 action。

**教程级别：** 中级

**时间：** 5 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

你之前在 :doc:`../Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions` 教程中学习过 action。
与其他通信类型及其各自的接口（topics/msg 和 services/srv）一样，
你也可以在软件包中自定义 action。
本教程展示如何定义和构建一个 action，以便在下一个教程中与你要编写的 action 服务器和 action 客户端一起使用。

前提条件
--------

你应该已安装 :doc:`ROS 2 <../../Installation>` 和 `colcon <https://colcon.readthedocs.org>`__。

你应该知道如何设置 :doc:`工作空间 <../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace>` 并创建软件包。

请记得先 :doc:`source 你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`。

任务
----

1 创建接口软件包
^^^^^^^^^^^^^^^^

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ mkdir -p ~/ros2_ws/src # 你可以复用现有的同名工作空间
      $ cd ~/ros2_ws/src
      $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces

  .. group-tab:: macOS

    .. code-block:: console

      $ mkdir -p ~/ros2_ws/src
      $ cd ~/ros2_ws/src
      $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces

  .. group-tab:: Windows

    .. code-block:: console

      $ md \ros2_ws\src
      $ cd \ros2_ws\src
      $ ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces

``custom_action_interfaces`` 是新软件包的名称。
请注意，它只能是（也只能是）一个 CMake 软件包，但这并不限制你可以在哪些类型的软件包中使用你的 action。
创建新 ROS 2 软件包时，``--build-type ament_cmake`` 标志在很大程度上是可选的，但为了完整起见，我们在这里包含它。
你可以在 CMake 软件包中创建自己的自定义接口，然后在 C++ 或 Python 节点中使用它。

.. note::

  将 ``.msg``、``.srv`` 和 ``.action`` 文件放在与使用它们的节点分开的软件包中是一个好习惯。
  这样可以更方便地跨不同软件包复用接口定义。


2 定义一个 action
^^^^^^^^^^^^^^^^^

action 定义在 ``.action`` 文件中，格式如下：

.. code-block:: bash

    # 请求
    ---
    # 结果
    ---
    # 反馈

一个 action 定义由三个用 ``---`` 分隔的消息定义组成。

- 一个 *请求* 消息从 action 客户端发送到 action 服务器，用于启动一个新目标。
- 一个 *结果* 消息在目标完成时从 action 服务器发送到 action 客户端。
- *反馈* 消息定期从 action 服务器发送到 action 客户端，携带关于目标的最新更新。

一个 action 的实例通常被称为一个 *目标*。

假设我们想定义一个新的 action “Fibonacci”，用于计算 `斐波那契数列 <https://en.wikipedia.org/wiki/Fibonacci_number>`__。

在我们的 ROS 2 软件包 ``custom_action_interfaces`` 中创建一个 ``action`` 目录：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ cd custom_action_interfaces
      $ mkdir action

  .. group-tab:: macOS

    .. code-block:: console

      $ cd custom_action_interfaces
      $ mkdir action

  .. group-tab:: Windows

    .. code-block:: console

      $ cd custom_action_interfaces
      $ md action

在 ``action`` 目录内，创建一个名为 ``Fibonacci.action`` 的文件，内容如下：

.. code-block:: bash

  int32 order
  ---
  int32[] sequence
  ---
  int32[] partial_sequence

目标请求是我们想计算的斐波那契数列的 ``order``，结果是最终的 ``sequence``，反馈是到目前为止计算出的 ``partial_sequence``。

3 构建一个 action
^^^^^^^^^^^^^^^^^

在代码中使用新的 Fibonacci action 类型之前，我们必须将定义传递给 rosidl 代码生成流程。

通过在 ``ament_package()`` 行之前向 ``CMakeLists.txt`` 添加以下行来实现：

.. code-block:: cmake

    find_package(rosidl_default_generators REQUIRED)

    rosidl_generate_interfaces(${PROJECT_NAME}
      "action/Fibonacci.action"
    )

我们还应该向 ``package.xml`` 添加所需的依赖项：

.. code-block:: xml

    <buildtool_depend>rosidl_default_generators</buildtool_depend>

    <member_of_group>rosidl_interface_packages</member_of_group>

现在我们应该能够构建包含 ``Fibonacci`` action 定义的软件包：

.. code-block:: console

    $ cd ~/ros2_ws # 切换到工作空间的根目录
    $ colcon build # 构建

完成！

按照惯例，action 类型将以其软件包名称和单词 ``action`` 作为前缀。
所以当我们想引用新 action 时，它的全名将是 ``custom_action_interfaces/action/Fibonacci``。

我们可以用命令行工具检查 action 是否构建成功。
首先 source 我们的工作空间：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ source install/local_setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ source install/local_setup.console

  .. group-tab:: Windows

    .. code-block:: console

      $ call install\local_setup.bat

现在检查我们的 action 定义是否存在：

.. code-block:: console

   $ ros2 interface show custom_action_interfaces/action/Fibonacci

你应该能看到 Fibonacci action 定义打印到屏幕上。

小结
----

在本教程中，你学习了 action 定义的结构。
你还学习了如何使用 ``CMakeLists.txt`` 和 ``package.xml`` 正确构建新的 action 接口，
以及如何验证构建成功。

后续步骤
--------

接下来，让我们通过创建 action 服务和客户端来使用你新定义的 action 接口（用 :doc:`Python <Writing-an-Action-Server-Client/Py>` 或 :doc:`C++ <Writing-an-Action-Server-Client/Cpp>`）。

相关内容
--------

有关 ROS action 的更多详细信息，请参阅 `设计文章 <http://design.ros2.org/articles/actions.html>`__。
