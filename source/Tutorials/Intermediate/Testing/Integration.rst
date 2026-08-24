使用 launch_testing 编写基础集成测试
====================================

**目标：** 在 ROS 2 turtlesim 节点上创建并运行集成测试。

**教程级别：** 中级

**时间：** 20 分钟

.. contents:: 目录
   :depth: 2
   :local:

先决条件
--------

在开始本教程之前，建议先完成以下关于启动节点的教程：

* :doc:`启动多个节点 <../../Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes>`
* :doc:`创建启动文件 <../../Intermediate/Launch/Creating-Launch-Files>`

背景
----

单元测试侧重于验证非常特定的功能，而集成测试侧重于验证代码片段之间的交互。
在 ROS 2 中，这通常通过启动一个或几个节点组成的系统来完成，例如 `Gazebo 仿真器 <https://gazebosim.org/home>`__ 和 `Nav2 导航 <https://github.com/ros-planning/navigation2.git>`__ 栈。
因此，这些测试在设置和运行上都更复杂。

ROS 2 集成测试的一个关键方面是，不同测试的一部分节点不应相互通信，即使并行运行时也是如此。
这里将通过使用一个特定的测试运行器来实现，该运行器会选择唯一的 :doc:`ROS 域 ID <../../../Concepts/Intermediate/About-Domain-ID>`。
此外，集成测试必须适应整体测试工作流。
一种标准化的方法是确保每个测试输出一个 XUnit 文件，这些文件可以很容易地使用常见的测试工具解析。

概述
----

这里使用的主要工具是 `launch_testing <https://docs.ros.org/en/{DISTRO}/p/launch_testing/index.html>`_ 包
（`launch_testing 仓库 <https://github.com/ros2/launch/tree/{REPOS_FILE_BRANCH}/launch_testing>`_）。
这种与 ROS 无关的功能可以用主动测试（在节点也运行时运行）和关机后测试（在所有节点退出后运行一次）来扩展 Python 启动文件。
``launch_testing`` 依赖 Python 标准模块 `unittest <https://docs.python.org/3/library/unittest.html>`_ 来进行实际测试。
为了让我们的集成测试作为 ``colcon test`` 的一部分运行，我们在 ``CMakeLists.txt`` 中注册启动文件。

步骤
----

1 在测试启动文件中描述测试
^^^^^^^^^^^^^^^^^^^^^^^^^^

被测节点和测试本身都使用一个 Python 启动文件来启动，它类似于 ROS 2 Python 启动文件。
习惯上让集成测试启动文件名称遵循 ``test/test_*.py`` 模式。

集成测试中有两种常见类型的测试：主动测试（在被测节点运行时运行）和关机后测试（在节点退出后运行）。
我们将在本教程中介绍这两种。

1.1 导入
~~~~~~~~

我们首先从导入我们将使用的 Python 模块开始。
只有两个模块是测试特有的：通用的 ``unittest`` 和 ``launch_testing``。

.. code-block:: python

  import os
  import sys
  import time
  import unittest

  import launch
  import launch_ros
  import launch_testing.actions
  import rclpy
  from turtlesim.msg import Pose

1.2 生成测试描述
~~~~~~~~~~~~~~~~

函数 ``generate_test_description`` 描述要启动什么，类似于 ROS 2 Python 启动文件中的 ``generate_launch_description``。
在下面的示例中，我们启动 turtlesim 节点，半秒后启动我们的测试。

在更复杂的集成测试设置中，你可能想启动一个由多个节点组成的系统，连同执行模拟或必须以其他方式与被测节点交互的额外节点。

.. code-block:: python

  def generate_test_description():
      return (
          launch.LaunchDescription(
              [
                  # Nodes under test
                  launch_ros.actions.Node(
                      package='turtlesim',
                      namespace='',
                      executable='turtlesim_node',
                      name='turtle1',
                  ),
                  # Launch tests 0.5 s later
                  launch.actions.TimerAction(
                      period=0.5, actions=[launch_testing.actions.ReadyToTest()]),
              ]
          ), {},
      )

1.3 主动测试
~~~~~~~~~~~~

主动测试与正在运行的节点交互。
在本教程中，我们将检查 turtlesim 节点是否发布 pose 消息（通过监听节点的 'turtle1/pose' 话题）以及它是否记录它生成了 turtle（通过监听 stderr）。

主动测试被定义为继承自 `unittest.TestCase <https://docs.python.org/3/library/unittest.html#unittest.TestCase>`_ 的类的方法。
子类，这里是 ``TestTurtleSim``，包含以下方法：

- ``test_*``：测试方法，每个方法与被测节点执行一些 ROS 通信和/或监听进程输出（通过 ``proc_output`` 传入）。
  它们按顺序执行。
- ``setUp``、``tearDown``：分别在执行每个测试方法之前（准备测试固定装置）和之后运行。
  通过在 ``setUp`` 方法中创建节点，我们为每个测试使用不同的节点实例，以减少测试之间相互通信的风险。
- ``setUpClass``、``tearDownClass``：这些类方法分别在所有测试方法执行之前和之后运行一次。

强烈建议阅读 `launch_testing 关于此主题的详细文档 <https://docs.ros.org/en/{DISTRO}/p/launch_testing/index.html>`_。

.. code-block:: python

  # Active tests
  class TestTurtleSim(unittest.TestCase):
      @classmethod
      def setUpClass(cls):
          rclpy.init()

      @classmethod
      def tearDownClass(cls):
          rclpy.shutdown()

      def setUp(self):
          self.node = rclpy.create_node('test_turtlesim')

      def tearDown(self):
          self.node.destroy_node()

      def test_publishes_pose(self, proc_output):
          """Check whether pose messages published"""
          msgs_rx = []
          sub = self.node.create_subscription(
              Pose, 'turtle1/pose',
              lambda msg: msgs_rx.append(msg), 100)
          try:
              # Listen to the pose topic for 10 s
              end_time = time.time() + 10
              while time.time() < end_time:
                  # spin to get subscriber callback executed
                  rclpy.spin_once(self.node, timeout_sec=1)
              # There should have been 100 messages received
              assert len(msgs_rx) > 100
          finally:
              self.node.destroy_subscription(sub)

      def test_logs_spawning(self, proc_output):
          """Check whether logging properly"""
          proc_output.assertWaitFor(
              'Spawning turtle [turtle1] at x=',
              timeout=5, stream='stderr')

注意，我们在 ``test_publishes_pose`` 中监听 'turtle1/pose' 话题的方式与 :doc:`通常的做法 <../../Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber>` 不同。
我们不调用阻塞的 ``rclpy.spin``，而是触发 ``spin_once`` 方法——它执行第一个可用的回调（如果 1 秒内收到消息，就是我们的订阅者回调）——直到我们收集了过去 10 秒内发布的所有消息。
包 `launch_testing_ros <https://docs.ros.org/en/{DISTRO}/p/launch_testing_ros/index.html>`_ 提供了一些便利函数来实现类似的行为，
例如 `WaitForTopics <https://docs.ros.org/en/{DISTRO}/p/launch_testing_ros/launch_testing_ros.wait_for_topics.html>`_。

如果你想更进一步，你可以实现第三个测试，发布一个 twist 消息，要求 turtle 移动，随后通过断言 pose 消息发生变化来检查它确实移动了。
这有效地自动化了 :doc:`Turtlesim 介绍教程 <../../Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim>` 的一部分。

1.4 关机后测试
~~~~~~~~~~~~~~

用 ``launch_testing.post_shutdown_test`` 装饰器标记的类会在让被测节点退出后运行。
这里的一个典型测试是节点是否干净退出，为此 ``launch_testing`` 提供了方法
`asserts.assertExitCodes <https://docs.ros.org/en/{DISTRO}/p/launch_testing/launch_testing.asserts.html#launch_testing.asserts.assertExitCodes>`_。

.. code-block:: python

  # Post-shutdown tests
  @launch_testing.post_shutdown_test()
  class TestTurtleSimShutdown(unittest.TestCase):
      def test_exit_codes(self, proc_info):
          """Check if the processes exited normally."""
          launch_testing.asserts.assertExitCodes(proc_info)

2 在 CMakeLists.txt 中注册测试
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 ``CMakeLists.txt`` 中注册测试实现两个功能：

- 将其集成到 ROS 2 基于 CMake 的包所依赖的 ``CTest`` 框架中
  （因此运行 ``colcon test`` 时会调用它）。
- 允许指定测试*如何*运行——
  在本例中，使用唯一的域 id 来确保测试隔离。

后一个方面通过使用特殊的测试运行器 `run_test_isolated.py <https://github.com/ros2/ament_cmake_ros/blob/{REPOS_FILE_BRANCH}/ament_cmake_ros/cmake/run_test_isolated.py>`_ 实现。
为了便于添加多个集成测试，我们定义 CMake 函数 ``add_ros_isolated_launch_test``，这样每个额外的测试只需要一行。

.. code-block:: cmake

  cmake_minimum_required(VERSION 3.8)
  project(app)

  ########
  # test #
  ########

  if(BUILD_TESTING)
    # Integration tests
    find_package(ament_cmake_ros REQUIRED)
    find_package(launch_testing_ament_cmake REQUIRED)
    function(add_ros_isolated_launch_test path)
      set(RUNNER "${ament_cmake_ros_DIR}/run_test_isolated.py")
      add_launch_test("${path}" RUNNER "${RUNNER}" ${ARGN})
    endfunction()
    add_ros_isolated_launch_test(test/test_integration.py)
  endif()

3 依赖与包组织
^^^^^^^^^^^^^^

最后，将以下依赖添加到你的 ``package.xml``：

.. code-block:: XML

  <test_depend>ament_cmake_ros</test_depend>
  <test_depend>launch</test_depend>
  <test_depend>launch_ros</test_depend>
  <test_depend>launch_testing</test_depend>
  <test_depend>launch_testing_ament_cmake</test_depend>
  <test_depend>rclpy</test_depend>
  <test_depend>turtlesim</test_depend>

按照上述步骤后，你的包（这里命名为 'app'）应该如下所示：

.. code-block::

  app/
    CMakeLists.txt
    package.xml
    tests/
        test_integration.py

集成测试可以是任何 ROS 包的一部分。
可以指定一个或多个包专门用于集成测试，或者将它们添加到它们所测试功能的包中。
在本教程中，我们采用第一种方式，因为我们要测试现有的 turtlesim 节点。

4 运行测试与报告生成
^^^^^^^^^^^^^^^^^^^^

要运行集成测试并检查结果，请参阅教程 :doc:`在 ROS 2 中从命令行运行测试<../../Intermediate/Testing/CLI>`。

总结
----

在本教程中，我们探讨了在 ROS 2 turtlesim 节点上创建和运行集成测试的过程。
我们讨论了集成测试启动文件，并介绍了编写主动测试和关机后测试。
回顾一下，集成测试启动文件的四个关键元素是：

* 函数 ``generate_test_description``：它启动我们的被测节点以及我们的测试。
* ``launch_testing.actions.ReadyToTest()``：它提醒测试框架应该运行测试，并确保主动测试和节点一起运行。
* 一个继承自 ``unittest.TestCase`` 的未装饰类：它容纳主动测试，包括设置和拆除，并通过 ``proc_output`` 提供对 ROS 日志的访问。
* 第二个继承自 ``unittest.TestCase`` 的类，用 ``@launch_testing.post_shutdown_test()`` 装饰：这些是在所有节点关闭后运行的测试；通常断言节点干净退出。

启动测试随后使用自定义 cmake 宏 ``add_ros_isolated_launch_test`` 在 ``CMakeLists.txt`` 中注册，它确保每个启动测试以唯一的 ``ROS_DOMAIN_ID`` 运行，
避免不希望出现的交叉通信。

相关内容
--------

* :doc:`为什么需要自动测试？ <../../Intermediate/Testing/Testing-Main>`
* :doc:`使用 GTest 进行 C++ 单元测试 <../../Intermediate/Testing/Cpp>`
  和 :doc:`使用 Pytest 进行 Python 单元测试 <../../Intermediate/Testing/Python>`
* `launch_pytest 文档 <https://docs.ros.org/en/{DISTRO}/p/launch_pytest/index.html>`_，
  一个替代 ``launch_testing`` 的启动集成测试包
