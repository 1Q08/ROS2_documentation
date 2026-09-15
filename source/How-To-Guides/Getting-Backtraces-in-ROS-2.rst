在 ROS 2 中获取回溯
###################

.. contents:: 目录
   :local:

**目标：** 展示在 ROS 2 中获取回溯的多种方法

**教程级别：** 中级

**时间：** 15 分钟

以下步骤向 ROS 2 用户展示在遇到问题时如何获取回溯。

概述
----

**什么是回溯？**

- 把程序想象成一摞薄饼，每一张薄饼代表它当前正在执行的一个函数。
  回溯就像是对这摞倒塌薄饼拍下的一张照片，展示它们原本的顺序，揭示程序是如何走到失败的。
- 它列出了被调用的函数序列，一个叠在另一个之上，一直通向失败发生的位置。

**为什么它很有用？**

- **精准定位问题：** 无需猜测代码中出错的位置，回溯会直接告诉你导致崩溃的确切行号。
- **揭示上下文：** 你可以看到最终触发失败的事件链（函数调用其他函数）。
  这不仅能帮助你理解出错的位置，还能理解出错的原因。

**形象类比**：一摞薄饼

1. 每张薄饼就是一个函数：把一摞薄饼中的每一张都想象成程序当前正在执行的一个函数。
   最下面那张薄饼就是你的 main() 函数，一切都从这里开始。

2. 不断添加薄饼：每当一个函数调用另一个函数时，就会有一张新的薄饼被放到这摞薄饼的最上面。

3. 崩溃：崩溃就像盘子从这摞薄饼底部滑脱——当前正在执行的函数出了灾难性的问题。

4. 回溯：回溯就像对那摞倒塌的薄饼拍下的一张照片。
   它从下到上展示薄饼（函数）的顺序，揭示你是如何走到崩溃现场的。


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

**崩溃产生的回溯：**

.. code-block:: bash

  #0  functionC() at file.cpp:3 // Crash occurred here
  #1  functionB() at file.cpp:8
  #2  functionA() at file.cpp:13
  #3  main() at file.cpp:18

**回溯如何提供帮助：**

- **崩溃源头：** 显示 ``functionC()`` 中触发崩溃的确切行。
- **调用顺序：** 揭示 ``main()`` 调用了 ``functionA()``，后者调用了 ``functionB()``，最终导致 ``functionC()`` 中出错。

上面的示例让我们清楚地了解了什么是回溯以及它有什么用。
接下来，以下步骤将向 ROS 2 用户展示在遇到问题时如何从特定节点获取跟踪信息。
本教程既适用于仿真机器人，也适用于实体机器人。

内容将涵盖：如何使用 ``ros2 run`` 从特定节点获取回溯，如何使用 ``ros2 launch`` 从表示单个节点的启动文件获取回溯，以及如何从更复杂的节点编排中获取回溯。
学完本教程后，当你在 ROS 2 中注意到某个节点崩溃时，应当能够获取回溯。

预备知识
--------

GDB 是 Unix 系统上最流行的 C/C++ 调试器。
它可用于确定崩溃原因并跟踪线程。
它也可以用来在代码中添加断点，以便在软件的特定位置检查内存中的值。

对于所有从事 C/C++ 开发的软件开发者来说，使用 GDB 是一项关键技能。
尽管许多 IDE 都内置了某种调试器或性能分析器，但重要的是要理解如何使用手头这些原始工具，而不是依赖 IDE 来提供它们。
理解这些工具是 C/C++ 开发的基本功，把它完全交给 IDE 可能会带来麻烦：比如你换了岗位、不再能使用该 IDE，或者需要通过 ssh 会话对远程设备进行即时开发。

掌握基础知识之后，使用 GDB 其实相当简单。
下面说明如何确保你的 ROS 2 代码已为调试做好准备：

- 通过使用 ``--cmake-args``：包含调试符号最简单的方法是在 ``colcon build`` 命令中添加 ``--cmake-args -DCMAKE_BUILD_TYPE=Debug``：

.. code-block:: console

  $ colcon build --packages-up-to <package_name> --cmake-args -DCMAKE_BUILD_TYPE=Debug

- 通过编辑 ``CMakeLists.txt``：另一种方法是为你想分析/调试的 ROS 软件包的编译器标志添加 ``-g``。
  该标志会生成调试符号，GDB 可以读取它们，从而告诉你项目中具体哪几行代码失败以及原因。
  如果不设置该标志，你仍然可以获得回溯，但不会提供失败位置的行号。

现在你可以开始调试代码了！
如果这是一个非 ROS 项目，此时你可能会像下面这样做。
这里我们启动一个 GDB 会话，并让程序立即运行。
程序崩溃后，会返回一个由 ``(gdb)`` 表示的 gdb 会话提示符。
在该提示符下，你可以访问自己感兴趣的信息。
不过，由于这是一个 ROS 项目，涉及大量节点配置和其他事务，对于初学者，或者不喜欢大量命令行操作和文件系统知识的人来说，这并不是一个好选择。

.. code-block:: console

  $ gdb ex run --args /path/to/exe/program

以下各节描述了你在基于 ROS 2 的系统中可能遇到的三种主要情况。
请阅读最贴合你所要解决问题的那一节。

使用 GDB 调试特定节点
---------------------

要在启动 ROS 2 节点之前方便地建立 GDB 会话，可以利用 ``--prefix`` 选项。
用于 GDB 调试时，用法如下：

.. note::

  请记住，一个 ROS 2 可执行文件可能包含多个节点。
  ``--prefix`` 方法可确保你调试的是进程中正确的节点。

**为什么直接使用 GDB 可能会很棘手**

``--prefix`` 会在我们的 ROS 2 命令之前执行一些代码，从而让我们插入一些信息。
如果你像预备知识中的示例那样尝试执行 ``gdb ex run --args ros2 run <pkg> <node>``，你会发现它找不到 ``ros2`` 命令。
此外，在 GDB 内尝试 source 你的工作空间也会因类似原因失败。
这是因为以这种方式启动的 GDB 缺少通常让 ``ros2`` 命令可用的环境设置。

**使用 --prefix 简化流程**

我们不必退回到查找可执行文件的安装路径并把它完整敲出来，而是可以使用 ``--prefix``。
这样就能沿用你熟悉的 ``ros2 run`` 语法，而无需操心 GDB 的一些细节。

.. code-block:: console

  $ ros2 run --prefix 'gdb -ex run --args' <pkg> <node> --all-other-launch arguments

**GDB 使用体验**

和之前一样，该前缀会启动一个 GDB 会话，并带着所有附加命令行参数运行你请求的节点。
现在你的节点应该已经运行起来，并伴随着一些调试打印信息继续工作。

阅读堆栈回溯
------------

使用 GDB 获得回溯之后，可以这样解读它：

- 从底部开始：回溯按时间倒序列出函数调用。
  最底部的函数就是崩溃的源头。

- 沿堆栈向上追溯：上面的每一行都代表调用其下方函数的那个函数。
  一直向上追溯，直到进入你自己项目中的某一行代码。
  这通常能揭示问题最初发生在哪里。

- 调试线索：函数名及其参数可以为你提供有关出错原因的宝贵线索。

**节点崩溃后如何调试**

节点崩溃后，你会看到类似下面的提示符。
此时你就可以获取回溯了。

.. code-block:: bash

  (gdb)

在该会话中输入 ``backtrace``，它就会给出回溯。
按需复制下来即可。


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

在这个示例中，你应该从底部开始，按以下方式解读：

- 在 main 函数中，第 25 行我们调用了 VectorCrash 函数。

- 在 VectorCrash 中，第 44 行我们在 Vector 的 ``at()`` 方法中、以输入 ``100`` 发生了崩溃。

- 它在 ``at()`` 中因范围检查失败抛出异常后，于 STL vector 第 1091 行崩溃。

阅读这些回溯需要一些时间来适应，但总体而言，从底部开始沿堆栈向上看，直到找到发生崩溃的那一行。
然后就可以推断出崩溃的原因。
GDB 使用完毕后，输入 ``quit``，它会退出会话并终止仍在运行的进程。
最后它可能会询问你是否要终止某些线程，回答是即可。

从启动文件启动
--------------

和我们的非 ROS 示例一样，在启动 ROS 2 启动文件之前，我们需要先建立 GDB 会话。
虽然可以通过命令行来设置，但我们也可以沿用 ``ros2 run`` 节点示例中的相同机制，只不过这里用的是启动文件。

在你的启动文件中，找到你想调试的节点。
本节假设你的启动文件只包含一个节点（也可能包含其他信息）。
``launch_ros`` 软件包中使用的 ``Node`` 函数会接收一个 prefix 字段，其值为一个前缀参数列表。
我们将在该处插入 GDB 片段。

**请根据你的环境考虑以下方法：**

- **带 GUI 的本地调试：** 如果你在本地调试并且有可用的 GUI 系统，请使用：

.. code-block:: python

  prefix=['xterm -e gdb -ex run --args']

这会提供更具交互性的调试体验。
以下是基于 ``'start_sync_slam_toolbox_node'`` 的调试示例用法 -

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

- **远程调试（无 GUI）：** 如果在没有 GUI 的情况下调试，请省略 ``xterm -e``：

.. code-block:: bash

  prefix=['gdb -ex run --args']

GDB 的输出和交互会发生在你启动 ROS 2 应用程序的那个终端会话中。
以下是 ``'start_sync_slam_toolbox_node'`` 的类似示例 -

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

和之前一样，该前缀会启动一个 GDB 会话（此时位于 ``xterm`` 中），并带着所有已定义的附加启动参数运行你请求的启动文件。

节点崩溃后，你会看到类似下面的提示符，此时位于 ``xterm`` 会话中。
此时你就可以获取回溯，并按 `阅读堆栈回溯`_ 中的说明来阅读它。

从大型项目启动
--------------
处理包含多个节点的启动文件稍有不同，这样你与 GDB 会话交互时就不会被同一终端中的其他日志淹没。
因此，在处理较大的启动文件时，最好把你关注的特定节点单独提出来并单独启动。

如果你关注的节点是从嵌套启动文件（例如被包含的启动文件）中启动的，你可能需要这样做：

- 在父启动文件中注释掉对该启动文件的包含

- 使用 ``-g`` 标志重新编译你关注的软件包以获得调试符号

- 在一个终端中启动父启动文件

- 按照 `从启动文件启动`_ 中的说明，在另一个终端中启动该节点的启动文件

或者，如果你关注的节点是在这些文件中直接启动的（例如你看到 ``Node``、``LifecycleNode``，或者它在 ``ComponentContainer`` 内部），则需要把它与其他部分分开：

- 在父启动文件中注释掉对该节点的包含

- 使用 ``-g`` 标志重新编译你关注的软件包以获得调试符号

- 在一个终端中启动父启动文件

- 按照 `使用 GDB 调试特定节点`_ 中的说明，在另一个终端中启动该节点

.. note::

  在这种情况下，如果该节点此前是由启动文件提供的，你可能需要为其重映射或提供参数文件。
  使用 ``--ros-args`` 可以为其指定新的参数文件路径、重映射或名称。
  所需的命令行参数请参见 :doc:`本教程 <../../How-To-Guides/Node-arguments>`。

  我们理解这可能很麻烦，因此建议你尽可能让每个节点都作为单独包含的启动文件，以便更轻松地调试。
  一组示例参数可以是 ``--ros-args -r __node:=<node_name> --params-file /absolute/path/to/params.yaml`` （作为模板）。

节点崩溃后，你会在该特定节点的终端中看到类似下面的提示符。
此时你就可以获取回溯，并按 `阅读堆栈回溯`_ 中的说明来阅读它。

使用 GDB 调试测试
-----------------

如果某个 C++ 测试失败，可以直接对构建目录中的测试可执行文件使用 GDB。
请确保以调试模式构建代码。
由于先前的构建类型可能已被 CMake 缓存，需要清理缓存并重新构建。

.. code-block:: console

  $ colcon build --cmake-clean-cache --mixin debug

为了让 GDB 能为所调用的任何共享库加载调试符号，请务必 source 你的环境。
这会配置 ``LD_LIBRARY_PATH`` 的值。

.. code-block:: console

  $ source install/setup.bash

最后，直接通过 GDB 运行该测试。
例如：

.. code-block:: console

  $ gdb -ex run ./build/rcl/test/test_logging

如果代码抛出了未处理的异常，你可以在 gtest 处理它之前先在 GDB 中捕获它。

.. code-block:: console

  $ gdb ./build/rcl/test/test_logging
  $ catch throw
  $ run

崩溃时自动获取回溯
------------------

`backward-cpp <https://github.com/pal-robotics/backward_ros>`_ 库可以提供漂亮的堆栈回溯，而 `backward_ros <https://github.com/pal-robotics/backward_ros>`_ 封装则简化了它的集成。

只需将它添加为依赖项，并在你的 CMakeLists 中调用 ``find_package``，backward 库就会被注入到你所有的可执行文件和库中。
