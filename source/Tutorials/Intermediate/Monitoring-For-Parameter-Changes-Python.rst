监测参数变化（Python）
======================

**目标：** 学习使用 ParameterEventHandler 类来监测并响应参数变化。

**教程级别：** 中级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

节点通常需要响应其自身参数或其他节点参数的变化。
ParameterEventHandler 类可以方便地监听参数变化，从而使你的代码能够对其做出响应。
本教程将展示如何使用 Python 版本的 ParameterEventHandler 类来监测节点自身参数的变化以及其他节点参数的变化。

前提条件
--------

开始本教程之前，你应该先完成以下教程：

- :doc:`../Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters`
- :doc:`../Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python`

任务
----

在本教程中，你将创建一个新软件包来包含一些示例代码，编写一些使用 ParameterEventHandler 类的 Python 代码，并测试生成的代码。


1 创建软件包
^^^^^^^^^^^^

首先，打开一个新终端并 :doc:`source 你的 ROS 2 安装 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，使 ``ros2`` 命令能够正常工作。

按照 :ref:`这些说明 <new-directory>` 创建一个名为 ``ros2_ws`` 的新工作空间。

请记住，软件包应创建在 ``src`` 目录中，而不是工作空间的根目录。
因此，进入 ``ros2_ws/src``，然后在其中创建一个新软件包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_python --license Apache-2.0 python_parameter_event_handler --dependencies rclpy

你的终端将返回一条消息，确认你的软件包 ``python_parameter_event_handler`` 及其所有必要文件和文件夹已创建。

``--dependencies`` 参数将自动向 ``package.xml`` 和 ``CMakeLists.txt`` 添加必要的依赖行。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

由于你在创建软件包时使用了 ``--dependencies`` 选项，因此无需手动向 ``package.xml`` 添加依赖项。
但像往常一样，请务必向 ``package.xml`` 添加描述、维护者邮箱和姓名以及许可证信息。

.. code-block:: xml

  <description>Python parameter events client tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

2 编写 Python 节点
^^^^^^^^^^^^^^^^^^

在 ``ros2_ws/src/python_parameter_event_handler/python_parameter_event_handler`` 目录内，创建一个名为 ``parameter_event_handler.py`` 的新文件，并将以下代码粘贴到其中：

.. code-block:: Python

    import rclpy
    from rclpy.node import Node
    import rclpy.parameter

    from rclpy.parameter_event_handler import ParameterEventHandler


    class SampleNodeWithParameters(Node):
        def __init__(self):
            super().__init__('node_with_parameters')

            self.declare_parameter('an_int_param', 0)

            self.handler = ParameterEventHandler(self)

            self.callback_handle = self.handler.add_parameter_callback(
                parameter_name="an_int_param",
                node_name="node_with_parameters",
                callback=self.callback,
            )

        def callback(self, p: rclpy.parameter.Parameter) -> None:
            self.get_logger().info(f"Received an update to parameter: {p.name}: {rclpy.parameter.parameter_value_to_python(p.value)}")


    def main():
        rclpy.init()
        node = SampleNodeWithParameters()
        rclpy.spin(node)
        rclpy.shutdown()

2.1 检查代码
~~~~~~~~~~~~

顶部的 ``import`` 语句用于导入软件包依赖项。

.. code-block:: Python

    import rclpy
    from rclpy.node import Node
    import rclpy.parameter

    from rclpy.parameter_event_handler import ParameterEventHandler

下一段代码创建了类 ``SampleNodeWithParameters`` 及其构造函数。
该类的构造函数声明了一个整数参数 ``an_int_param``，默认值为 0。
接下来，代码创建了一个 ``ParameterEventHandler``，用于监测参数的变化。

.. code-block:: Python

    class SampleNodeWithParameters(Node):
        def __init__(self):
            super().__init__('node_with_parameters')

            self.declare_parameter('an_int_param', 0)

            self.handler = ParameterEventHandler(self)


最后，我们添加一个参数回调，并为新回调获取一个回调句柄。

.. note::

   保存 ``add_parameter_callback`` 返回的句柄非常重要；否则，回调将无法正确注册。

.. code-block:: Python

            self.callback_handle = self.handler.add_parameter_callback(
                parameter_name="an_int_param",
                node_name="node_with_parameters",
                callback=self.callback,
            )

对于回调函数，我们使用 ``SampleNodeWithParameters`` 类的 ``callback`` 方法。

.. code-block:: Python

        def callback(self, p: rclpy.parameter.Parameter) -> None:
            self.get_logger().info(f"Received an update to parameter: {p.name}: {rclpy.parameter.parameter_value_to_python(p.value)}")


在 ``SampleNodeWithParameters`` 之后是一个典型的 ``main`` 函数，它初始化 ROS，旋转示例节点以使其能够发送和接收消息，然后在用户在控制台输入 ^C 后关闭。

.. code-block:: Python

    def main():
        rclpy.init()
        node = SampleNodeWithParameters()
        rclpy.spin(node)
        rclpy.shutdown()


2.2 添加入口点
~~~~~~~~~~~~~~

打开 ``setup.py`` 文件。
同样，将 ``maintainer``、``maintainer_email``、``description`` 和 ``license`` 字段与你的 ``package.xml`` 保持一致：

.. code-block:: Python

    maintainer='YourName',
    maintainer_email='you@email.com',
    description='Python parameter tutorial',
    license='Apache-2.0',

在 ``entry_points`` 字段的 ``console_scripts`` 括号内添加以下行：

.. code-block:: Python

  entry_points={
      'console_scripts': [
          'node_with_parameters = python_parameter_event_handler.parameter_event_handler:main',
      ],
  },


3 构建并运行
^^^^^^^^^^^^

构建之前，最好在工作空间的根目录（``ros2_ws``）运行 ``rosdep`` 以检查缺失的依赖项：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ rosdep install -i --from-path src --rosdistro $ROS_DISTRO -y

   .. group-tab:: macOS

      rosdep 仅在 Linux 上运行，所以你可以跳到下一步。

   .. group-tab:: Windows

      rosdep 仅在 Linux 上运行，所以你可以跳到下一步。

返回到工作空间的根目录 ``ros2_ws``，并构建你的新软件包：

.. code-block:: console

    $ colcon build --packages-select python_parameter_event_handler

打开一个新终端，进入 ``ros2_ws``，并 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install\setup.bat

现在运行节点：

.. code-block:: console

     $ ros2 run python_parameter_event_handler node_with_parameters

节点现在处于活动状态，有一个参数，并且每当该参数更新时会打印一条消息。
为了测试这一点，打开另一个终端，像之前一样 source ROS 安装文件，并执行以下命令：

.. code-block:: console

    $ ros2 param set node_with_parameters an_int_param 43

运行节点的终端将显示类似以下内容的消息：

.. code-block:: console

    [INFO] [1698483083.315084660] [node_with_parameters]: Received an update to parameter: an_int_param: 43

我们之前在节点中设置的回调已被调用，并显示了更新后的值。
现在你可以使用 ^C 在终端中终止运行中的 parameter_event_handler 示例。

扩展
----

到目前为止，我们构建并测试了一个小节点，它监测节点自身拥有的单个参数。
以该节点为基础，下面展示 ParameterEventHandler 可以发挥作用的另外两种用例。

监测另一个节点的参数变化
^^^^^^^^^^^^^^^^^^^^^^^^

你还可以使用 ParameterEventHandler 来监测另一个节点参数的变化。
让我们更新 SampleNodeWithParameters 类，以监测另一个节点中参数的变化。
我们将使用 parameter_blackboard 演示应用程序来托管一个我们将监测其更新的 double 参数。

首先更新构造函数，在现有代码之后添加以下代码：

.. code-block:: Python

    def __init__(...):
        ...
        self.callback_handle2 = self.handler.add_parameter_callback(
            parameter_name="a_double_param",
            node_name="parameter_blackboard",
            callback=self.callback,
        )


在终端中，返回工作空间的根目录 ``ros2_ws``，并像之前一样构建更新后的软件包：

.. code-block:: console

    $ colcon build --packages-select python_parameter_event_handler

然后 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install\setup.bat

现在，为了测试远程参数的监测，首先运行新构建的 parameter_event_handler 代码：

.. code-block:: console

     $ ros2 run python_parameter_event_handler node_with_parameters

接下来，从另一个终端（已初始化 ROS），按如下方式运行 parameter_blackboard 演示应用程序：

.. code-block:: console

     $ ros2 run demo_nodes_cpp parameter_blackboard

最后，从第三个终端（已初始化 ROS），让我们在 parameter_blackboard 节点上设置一个参数：

.. code-block:: console

     $ ros2 param set parameter_blackboard a_double_param 3.45

执行此命令后，你应该在 parameter_event_handler 窗口中看到输出，表明回调函数在参数更新时被调用：

.. code-block:: console

      [INFO] [1699821958.757770223] [node_with_parameters]: Received an update to parameter: a_double_param: 3.45

同时监测所有节点参数
^^^^^^^^^^^^^^^^^^^^

如果你需要同时监测多个节点或参数，为每个参数分别调用 ``add_parameter_callback`` 会很繁琐。
在这种情况下，你可以使用 ``add_parameter_event_callback`` 注册一个单一回调，当 *任何* 节点的 *任何* 参数变化时触发。

为此，首先更新 SampleNodeWithParameters 构造函数，添加以下代码：

.. code-block:: Python

    def __init__(...):
        self.declare_parameter("another_double_param", 0.0)
        ...
        self.event_calback_handle = self.handler.add_parameter_event_callback(
            callback=self.event_callback,
        )

这会声明一个新的 double 参数 ``another_double_param``，并添加一个将监测两个参数的事件回调。
事件回调的签名与普通单参数回调不同，因此我们还需要定义一个合适的回调：

.. code-block:: Python

    def event_callback(self, parameter_event):
        self.get_logger().info(f"Received parameter event from node {parameter_event.node}")

        for p in parameter_event.changed_parameters:
            self.get_logger().info(
                f"Inside event: {p.name} changed to: {rclpy.parameter.parameter_value_to_python(p.value)}"
            )

请注意，``parameter_event`` 的类型为 {interface(rcl_interfaces/msg/ParameterEvent)}。
尽管本教程未展示，事件回调也可以用于监测参数何时被添加或删除。

返回工作空间的根目录 ``ros2_ws``，并像之前一样重新构建更新后的软件包：

.. code-block:: console

    $ colcon build --packages-select python_parameter_event_handler

然后 source 安装文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

      $ . install/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

      $ call install\setup.bat

要测试新的事件回调，首先运行 parameter_event_handler 节点：

.. code-block:: console

     $ ros2 run python_parameter_event_handler node_with_parameters

然后，从第二个终端（已 source ROS），让我们设置原始的 int 参数：

.. code-block:: console

     $ ros2 param set node_with_parameters an_int_param 44

执行此命令后，你应该看到单参数回调和事件回调都被触发：

.. code-block:: console

      [INFO] [1746414766.240101027] [node_with_parameters]: Received an update to parameter: an_int_param: 44
      [INFO] [1746414766.243499816] [node_with_parameters]: Received parameter event from node /node_with_parameters
      [INFO] [1746414766.244271445] [node_with_parameters]: Inside event: an_int_param changed to: 4

现在设置新的 double 参数：

.. code-block:: console

     $ ros2 param set node_with_parameters another_double_param 4.4

由于没有为 double 参数添加单参数回调（通过 ``add_parameter_callback``），我们应该只看到事件回调被触发：

.. code-block:: console

      [INFO] [1746414962.604832196] [node_with_parameters]: Received parameter event from node /node_with_parameters
      [INFO] [1746414962.607429035] [node_with_parameters]: Inside event: another_double_param changed to: 4.4

.. note::

   一次性设置多个参数时，最好使用 ``set_parameters_atomically``，这在 :doc:`../../Concepts/Basic/About-Parameters` 中有解释。
   这样，事件回调只会被触发一次。

小结
----

你创建了一个带参数的节点，并使用 ParameterEventHandler 类设置了一个回调来监测该参数的变化。
你还使用同一个类来监测远程节点的变化，以及在单个事件回调中监测所有参数。
ParameterEventHandler 是监测参数变化以便你能响应更新值的便捷方式。

相关内容
--------

要了解如何为 ROS 2 改编 ROS 1 参数文件，请参阅 :doc:`将 YAML 参数文件从 ROS 1 迁移到 ROS2 <../../How-To-Guides/Migrating-from-ROS1/Migrating-Parameters>` 教程。
