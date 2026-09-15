.. redirect-from::

    Tutorials/Using-Parameters-In-A-Class-Python

.. _PythonParamNode:

在类中使用参数（Python）
========================

**目标：** 使用 Python 创建并运行一个带有 ROS 参数的类。

**教程级别：** 初级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

当你制作自己的 :doc:`节点 <../Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>` 时，有时需要添加可以从 launch 文件设置的参数。

本教程将向你展示如何在 Python 类中创建这些参数，以及如何在 launch 文件中设置它们。

前置条件
--------

在前面的教程中，你学习了如何 :doc:`创建工作空间 <./Creating-A-Workspace/Creating-A-Workspace>` 和 :doc:`创建包 <./Creating-Your-First-ROS2-Package>`。
你还学习了 :doc:`参数 <../Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters>` 及其在 ROS 2 系统中的作用。

任务
----

1 创建一个包
^^^^^^^^^^^^

打开一个新终端，并 :doc:`source 你的 ROS 2 安装环境 <../Beginner-CLI-Tools/Configuring-ROS2-Environment>`，这样 ``ros2`` 命令才能正常工作。

按照 :ref:`这些说明 <new-directory>` 创建一个名为 ``ros2_ws`` 的新工作空间。

请记住，包应该在 ``src`` 目录中创建，而不是在工作空间的根目录。
进入 ``ros2_ws/src`` 并创建一个新包：

.. code-block:: console

  $ ros2 pkg create --build-type ament_python --license Apache-2.0 python_parameters --dependencies rclpy

你的终端将返回一条消息，验证你的包 ``python_parameters`` 及其所有必要的文件和文件夹已创建。

``--dependencies`` 参数会自动将必要的依赖行添加到 ``package.xml``。

1.1 更新 ``package.xml``
~~~~~~~~~~~~~~~~~~~~~~~~

因为你在创建包时使用了 ``--dependencies`` 选项，所以你不必手动向 ``package.xml`` 添加依赖。

不过，和往常一样，请确保将描述、维护者邮箱和姓名以及许可证信息添加到 ``package.xml``。

.. code-block:: xml

  <description>Python parameter tutorial</description>
  <maintainer email="you@email.com">Your Name</maintainer>
  <license>Apache-2.0</license>

2 编写 Python 节点
^^^^^^^^^^^^^^^^^^

在 ``ros2_ws/src/python_parameters/python_parameters`` 目录中，创建一个名为 ``python_parameters_node.py`` 的新文件，并在其中粘贴以下代码：

.. code-block:: Python

    import rclpy
    from rclpy.node import Node

    class MinimalParam(Node):
        def __init__(self):
            super().__init__('minimal_param_node')

            self.declare_parameter('my_parameter', 'world')

            self.timer = self.create_timer(1, self.timer_callback)

        def timer_callback(self):
            my_param = self.get_parameter('my_parameter').get_parameter_value().string_value

            self.get_logger().info('Hello %s!' % my_param)

            my_new_param = rclpy.parameter.Parameter(
                'my_parameter',
                rclpy.Parameter.Type.STRING,
                'world'
            )
            all_new_parameters = [my_new_param]
            self.set_parameters(all_new_parameters)

    def main():
        rclpy.init()
        node = MinimalParam()
        rclpy.spin(node)

    if __name__ == '__main__':
        main()



2.1 检查代码
~~~~~~~~~~~~
顶部的 ``import`` 语句用于导入包依赖。

下一段代码创建了类和构造函数。
构造函数中的 ``self.declare_parameter('my_parameter', 'world')`` 这一行创建了一个名为 ``my_parameter``、默认值为 ``world`` 的参数。
参数类型由默认值推断，因此在这种情况下它会被设置为字符串类型。
接下来，``timer`` 被初始化为 1 秒的周期，这会导致 ``timer_callback`` 函数每秒执行一次。

.. code-block:: Python

    class MinimalParam(Node):
        def __init__(self):
            super().__init__('minimal_param_node')

            self.declare_parameter('my_parameter', 'world')

            self.timer = self.create_timer(1, self.timer_callback)

我们的 ``timer_callback`` 函数的第一行从节点获取参数 ``my_parameter``，并将其存储在 ``my_param`` 中。
接下来，``get_logger`` 函数确保事件被记录。
然后 ``set_parameters`` 函数将参数 ``my_parameter`` 设置回默认字符串值 ``world``。
如果用户从外部更改了参数，这可以确保它总是被重置回原始值。

.. code-block:: Python

      def timer_callback(self):
          my_param = self.get_parameter('my_parameter').get_parameter_value().string_value

          self.get_logger().info('Hello %s!' % my_param)

          my_new_param = rclpy.parameter.Parameter(
              'my_parameter',
              rclpy.Parameter.Type.STRING,
              'world'
          )
          all_new_parameters = [my_new_param]
          self.set_parameters(all_new_parameters)

在 ``timer_callback`` 之后是我们的 ``main``。
这里初始化了 ROS 2，构造了一个 ``MinimalParam`` 类的实例，并且 ``rclpy.spin`` 开始处理来自节点的数据。

.. code-block:: Python

    def main():
        rclpy.init()
        node = MinimalParam()
        rclpy.spin(node)

    if __name__ == '__main__':
        main()


2.1.1 （可选）添加 ParameterDescriptor
""""""""""""""""""""""""""""""""""""""
可选地，你可以为参数设置一个描述符。
描述符允许你指定参数的文本描述及其约束，例如将其设为只读、指定范围等。
为此，``__init__`` 代码必须更改为：

.. code-block:: Python

    # ...

    class MinimalParam(Node):
        def __init__(self):
            super().__init__('minimal_param_node')

            from rcl_interfaces.msg import ParameterDescriptor
            my_parameter_descriptor = ParameterDescriptor(description='This parameter is mine!')

            self.declare_parameter('my_parameter', 'world', my_parameter_descriptor)

            self.timer = self.create_timer(1, self.timer_callback)

由于我们导入了 ``rcl_interfaces``，我们需要将依赖添加到 ``package.xml`` 以避免将来出现任何依赖问题：

.. code-block:: xml

    # ...
    <depend>rclpy</depend>
    <depend>rcl_interfaces</depend>

其余代码保持不变。
一旦你运行节点，就可以运行 ``ros2 param describe /minimal_param_node my_parameter`` 来查看类型和描述。

2.2 添加入口点
~~~~~~~~~~~~~~

打开 ``setup.py`` 文件。
再次将 ``maintainer``、``maintainer_email``、``description`` 和 ``license`` 字段与你的 ``package.xml`` 匹配：

.. code-block:: python

  maintainer='YourName',
  maintainer_email='you@email.com',
  description='Python parameter tutorial',
  license='Apache-2.0',

在 ``entry_points`` 字段的 ``console_scripts`` 括号内添加以下行：

.. code-block:: python

  entry_points={
      'console_scripts': [
          'minimal_param_node = python_parameters.python_parameters_node:main',
      ],
  },

不要忘记保存。


3 构建并运行
^^^^^^^^^^^^

在构建之前，最好在工作空间的根目录（``ros2_ws``）运行 ``rosdep`` 来检查缺失的依赖：

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ rosdep install -i --from-path src --rosdistro {DISTRO} -y

   .. group-tab:: macOS

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

   .. group-tab:: Windows

      rosdep 只在 Linux 上运行，所以你可以跳到下一步。

返回到工作空间的根目录 ``ros2_ws``，并构建你的新包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select python_parameters

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select python_parameters

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select python_parameters

打开一个新终端，进入 ``ros2_ws``，然后 source 安装文件：

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

现在运行节点。
终端应该每秒返回一次 ``Hello world!``：

.. code-block:: console

     $ ros2 run python_parameters minimal_param_node
    [INFO] [parameter_node]: Hello world!

现在你可以看到参数的默认值，但你想能够自己设置它。
有两种方法可以实现这一点。

3.1 通过控制台更改
~~~~~~~~~~~~~~~~~~

这部分将使用你从 :doc:`关于参数的教程 <../Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters>` 中获得的知识，并将其应用到你刚刚创建的节点上。

确保节点正在运行：

.. code-block:: console

     $ ros2 run python_parameters minimal_param_node

打开另一个终端，再次从 ``ros2_ws`` 内 source 安装文件，然后输入以下行：

.. code-block:: console

    $ ros2 param list

在那里你会看到自定义参数 ``my_parameter``。
要更改它，只需在控制台中运行以下行：

.. code-block:: console

    $ ros2 param set /minimal_param_node my_parameter earth

如果你得到了输出 ``Set parameter successful``，你就知道它成功了。
如果你查看另一个终端，你应该会看到输出变为 ``[INFO] [minimal_param_node]: Hello earth!``

由于节点随后将参数设置回 ``world``，后续输出显示 ``[INFO] [minimal_param_node]: Hello world!``

3.2 通过 launch 文件更改
~~~~~~~~~~~~~~~~~~~~~~~~

你也可以在 launch 文件中设置参数，但首先你需要添加一个 launch 目录。
在 ``ros2_ws/src/python_parameters/`` 目录中，创建一个名为 ``launch`` 的新目录。
在其中，创建一个名为 ``python_parameters_launch.py`` 的新文件。

.. literalinclude:: launch/python_parameters_launch.py
  :language: python

在这里你可以看到，当我们启动节点 ``parameter_node`` 时，我们将 ``my_parameter`` 设置为 ``earth``。
通过添加下面两行，我们确保输出打印在我们的控制台中。

.. code-block:: console

          output="screen",
          emulate_tty=True,

现在打开 ``setup.py`` 文件。
将 ``import`` 语句添加到文件顶部，并将另一个新语句添加到 ``data_files`` 参数以包含所有 launch 文件：

.. code-block:: Python

    import os
    from glob import glob
    # ...

    setup(
      # ...
      data_files=[
          # ...
          (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        ]
      )

打开一个控制台，进入工作空间的根目录 ``ros2_ws``，然后构建你的新包：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ colcon build --packages-select python_parameters

  .. group-tab:: macOS

    .. code-block:: console

      $ colcon build --packages-select python_parameters

  .. group-tab:: Windows

    .. code-block:: console

      $ colcon build --merge-install --packages-select python_parameters

然后在一个新终端中 source 安装文件：

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

现在使用我们刚刚创建的 launch 文件运行节点：

.. code-block:: console

     $ ros2 launch python_parameters python_parameters_launch.py
    [INFO] [custom_minimal_param_node]: Hello earth!

后续输出应该每秒显示一次 ``[INFO] [minimal_param_node]: Hello world!``。

总结
----

你创建了一个带有自定义参数的节点，该参数可以从 launch 文件或命令行设置。
你向包配置文件添加了依赖、可执行文件和 launch 文件，这样你就可以构建并运行它们，并看到参数的实际效果。

后续步骤
--------

既然你已经有了自己的包和 ROS 2 系统，:doc:`下一个教程 <./Getting-Started-With-Ros2doctor>` 将向你展示如何在你遇到问题时检查你的环境和系统中的问题。
