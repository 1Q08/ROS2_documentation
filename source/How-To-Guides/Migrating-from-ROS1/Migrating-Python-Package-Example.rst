迁移 Python 包示例
==================

本指南展示如何将一个示例 Python 包从 ROS 1 迁移到 ROS 2。

.. contents:: 目录
   :depth: 2
   :local:

前提条件
--------

你需要一个可用的 ROS 2 安装，例如 :doc:`ROS {DISTRO} <../../Installation>`。

ROS 1 代码
----------

在本指南中你不会使用 `catkin <https://index.ros.org/p/catkin/>`__，因此你不需要一个可用的 ROS 1 安装。
你将改用 ROS 2 的构建工具 `Colcon <https://colcon.readthedocs.io/>`__。

本节为你提供 ROS 1 Python 包的代码。
该包名为 ``talker_py``，它有一个名为 ``talker_py_node`` 的节点。
为了便于稍后运行 Colcon，这些说明让你在一个 `Colcon 工作空间 <https://colcon.readthedocs.io/en/released/user/what-is-a-workspace.html>`__ 中创建该包，

首先，在 ``~/ros2_talker_py`` 处创建一个文件夹，作为 Colcon 工作空间的根目录。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ mkdir -p ~/ros2_talker_py/src

  .. group-tab:: macOS

    .. code-block:: console

        $ mkdir -p ~/ros2_talker_py/src

  .. group-tab:: Windows

    .. code-block:: console

        $ md \ros2_talker_py\src

接下来，为 ROS 1 包创建文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ cd ~/ros2_talker_py
        $ mkdir -p src/talker_py/src/talker_py
        $ mkdir -p src/talker_py/scripts
        $ touch src/talker_py/package.xml
        $ touch src/talker_py/CMakeLists.txt
        $ touch src/talker_py/src/talker_py/__init__.py
        $ touch src/talker_py/scripts/talker_py_node
        $ touch src/talker_py/setup.py

  .. group-tab:: macOS

    .. code-block:: console

        $ cd ~/ros2_talker_py
        $ mkdir -p src/talker_py/src/talker_py
        $ mkdir -p src/talker_py/scripts
        $ touch src/talker_py/package.xml
        $ touch src/talker_py/CMakeLists.txt
        $ touch src/talker_py/src/talker_py/__init__.py
        $ touch src/talker_py/scripts/talker_py_node
        $ touch src/talker_py/setup.py

  .. group-tab:: Windows

    .. code-block:: console

        $ cd \ros2_talker_py
        $ md src\talker_py\src\talker_py
        $ md src\talker_py\scripts
        $ type nul > src\talker_py\package.xml
        $ type nul > src\talker_py\CMakeLists.txt
        $ type nul > src\talker_py\src\talker_py\__init__.py
        $ type nul > src\talker_py\scripts/talker_py_node
        $ type nul > src\talker_py\setup.py

将以下内容放入每个文件。

``src/talker_py/package.xml``:

.. code-block:: xml

    <?xml version="1.0"?>
    <?xml-model href="http://download.ros.org/schema/package_format2.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
    <package format="2">
        <name>talker_py</name>
        <version>1.0.0</version>
        <description>The talker_py package</description>
        <maintainer email="gerkey@example.com">Brian Gerkey</maintainer>
        <license>BSD</license>

        <buildtool_depend>catkin</buildtool_depend>

        <depend>rospy</depend>
        <depend>std_msgs</depend>
    </package>

``src/talker_py/CMakeLists.txt``:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.0.2)
    project(talker_py)

    find_package(catkin REQUIRED)

    catkin_python_setup()

    catkin_package()

    catkin_install_python(PROGRAMS
        scripts/talker_py_node
        DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    )

``src/talker/src/talker_py/__init__.py``:

.. code-block:: Python

    import rospy
    from std_msgs.msg import String

    def main():
        rospy.init_node('talker')
        pub = rospy.Publisher('chatter', String, queue_size=10)
        rate = rospy.Rate(10)  # 10hz
        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
            rate.sleep()

``src/talker_py/scripts/talker_py_node``:

.. code-block:: Python

    #!/usr/bin/env python

    import talker_py

    if __name__ == '__main__':
        talker_py.main()

``src/talker_py/setup.py``:

.. code-block:: Python

    from setuptools import setup
    from catkin_pkg.python_setup import generate_distutils_setup

    setup_args = generate_distutils_setup(
        packages=['talker_py'],
        package_dir={'': 'src'}
    )

    setup(**setup_args)

这就是完整的 ROS 1 Python 包。

迁移 ``package.xml``
--------------------

在将包迁移到 ROS 2 时，先迁移构建系统文件，这样你就可以边构建、运行代码边检查自己的工作。
始终从迁移你的 ``package.xml`` 开始。

首先，ROS 2 不使用 ``catkin``。
删除对它的 ``<buildtool_depend>`` 依赖。

.. code-block::

    <!-- delete this -->
    <buildtool_depend>catkin</buildtool_depend>


接下来，ROS 2 使用 ``rclpy`` 而不是 ``rospy``。
删除对 ``rospy`` 的依赖。

.. code-block::

    <!-- Delete this -->
    <depend>rospy</depend>


用对 ``rclpy`` 的新依赖替换它。

.. code-block:: xml

    <depend>rclpy</depend>

添加一个 ``<export>`` 部分，告诉 ROS 2 的构建工具 `Colcon <https://colcon.readthedocs.io/>`__ 这是一个 ``ament_python`` 包，而不是 ``catkin`` 包。

.. code-block:: xml

     <export>
       <build_type>ament_python</build_type>
     </export>


你的 ``package.xml`` 已完全迁移。
它现在应该看起来像这样：

.. code-block:: xml

    <?xml version="1.0"?>
    <?xml-model href="http://download.ros.org/schema/package_format2.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
    <package format="2">
        <name>talker_py</name>
        <version>1.0.0</version>
        <description>The talker_py package</description>
        <maintainer email="gerkey@example.com">Brian Gerkey</maintainer>
        <license>BSD</license>

        <depend>rclpy</depend>
        <depend>std_msgs</depend>

        <export>
            <build_type>ament_python</build_type>
        </export>
    </package>

删除 ``CMakeLists.txt``
-----------------------

ROS 2 中的 Python 包不使用 CMake，因此删除 ``CMakeLists.txt``。

迁移 ``setup.py``
-----------------

``setup.py`` 中 ``setup()`` 的参数不能再通过 ``catkin_pkg`` 自动生成。
你必须手动传入这些参数，这意味着会与你的 ``package.xml`` 有一些重复。

首先删除来自 ``catkin_pkg`` 的导入。

.. code-block::

    # Delete this
    from catkin_pkg.python_setup import generate_distutils_setup

将传给 ``generate_distutils_setup()`` 的所有参数移到对 ``setup()`` 的调用中，然后添加 ``install_requires`` 和 ``zip_safe`` 参数。
你对 ``setup()`` 的调用应该看起来像这样：

.. code-block:: Python

    setup(
        packages=['talker_py'],
        package_dir={'': 'src'},
        install_requires=['setuptools'],
        zip_safe=True,
    )

删除对 ``generate_distutils_setup()`` 的调用。

.. code-block::

    # Delete this
    setup_args = generate_distutils_setup(
        packages=['talker_py'],
        package_dir={'': 'src'}
    )

对 ``setup()`` 的调用需要从 ``package.xml`` 复制一些 `附加元数据 <https://docs.python.org/3.11/distutils/setupscript.html#additional-meta-data>`__：

* 通过 ``name`` 参数传入包名
* 通过 ``version`` 参数传入包版本
* 通过 ``maintainer`` 和 ``maintainer_email`` 参数传入维护者
* 通过 ``description`` 参数传入描述
* 通过 ``license`` 参数传入许可证

包名会被多次使用。
在 ``setup()`` 调用上方创建一个名为 ``package_name`` 的变量。

.. code-block:: Python

    package_name = 'talker_py'

将所有剩余信息复制到 ``setup.py`` 中 ``setup()`` 的参数里。
你对 ``setup()`` 的调用应该看起来像这样：

.. code-block:: Python

    setup(
        name=package_name,
        version='1.0.0',
        install_requires=['setuptools'],
        zip_safe=True,
        packages=['talker_py'],
        package_dir={'': 'src'},
        maintainer='Brian Gerkey',
        maintainer_email='gerkey@example.com',
        description='The talker_py package',
        license='BSD',
    )


ROS 2 包必须安装两个数据文件：

* 一个 ``package.xml``
* 一个包标记文件

你的包已经有一个 ``package.xml``。
它描述了包的依赖关系。
包标记文件告诉诸如 ``ros2 run`` 之类的工具在哪里找到你的包。

在 ``package.xml`` 旁边创建一个名为 ``resource`` 的目录。
在 ``resource`` 目录中创建一个与包同名且内容为空的文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ mkdir resource
        $ touch resource/talker_py

  .. group-tab:: macOS

    .. code-block:: console

        $ mkdir resource
        $ touch resource/talker_py

  .. group-tab:: Windows

    .. code-block:: console

        $ md resource
        $ type nul > resource\talker_py

``setup.py`` 中的 ``setup()`` 调用必须告诉 ``setuptools`` 如何安装这些文件。
将以下 ``data_files`` 参数添加到对 ``setup()`` 的调用中。

.. code-block:: Python

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],

你的 ``setup.py`` 已基本完成。

迁移 Python 脚本并创建 ``setup.cfg``
------------------------------------

ROS 2 Python 包使用 ``console_scripts`` `入口点 <https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point>`__ 将 Python 脚本安装为可执行文件。
`配置文件 <https://setuptools.pypa.io/en/latest/userguide/declarative_config.html>`__ ``setup.cfg`` 告诉 ``setuptools`` 将这些可执行文件安装到包专属目录，以便诸如 ``ros2 run`` 之类的工具能够找到它们。
在 ``package.xml`` 旁边创建一个 ``setup.cfg`` 文件。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ touch setup.cfg

  .. group-tab:: macOS

    .. code-block:: console

        $ touch setup.cfg

  .. group-tab:: Windows

    .. code-block:: console

        $ type nul > touch setup.cfg

将以下内容放入其中：

.. code-block:: ini

    [develop]
    script_dir=$base/lib/talker_py
    [install]
    install_scripts=$base/lib/talker_py

你需要使用 ``console_scripts`` 入口点来定义要安装的可执行文件。
每个条目的格式为 ``executable_name = some.module:function``。
第一部分指定要创建的可执行文件的名称。
第二部分指定可执行文件启动时应运行的函数。
此包需要创建一个名为 ``talker_py_node`` 的可执行文件，该可执行文件需要调用 ``talker_py`` 模块中的 ``main`` 函数。
将以下入口点规范作为另一个参数添加到你的 ``setup.py`` 的 ``setup()`` 中。

.. code-block:: Python

    entry_points={
        'console_scripts': [
            'talker_py_node = talker_py:main',
        ],
    },

``talker_py_node`` 文件不再需要。
删除文件 ``talker_py_node`` 并删除 ``scripts/`` 目录。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ rm scripts/talker_py_node
        $ rmdir scripts

  .. group-tab:: macOS

    .. code-block:: console

        $ rm scripts/talker_py_node
        $ rmdir scripts

  .. group-tab:: Windows

    .. code-block:: console

        $ del scripts/talker_py_node
        $ rd scripts

添加 ``console_scripts`` 是对你的 ``setup.py`` 的最后一次修改。
你最终的 ``setup.py`` 应该看起来像这样：

.. code-block:: Python

    from setuptools import setup

    package_name = 'talker_py'

    setup(
        name=package_name,
        version='1.0.0',
        packages=['talker_py'],
        package_dir={'': 'src'},
        install_requires=['setuptools'],
        zip_safe=True,
        data_files=[
            ('share/ament_index/resource_index/packages',
                ['resource/' + package_name]),
            ('share/' + package_name, ['package.xml']),
        ],
        maintainer='Brian Gerkey',
        maintainer_email='gerkey@example.com',
        description='The talker_py package',
        license='BSD',
        entry_points={
            'console_scripts': [
                'talker_py_node = talker_py:main',
            ],
        },
    )

迁移 ``src/talker_py/__init__.py`` 中的 Python 代码
---------------------------------------------------

ROS 2 改变了许多 Python 代码的最佳实践。
先按原样迁移代码。
在有了可运行的东西之后，稍后再重构代码会更容易。

使用 ``rclpy`` 而不是 ``rospy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ROS 2 包使用 `rclpy <https://index.ros.org/p/rclpy>`__ 而不是 ``rospy``。
要使用 ``rclpy``，你必须做两件事：

    1. 导入 ``rclpy``
    2. 初始化 ``rclpy``

删除导入 ``rospy`` 的语句。

.. code-block:: Python

    # Remove this
    import rospy

用导入 ``rclpy`` 的语句替换它。

.. code-block:: Python

    import rclpy

在 ``main()`` 函数中，将 ``rclpy.init()`` 的调用添加为第一条语句。

.. code-block:: Python

    def main():
        # Add this line
        rclpy.init()

在后台执行回调
~~~~~~~~~~~~~~

ROS 1 和 ROS 2 都使用 `回调 <https://en.wikipedia.org/wiki/Callback_(computer_programming)>`__。
在 ROS 1 中，回调始终在后台线程中执行，用户可以自由地用诸如 ``rate.sleep()`` 之类的调用阻塞主线程。
在 ROS 2 中，``rclpy`` 使用 :doc:`执行器 <../../Concepts/Intermediate/About-Executors>` 让用户能更好地控制回调在何处被调用。
在移植使用诸如 ``rate.sleep()`` 之类的阻塞调用的代码时，你必须确保这些调用不会干扰执行器。
一种做法是为执行器创建一个专用线程。

首先，添加这两个导入语句。

.. code-block:: Python

    import threading

    from rclpy.executors import ExternalShutdownException

接下来，添加一个名为 ``spin_in_background()`` 的顶层函数。
此函数请求默认执行器执行回调，直到有东西将其关闭。

.. code-block:: Python

    def spin_in_background():
        executor = rclpy.get_global_executor()
        try:
            executor.spin()
        except ExternalShutdownException:
            pass

在 ``main()`` 函数中，紧接在 ``rclpy.init()`` 调用之后添加以下代码，以启动一个调用 ``spin_in_background()`` 的线程。

.. code-block:: Python

        # In rospy callbacks are always called in background threads.
        # Spin the executor in another thread for similar behavior in ROS 2.
        t = threading.Thread(target=spin_in_background)
        t.start()


最后，在程序结束时通过在 ``main()`` 函数底部放置以下语句来加入（join）该线程。

.. code-block:: Python

        t.join()


创建节点
~~~~~~~~

在 ROS 1 中，Python 脚本每个进程只能创建一个节点，并且 API ``init_node()`` 会创建它。
在 ROS 2 中，单个 Python 脚本可以创建多个节点，并且创建节点的 API 名为 ``create_node``。

删除对 ``rospy.init_node()`` 的调用：

.. code-block::

    rospy.init_node('talker')

添加一个对 ``rclpy.create_node()`` 的新调用，并将结果存储在一个名为 ``node`` 的变量中：

.. code-block:: Python

    node = rclpy.create_node('talker')

我们必须告诉执行器这个节点。
在创建节点的正下方添加以下行：

.. code-block:: Python

    rclpy.get_global_executor().add_node(node)

创建发布者
~~~~~~~~~~

在 ROS 1 中，用户通过实例化 ``Publisher`` 类来创建发布者。
在 ROS 2 中，用户通过节点的 ``create_publisher()`` API 创建发布者。
``create_publisher()`` API 与 ROS 1 有一个不幸的差异：话题名称和话题类型参数的顺序对调了。

删除 ``rospy.Publisher`` 实例的创建。

.. code-block::

    pub = rospy.Publisher('chatter', String, queue_size=10)

用对 ``node.create_publisher()`` 的调用替换它。

.. code-block:: Python

    pub = node.create_publisher(String, 'chatter', 10)


创建 rate
~~~~~~~~~

在 ROS 1 中，用户直接创建 ``Rate`` 实例，而在 ROS 2 中，用户通过节点的 ``create_rate()`` API 来创建它们。

删除 ``rospy.Rate`` 实例的创建。

.. code-block::

    rate = rospy.Rate(10)  # 10hz

用对 ``node.create_rate()`` 的调用替换它。

.. code-block:: Python

    rate = node.create_rate(10)  # 10hz

在 ``rclpy.ok()`` 上循环
~~~~~~~~~~~~~~~~~~~~~~~~

在 ROS 1 中，``rospy.is_shutdown()`` API 指示进程是否已被要求关闭。
在 ROS 2 中，``rclpy.ok()`` API 完成这项工作。

删除语句 ``not rospy.is_shutdown()``

.. code-block::

    while not rospy.is_shutdown():

用对 ``rclpy.ok()`` 的调用替换它。

.. code-block:: Python

    while rclpy.ok():


创建一个带有当前时间的 ``String`` 消息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

你必须对这一行做一些修改

.. code-block::

    hello_str = "hello world %s" % rospy.get_time()

在 ROS 2 中你需要：

* 必须从一个 ``Clock`` 实例获取时间
* 应该使用 `f-string <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`__ 格式化 ``str`` 数据，因为 `% 在活跃的 Python 版本中不受推荐 <https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting>`__
* 必须实例化一个 ``std_msgs.msg.String`` 实例

从获取时间开始。
ROS 2 节点有一个 ``Clock`` 实例。
用 ``node.get_clock().now()`` 替换对 ``rospy.get_time()`` 的调用，以从节点时钟获取当前时间。

接下来，用 f-string 替换 ``%`` 的用法：``f'hello world {node.get_clock().now()}'``。

最后，实例化一个 ``std_msgs.msg.String()`` 实例，并将上述内容赋给该实例的 ``data`` 属性。
你的最终代码应该看起来像这样：

.. code-block:: Python

    hello_str = String()
    hello_str.data = f'hello world {node.get_clock().now()}'

记录一条信息性消息
~~~~~~~~~~~~~~~~~~

在 ROS 2 中，你必须通过一个 ``Logger`` 实例发送日志消息，而节点就有一个。

删除对 ``rospy.loginfo()`` 的调用。

.. code-block::

    rospy.loginfo(hello_str)

用对节点 ``Logger`` 实例的 ``info()`` 的调用替换它。

.. code-block:: Python

    node.get_logger().info(hello_str.data)

这是对 ``src/talker_py/__init__.py`` 的最后一次修改。
你的文件应该看起来如下所示：

.. code-block:: Python

    import threading

    import rclpy
    from rclpy.executors import ExternalShutdownException
    from std_msgs.msg import String


    def spin_in_background():
        executor = rclpy.get_global_executor()
        try:
            executor.spin()
        except ExternalShutdownException:
            pass


    def main():
        rclpy.init()
        # In rospy callbacks are always called in background threads.
        # Spin the executor in another thread for similar behavior in ROS 2.
        t = threading.Thread(target=spin_in_background)
        t.start()

        node = rclpy.create_node('talker')
        rclpy.get_global_executor().add_node(node)
        pub = node.create_publisher(String, 'chatter', 10)
        rate = node.create_rate(10)  # 10hz

        while rclpy.ok():
            hello_str = String()
            hello_str.data = f'hello world {node.get_clock().now()}'
            node.get_logger().info(hello_str.data)
            pub.publish(hello_str)
            rate.sleep()

        t.join()


构建并运行 ``talker_py_node``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

创建三个终端：

1. 一个用于构建 ``talker_py``
2. 一个用于运行 ``talker_py_node``
3. 一个用于回显 ``talker_py_node`` 发布的消息

在第一个终端中构建工作空间。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ cd ~/ros2_talker_py
        $ . /opt/ros/{DISTRO}/setup.bash
        $ colcon build

  .. group-tab:: macOS

    .. code-block:: console

        $ cd ~/ros2_talker_py
        $ . /opt/ros/{DISTRO}/setup.bash
        $ colcon build

  .. group-tab:: Windows

    .. code-block:: console

        $ cd \ros2_talker_py
        $ call C:\dev\ros2\local_setup.bat
        $ colcon build

在第二个终端中 source 你的工作空间，并运行 ``talker_py_node``。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ cd ~/ros2_talker_py
        $ . install/setup.bash
        $ ros2 run talker_py talker_py_node

  .. group-tab:: macOS

    .. code-block:: console

        $ cd ~/ros2_talker_py
        $ . install/setup.bash
        $ ros2 run talker_py talker_py_node

  .. group-tab:: Windows

    .. code-block:: console

        $ cd \ros2_talker_py
        $ call install\setup.bat
        $ ros2 run talker_py talker_py_node

在第三个终端中回显节点发布的消息：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

        $ . /opt/ros/{DISTRO}/setup.bash
        $ ros2 topic echo /chatter

  .. group-tab:: macOS

    .. code-block:: console

        $ . /opt/ros/{DISTRO}/setup.bash
        $ ros2 topic echo /chatter

  .. group-tab:: Windows

    .. code-block:: console

        $ call C:\dev\ros2\local_setup.bat
        $ ros2 topic echo /chatter


你应该在第二个终端中看到带有当前时间的消息被发布，并在第三个终端中收到这些相同的消息。

重构代码以使用 ROS 2 约定
-------------------------

你已经成功地将一个 ROS 1 Python 包迁移到了 ROS 2！
现在你有了可运行的东西，考虑重构它以更好地贴合 ROS 2 的 Python API。
遵循以下两条原则。

* 创建一个继承自 ``Node`` 的类。
* 在回调中完成所有工作，并且绝不要阻塞这些回调。

例如，创建一个继承自 ``Node`` 的 ``Talker`` 类。
至于在回调中完成工作，使用带回调的 ``Timer`` 而不是 ``rate.sleep()``。
让定时器回调发布消息并返回。
让 ``main()`` 创建 ``Talker`` 实例而不是使用 ``rclpy.create_node()``，并将主线程交给执行器去执行。

你的重构后代码可能看起来像这样：

.. code-block:: Python

    import rclpy
    from rclpy.node import Node
    from rclpy.executors import ExternalShutdownException
    from std_msgs.msg import String


    class Talker(Node):

        def __init__(self, **kwargs):
            super().__init__('talker', **kwargs)

            self._pub = self.create_publisher(String, 'chatter', 10)
            self._timer = self.create_timer(1 / 10, self.do_publish)

        def do_publish(self):
            hello_str = String()
            hello_str.data = f'hello world {self.get_clock().now()}'
            self.get_logger().info(hello_str.data)
            self._pub.publish(hello_str)


    def main():
        rclpy.init()
        try:
            rclpy.spin(Talker())
        except (ExternalShutdownException, KeyboardInterrupt):
            pass
        finally:
            rclpy.try_shutdown()

结论
----

你已经学会了如何将一个示例 Python ROS 1 包迁移到 ROS 2。
从现在起，在迁移你自己的 Python 包时，请参考 :doc:`迁移 Python 包参考页 <./Migrating-Python-Packages>`。
