在 ROS 2 中获取回溯
###################

.. contents:: 目录
   :local:

**目标：** 展示在 ROS 2 中获取回溯（backtrace）的各种方法

**教程级别：** 中级

**时间：** 15 分钟

以下步骤向 ROS 2 用户展示在遇到问题时如何获取回溯。

概述
----

**什么是回溯？**

- 想象你的程序就像一叠煎饼，每一张煎饼代表它当前正在执行的一个函数。
  回溯就像一张煎饼堆倒塌后的照片，向你展示它们的顺序，揭示程序是如何最终出现故障的。
- 它列出被调用的函数序列，一个叠在另一个之上，一直追溯到故障发生点。

**它为什么有用？**

- **精确定位问题：** 回溯会向你展示导致崩溃的确切行号，而不是猜测错误发生在代码中的哪个位置。
- **揭示上下文：** 你可以看到最终触发故障的事件链（函数调用其他函数）。
  这不仅能帮助你理解哪里出了问题，还能理解为什么。

**视觉类比**：煎饼堆

1. 每张煎饼是一个函数：想象堆叠中的每张煎饼代表你的程序当前正在执行的一个函数。
   最底部的煎饼是你的 main() 函数，一切从这里开始。

2. 添加煎饼：每当一个函数调用另一个函数时，就会在堆栈顶部放置一张新的煎饼。

3. 崩溃：崩溃就像盘子从煎饼堆底部滑出——在当前执行的函数中发生了灾难性的错误。

4. 回溯：回溯就像那张倒塌煎饼堆的照片。
   它展示了煎饼（函数）从顶部到底部的顺序，揭示你是如何最终到达崩溃现场的。


**代码示例：**

.. code-block:: cpp

  void functionC() {
    // Something bad happens here, causing a crash
  }

  void functionB() {
      functionC();
  }

  void functionA() {
      functionB();
  }

  int main() {
      functionA();
      return 0;
  }

**崩溃时的回溯：**

.. code-block:: bash

  #0  functionC() at file.cpp:3 // Crash occurred here
  #1  functionB() at file.cpp:8
  #2  functionA() at file.cpp:13
  #3  main() at file.cpp:18

**回溯如何提供帮助：**

- **崩溃来源：** 向你展示 ``functionC()`` 中触发崩溃的确切行。
- **调用序列：** 揭示 ``main()`` 调用了 ``functionA()``，``functionA()`` 调用了 ``functionB()``，最终导致了 ``functionC()`` 中的错误。

上面的示例让我们清楚地了解了什么是回溯以及它如何有用。
现在，以下步骤向 ROS 2 用户展示在遇到问题时如何从特定节点获取回溯。
本教程同时适用于仿真机器人和实体机器人。

这将涵盖如何使用 ``ros2 run`` 从特定节点获取回溯、如何使用 ``ros2 launch`` 从表示单个节点的 launch 文件获取回溯，以及如何从更复杂的节点编排中获取回溯。
学完本教程后，当你发现 ROS 2 中的节点崩溃时，应该能够获取回溯。

预备知识
--------

GDB 是 Unix 系统上最流行的 C/C++ 调试器。
它可以用来确定崩溃的原因并跟踪线程。
它还可以用于在代码中添加断点，以检查软件中特定点的内存值。

对于所有从事 C/C++ 开发的软件开发者来说，使用 GDB 是一项关键技能。
虽然许多 IDE 都内置了某种调试器或性能分析器，但重要的是要理解如何使用这些你可用的原始工具，而不是依赖 IDE 来提供它们。
理解这些工具是 C/C++ 开发的基本技能，如果你换了岗位、不再能访问这些工具，或者通过 ssh 会话对远程设备进行临时开发，那么把它交给 IDE 可能会带来问题。

幸运的是，掌握了基础知识之后，使用 GDB 是相当简单的。
以下是确保你的 ROS2 代码准备好调试的方法：

- 使用 ``--cmake-args``：包含调试符号的最简单方法是在你的 ``colcon build`` 命令中添加 ``--cmake-args -DCMAKE_BUILD_TYPE=Debug``：

.. code-block:: console

  $ colcon build --packages-up-to <package_name> --cmake-args -DCMAKE_BUILD_TYPE=Debug

- 编辑 ``CMakeLists.txt``：另一种方法是为你想要分析/调试的 ROS 包在编译器标志中添加 ``-g``。
  该标志会构建 GDB 可以读取的调试符号，以告诉你项目中哪些具体的代码行正在失败以及为什么。
  如果你不设置此标志，你仍然可以获得回溯，但它不会提供失败的行号。

现在你已经准备好调试代码了！
如果这是一个非 ROS 项目，此时你可能会执行如下操作。
这里我们启动一个 GDB 会话，并让程序立即运行。
一旦你的程序崩溃，它会返回一个以 ``(gdb)`` 表示的 gdb 会话提示符。
在此提示符下，你可以访问你感兴趣的信息。
但是，由于这是一个 ROS 项目，包含大量节点配置和其他内容，对于初学者或不喜欢大量命令行工作和理解文件系统的人来说，这并不是一个好选择。

.. code-block:: console

  $ gdb ex run --args /path/to/exe/program

以下部分描述了你在基于 ROS 2 的系统中可能遇到的三种主要情况。
阅读最能描述你试图解决问题的部分。

使用 GDB 调试特定节点
---------------------

要在启动 ROS 2 节点之前轻松设置 GDB 会话，可以利用 ``--prefix`` 选项在启动 ROS 2 节点之前轻松设置 GDB 会话。
对于 GDB 调试，按如下方式使用它：

.. note::

  请记住，一个 ROS 2 可执行文件可能包含多个节点。
  ``--prefix`` 方法可确保你调试的是进程中的正确节点。

**为什么直接使用 GDB 可能会很棘手**

``--prefix`` 会在我们的 ROS 2 命令之前执行一些代码片段，从而允许我们插入一些信息。
如果你尝试像预备知识中的示例那样执行 ``gdb ex run --args ros2 run <pkg> <node>``，你会发现它找不到 ``ros2`` 命令。
此外，尝试在 GDB 中 source 你的工作空间也会因类似原因而失败。
这是因为以这种方式启动 GDB 时，缺少通常使 ``ros2`` 命令可用的环境设置。

**使用 --prefix 简化流程**

与其回头查找可执行文件的安装路径并全部键入，我们可以改用 ``--prefix``。
这使我们能够使用你熟悉的 ``ros2 run`` 语法，而不必担心一些 GDB 细节。

.. code-block:: console

  $ ros2 run --prefix 'gdb -ex run --args' <pkg> <node> --all-other-launch arguments

**GDB 体验**

与之前一样，此前缀会启动一个 GDB 会话，并使用所有附加的命令行参数运行你请求的节点。
现在，你的节点应该正在运行，并伴随一些调试输出持续运行。

阅读堆栈跟踪
------------

使用 GDB 获取回溯后，以下是如何解读它：

- 从底部开始：回溯按逆时间顺序列出函数调用。
  底部的函数是崩溃的起源。

- 沿堆栈向上追溯：上面的每一行代表调用其下方函数的函数。
  向上追溯，直到到达你自己项目中的某行代码。
  这通常能揭示问题是从哪里开始的。

- 调试线索：函数名及其参数可以提供关于出了什么问题的宝贵线索。

**节点崩溃后如何调试**

一旦你的节点崩溃，你会看到如下所示的提示符。
此时你可以获取回溯。

.. code-block:: bash

  (gdb)

在此会话中，输入 ``backtrace``，它会为你提供回溯。
根据需要将其复制下来。


**回溯示例**

.. code-block:: bash

  (gdb) backtrace
  #0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
  #1  0x00007ffff79cc859 in __GI_abort () at abort.c:79
  #2  0x00007ffff7c52951 in ?? () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  #3  0x00007ffff7c5e47c in ?? () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  #4  0x00007ffff7c5e4e7 in std::terminate() () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  #5  0x00007ffff7c5e799 in __cxa_throw () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  #6  0x00007ffff7c553eb in ?? () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
  #7  0x000055555555936c in std::vector<int, std::allocator<int> >::_M_range_check (
      this=0x5555555cfdb0, __n=100) at /usr/include/c++/9/bits/stl_vector.h:1070
  #8  0x0000555555558e1d in std::vector<int, std::allocator<int> >::at (this=0x5555555cfdb0,
      __n=100) at /usr/include/c++/9/bits/stl_vector.h:1091
  #9  0x000055555555828b in GDBTester::VectorCrash (this=0x5555555cfb40)
      at /home/steve/Documents/nav2_ws/src/gdb_test_pkg/src/gdb_test_node.cpp:44
  #10 0x0000555555559cfc in main (argc=1, argv=0x7fffffffc108)
      at /home/steve/Documents/nav2_ws/src/gdb_test_pkg/src/main.cpp:25

在此示例中，你应该按以下方式从底部开始阅读：

- 在 main 函数中，第 25 行我们调用了函数 VectorCrash。

- 在 VectorCrash 中，第 44 行，我们在 Vector 的 ``at()`` 方法中以输入 ``100`` 崩溃了。

- 它是在 STL vector 第 1091 行的 ``at()`` 中崩溃的，此前抛出了来自范围检查失败的异常。

这些跟踪需要一些时间才能习惯阅读，但一般来说，从底部开始，沿堆栈向上追溯，直到看到它崩溃的那一行。
然后你就可以推断出它为什么崩溃。
当你用完 GDB 后，输入 ``quit``，它将退出会话并终止仍在运行的任何进程。
最后它可能会询问你是否要终止某些线程，回答 yes。

从 Launch 文件调试
------------------

正如在我们的非 ROS 示例中一样，我们需要在启动 ROS 2 launch 文件之前设置 GDB 会话。
虽然我们可以通过命令行来设置，但我们也可以利用在 ``ros2 run`` 节点示例中所用的相同机制，现在使用 launch 文件。

在你的 launch 文件中，找到你想要调试的节点。
在本节中，我们假设你的 launch 文件只包含一个节点（可能还包含其他信息）。
``launch_ros`` 包中使用的 ``Node`` 函数会接收一个字段 prefix，该字段接受一个前缀参数列表。
我们将在这里插入 GDB 代码片段。

**根据你的设置，考虑以下方法：**

- **带 GUI 的本地调试：** 如果你在本地调试并且有可用的 GUI 系统，请使用：

.. code-block:: python

  prefix=['xterm -e gdb -ex run --args']

这将提供更具交互性的调试体验。
基于 ``'start_sync_slam_toolbox_node'`` 进行调试的示例用例：

.. code-block:: python

  start_sync_slam_toolbox_node = Node(
    parameters=[
        get_package_share_directory("slam_toolbox") + '/config/mapper_params_online_sync.yaml',
        {'use_sim_time': use_sim_time}
    ],
    package='slam_toolbox',
    executable='sync_slam_toolbox_node',
    name='slam_toolbox',
    prefix=['xterm -e gdb -ex run --args'],  # For interactive GDB in a separate window/GUI
    output='screen')

- **远程调试（无 GUI）：** 如果没有 GUI 进行调试，请省略 ``xterm -e``：

.. code-block:: bash

  prefix=['gdb -ex run --args']

GDB 的输出和交互将发生在你启动 ROS 2 应用的那个终端会话中。
下面是 ``'start_sync_slam_toolbox_node'`` 的一个类似示例：

.. code-block:: python

  start_sync_slam_toolbox_node = Node(
    parameters=[
        get_package_share_directory("slam_toolbox") + '/config/mapper_params_online_sync.yaml',
        {'use_sim_time': use_sim_time}
    ],
    package='slam_toolbox',
    executable='sync_slam_toolbox_node',
    name='slam_toolbox',
    prefix=['gdb -ex run --args'],  # For GDB within the launch terminal
    output='screen')

与之前一样，此前缀会启动一个 GDB 会话，现在在 ``xterm`` 中，并使用定义的所有附加 launch 参数运行你请求的 launch 文件。

一旦你的节点崩溃，你会看到如下所示的提示符，现在在 ``xterm`` 会话中。
此时你可以获取回溯，并使用 `阅读堆栈跟踪`_ 中的说明来解读它。

从大型项目调试
--------------
使用包含多个节点的 launch 文件会略有不同，这样你就可以与 GDB 会话交互，而不会被同一终端中的其他日志所干扰。
因此，在处理较大的 launch 文件时，将你感兴趣的特定节点单独提取出来并单独启动是个好主意。

如果你感兴趣的节点是从嵌套的 launch 文件（例如被包含的 launch 文件）中启动的，你可能需要执行以下操作：

- 从父 launch 文件中注释掉对该 launch 文件的包含

- 使用 ``-g`` 标志重新编译感兴趣的包以生成调试符号

- 在一个终端中启动父 launch 文件

- 按照 `从 Launch 文件调试`_ 中的说明，在另一个终端中启动该节点的 launch 文件

或者，如果你感兴趣的节点是直接在这些文件中启动的（例如你看到 ``Node``、``LifecycleNode`` 或 ``ComponentContainer`` 内部），你需要将其与其他部分分离：

- 从父 launch 文件中注释掉对该节点的包含

- 使用 ``-g`` 标志重新编译感兴趣的包以生成调试符号

- 在一个终端中启动父 launch 文件

- 按照 `使用 GDB 调试特定节点`_ 中的说明，在另一个终端中启动该节点

.. note::

  在这种情况下，如果该节点之前由 launch 文件提供，你可能需要为其重新映射或提供参数文件。
  使用 ``--ros-args``，你可以为它提供新参数文件的路径、重映射或名称。
  有关所需的命令行参数，请参见 :doc:`本教程 <../../How-To-Guides/Node-arguments>`。

  我们理解这可能会很麻烦，因此这可能会促使你尽可能将每个节点作为一个单独包含的 launch 文件，以使调试更容易。
  一组示例参数可能是 ``--ros-args -r __node:=<node_name> --params-file /absolute/path/to/params.yaml`` （作为模板）。

一旦你的节点崩溃，你会在该特定节点的终端中看到如下所示的提示符。
此时你可以获取回溯，并使用 `阅读堆栈跟踪`_ 中的说明来解读它。

使用 GDB 调试测试
-----------------

如果 C++ 测试失败，可以直接在构建目录中对测试可执行文件使用 GDB。
确保以调试模式构建代码。
由于 CMake 可能缓存了之前的构建类型，请清理缓存并重新构建。

.. code-block:: console

  $ colcon build --cmake-clean-cache --mixin debug

为了让 GDB 为所调用的任何共享库加载调试符号，请确保 source 你的环境。
这会配置 ``LD_LIBRARY_PATH`` 的值。

.. code-block:: console

  $ source install/setup.bash

最后，直接通过 GDB 运行测试。
例如：

.. code-block:: console

  $ gdb -ex run ./build/rcl/test/test_logging

如果代码抛出了未处理的异常，你可以在 gtest 处理它之前在 GDB 中捕获它。

.. code-block:: console

  $ gdb ./build/rcl/test/test_logging
  $ catch throw
  $ run

崩溃时自动生成回溯
------------------

`backward-cpp <https://github.com/pal-robotics/backward_ros>`_ 库提供了漂亮的堆栈跟踪，而 `backward_ros <https://github.com/pal-robotics/backward_ros>`_ 封装简化了它的集成。

只需将其添加为依赖项并在你的 CMakeLists 中对其执行 ``find_package``，backward 库就会被注入到你的所有可执行文件和库中。
