.. redirect-from::

    Real-Time-Programming
    Tutorials/Real-Time-Programming

理解实时编程
============

.. contents:: 目录
   :depth: 2
   :local:

背景
----

实时计算是许多机器人系统的关键特性，尤其是安全关键和任务关键型应用，例如自动驾驶汽车、航天器和工业制造。
我们在设计和原型化 ROS 2 时考虑了实时性能约束，因为这是 ROS 1 早期阶段未考虑的需求，而现在重构 ROS 1 使其对实时友好已经变得难以实现。

`本文档 <https://design.ros2.org/articles/realtime_background.html>`__ 概述了实时计算的需求以及面向软件工程师的最佳实践。
简而言之：

要构建实时计算机系统，我们的实时循环必须定期更新以满足截止时间。
我们只能容忍这些截止时间上的很小误差（我们允许的最大抖动）。
为此，我们必须避免执行路径中的非确定性操作，例如：缺页事件、动态内存分配/释放，以及无限期阻塞的同步原语。

一个经典的、通常由实时计算解决的控制问题示例是平衡一个 `倒立摆 <https://en.wikipedia.org/wiki/Inverted_pendulum>`__。
如果控制器阻塞了出乎意料长的时间，摆就会倒下或变得不稳定。
但如果控制器可靠地以比控制摆的电机运行速度更快的速率更新，摆将成功地根据传感器数据自适应反应以保持平衡。

既然你已经了解了关于实时计算的一切，让我们试试演示！

安装并运行演示
--------------

实时演示是面向 Linux 操作系统编写的，因为 ROS 社区中许多做实时计算的成员使用 Xenomai 或 RT_PREEMPT 作为他们的实时解决方案。
由于演示中为优化性能所做的许多操作都是 OS 特定的，该演示只能在 Linux 系统上构建和运行。
**所以，如果你是 OSX 或 Windows 用户，不要尝试这一部分！**

此外，这必须使用静态 DDS API 从源代码构建。
**目前唯一支持的实现是 ConnextDDS**。

首先，按照说明使用 Connext DDS 作为中间件从源代码 :doc:`构建 ROS 2 <../../Installation/Alternatives/Ubuntu-Development-Setup>`。

运行测试
^^^^^^^^

**运行之前请确保你至少有 8Gb 的空闲 RAM。
一旦锁定了内存，swap 将不再工作。**

Source 你的 ROS 2 ``setup.bash``：

.. code-block:: console

   $ source ./install/setup.bash

运行演示二进制文件。
如果你遇到权限错误，可能需要使用 ``sudo``：

.. code-block:: console

   $ ros2 run pendulum_control pendulum_demo
   Initial major pagefaults: 518
   Initial minor pagefaults: 2139466
   No results filename given, not writing results
   rttest statistics:
   - Minor pagefaults: 0
   - Major pagefaults: 0
   Latency (time after deadline was missed):
      - Min: 1851 ns
      - Max: 166796 ns
      - Mean: 14229.182000 ns
      - Standard deviation: 12288.040996

你可能会看到以下错误输出到控制台（来自 stderr）：

.. code-block:: console

   mlockall failed: Cannot allocate memory
   Couldn't lock all cached virtual memory.
   Pagefaults from reading pages not yet mapped into RAM will be recorded.

在演示程序的初始化阶段之后，它将尝试把所有缓存的内存锁到 RAM 中，并使用 ``mlockall`` 阻止未来的动态内存分配。
这是为了防止加载大量新内存到 RAM 时产生缺页。
（更多信息请参阅 `实时设计文章 <https://design.ros2.org/articles/realtime_background.html#memory-management>`__。）

发生这种情况时，演示会照常继续。
你还可能看到如下输出，它表示执行期间遇到的缺页次数：

::

   rttest statistics:
     - Minor pagefaults: 20
     - Major pagefaults: 0

如果我们想让那些缺页消失，我们就必须...

调整内存锁定的权限
^^^^^^^^^^^^^^^^^^

（以 sudo 身份）添加到 ``/etc/security/limits.conf``：

::

   <你的用户名>    -   memlock   <限制（kB）>

限制为 ``-1`` 表示无限制。
如果你选择这个，可能需要在编辑文件后（以 root 身份）配合执行 ``ulimit -l unlimited``。

保存文件后，注销并重新登录。
然后重新运行 ``pendulum_demo`` 调用。

你要么会在输出文件中看到零缺页，要么会看到一个错误，说明捕获到 bad_alloc 异常。
如果发生这种情况，说明你没有足够的空闲内存来将进程分配的内存锁到 RAM 中。
你需要为计算机安装更多 RAM 才能看到零缺页！

输出概览
^^^^^^^^

要看到更多输出，我们必须运行 ``pendulum_logger`` 节点。

在一个已 source 你的 ``install/setup.bash`` 的 shell 中，执行：

.. code-block:: console

   $ ros2 run pendulum_control pendulum_logger


你应该会看到输出消息：

::

   Logger node initialized.

在另一个已 source setup.bash 的 shell 中，再次调用 ``pendulum_demo``。

一旦这个可执行文件启动，你应该会看到另一个 shell 不断打印输出：

::

   Commanded motor angle: 1.570796
   Actual motor angle: 1.570796
   Mean latency: 210144.000000 ns
   Min latency: 4805 ns
   Max latency: 578137 ns
   Minor pagefaults during execution: 0
   Major pagefaults during execution: 0

该演示控制着一个非常简单的倒立摆模拟。
摆模拟在其自己的线程中计算其位置。
一个 ROS 节点模拟摆的电机编码器传感器并发布其位置。
另一个 ROS 节点充当简单的 PID 控制器并计算下一条命令消息。

logger 节点定期打印摆的状态，以及演示在执行阶段的运行时性能统计。

``pendulum_demo`` 完成后，你必须 CTRL-C 退出 logger 节点。

延迟
^^^^

在 ``pendulum_demo`` 执行时，你会看到为演示收集的最终统计：

::

   rttest statistics:
     - Minor pagefaults: 0
     - Major pagefaults: 0
     Latency (time after deadline was missed):
       - Min: 3354 ns
       - Max: 2752187 ns
       - Mean: 19871.8 ns
       - Standard deviation: 1.35819e+08

   PendulumMotor received 985 messages
   PendulumController received 987 messages

延迟字段以纳秒为单位显示更新循环的最小、最大和平均延迟。
这里，延迟是指更新预期发生之后过去的时间量。

实时系统的需求取决于应用，但假设在本演示中我们有一个 1kHz（1 毫秒）的更新循环，我们的目标是允许的最大延迟为更新周期的 5%。

所以，这次运行中我们的平均延迟真的很好，但最大延迟是不可接受的，因为它实际上超出了我们的更新循环！
发生了什么？

我们可能正受到非确定性调度器的影响。
如果你运行的是原生 Linux 系统，且没有安装 RT_PREEMPT 内核，你可能无法达到我们为自己设定的实时目标，因为 Linux 调度器不允许你在用户级别任意抢占线程。

更多信息请参阅 `实时设计文章 <https://design.ros2.org/articles/realtime_background.html#multithreaded-programming-and-synchronization>`__。

该演示尝试将演示的调度器和线程优先级设置为适合实时性能的值。
如果此操作失败，你会看到错误消息：“Couldn't set scheduling priority and policy: Operation not permitted”。
你可以按照下一节的说明获得略好的性能：

设置调度器的权限
^^^^^^^^^^^^^^^^

（以 sudo 身份）添加到 ``/etc/security/limits.conf``：

::

   <你的用户名>    -   rtprio   98

rtprio（实时优先级）字段的范围是 0-99。
但是，不要将限制设置为 99，因为那样你的进程可能会干扰以最高优先级运行的重要系统进程（例如 watchdog）。
本演示将尝试以优先级 98 运行控制循环。

绘制结果
^^^^^^^^

你可以在演示运行后绘制本演示中收集的延迟和缺页统计。

由于代码已经用 `rttest <https://github.com/ros2/rttest>`__ 进行了插桩，因此有一些有用的命令行参数可用：

+---------+---------------------------------------------------------------------+---------------+
| 命令    | 描述                                                                | 默认值        |
+---------+---------------------------------------------------------------------+---------------+
| -i      | 指定实时循环要运行的迭代次数                                        | 1000          |
+---------+---------------------------------------------------------------------+---------------+
| -u      | 指定更新周期，默认单位为微秒                                        | 1ms           |
|         |                                                                     |               |
|         | 使用后缀 "s" 表示秒，"ms" 表示毫秒，                                |               |
|         |                                                                     |               |
|         | "us" 表示微秒，"ns" 表示纳秒                                        |               |
+---------+---------------------------------------------------------------------+---------------+
| -f      | 指定写入收集数据的文件名                                            |               |
+---------+---------------------------------------------------------------------+---------------+

再次运行演示，并指定保存结果的文件名：

.. code-block:: console

   $ ros2 run pendulum_control pendulum_demo -f pendulum_demo_results

然后在生成的文件上运行 ``rttest_plot`` 脚本：

.. code-block:: console

   $ ros2 run rttest rttest_plot pendulum_demo_results
   Writing results to file: pendulum_demo_results
   ...

此脚本将生成许多文件：

::

   pendulum_demo_results_plot_latency.svg
   pendulum_demo_results_plot_latency_hist.svg
   pendulum_demo_results_plot_majflts.svg
   pendulum_demo_results_plot_minflts.svg

你可以在你选择的图像查看器中查看这些绘图。
