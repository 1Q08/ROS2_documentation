.. redirect-from::

    Tutorials/Getting-Started-With-Ros2doctor

.. _Ros2Doctor:

使用 ``ros2doctor`` 识别问题
============================

**目标：** 使用 ``ros2doctor`` 工具识别你的 ROS 2 设置中的问题。

**教程级别：** 入门

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

当你的 ROS 2 设置未按预期运行时，你可以使用 ``ros2doctor`` 工具检查其设置。

``ros2doctor`` 会检查 ROS 2 的方方面面，包括平台、版本、网络、环境、运行中的系统等等，并就可能的错误和问题原因向你发出警告。

前置条件
--------

``ros2doctor`` 是 ``ros2cli`` 包的一部分。
只要安装了 ``ros2cli``（任何正常的安装都应该有），你就能使用 ``ros2doctor``。

本教程使用 :doc:`turtlesim <../Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim>` 来说明一些示例。

任务
----

1 检查你的设置
^^^^^^^^^^^^^^

让我们用 ``ros2doctor`` 整体检查你的常规 ROS 2 设置。
首先，在一个新终端中导入 ROS 2，然后输入命令：


.. code-block:: console

    $ ros2 doctor
    All <n> checks passed

这会对你的所有设置模块进行检查，并返回警告和错误。
如果你的 ROS 2 设置处于完美状态，你会看到类似上面的消息。

但是，返回几条警告并不罕见。
``UserWarning`` 并不意味着你的设置不可用；它更可能只是提示某个东西的配置方式不够理想。

如果你确实收到了警告，它会看起来像这样：

.. code-block:: console

    <path>: <line>: UserWarning: <message>

例如，如果你使用的是不稳定的 ROS 2 发行版，``ros2doctor`` 会发现这个警告：

.. code-block:: console

    UserWarning: Distribution <distro> is not fully supported or tested. To get more consistent features, download a stable version at https://index.ros.org/doc/ros2/Installation/

如果 ``ros2doctor`` 只在你的系统中发现警告，你仍然会收到 ``All <n> checks passed`` 消息。

大多数检查都被归类为警告而非错误。
``ros2doctor`` 返回的反馈的重要性，主要由你（用户）来决定。
如果它确实在你的设置中发现了一个罕见的错误（以 ``UserWarning: ERROR:`` 表示），那么该检查被认为是失败的。

你会看到类似以下问题反馈列表的消息：

.. code-block:: console

  1/3 checks failed

  Failed modules:  network

错误表示系统缺少对 ROS 2 至关重要的设置或功能。
应该解决错误，以确保系统正常运行。

2 检查一个系统
^^^^^^^^^^^^^^

你也可以检查一个正在运行的 ROS 2 系统，以识别问题的可能原因。
要看到 ``ros2doctor`` 在运行中的系统上的工作，让我们运行 turtlesim，它有一些节点在积极相互通信。

通过打开一个新终端、导入 ROS 2 并输入以下命令来启动系统：

.. code-block:: console

    $ ros2 run turtlesim turtlesim_node

打开另一个终端并导入 ROS 2 以运行 teleop 控制：

.. code-block:: console

    $ ros2 run turtlesim turtle_teleop_key

现在在它自己的终端中再次运行 ``ros2doctor``。
如果你上次运行时有警告和错误，你将看到它们。
紧随其后的将是一些与系统本身相关的新警告：

.. code-block:: console

    $ ros2 doctor
    UserWarning: Publisher without subscriber detected on /turtle1/color_sensor.
    UserWarning: Publisher without subscriber detected on /turtle1/pose.

看起来 ``/turtlesim`` 节点向两个没有被订阅的话题发布数据，而 ``ros2doctor`` 认为这可能会导致问题。

如果你运行命令来回显 ``/color_sensor`` 和 ``/pose`` 话题，这些警告就会消失，因为发布者将拥有订阅者。

你可以在 turtlesim 仍在运行时打开两个新终端，在每个终端中导入 ROS 2，并在各自的终端中运行以下每个命令来尝试：

.. code-block:: console

    $ ros2 topic echo /turtle1/color_sensor

.. code-block:: console

    $ ros2 topic echo /turtle1/pose

然后再次在其终端中运行 ``ros2doctor``。
``publisher without subscriber`` 警告将消失。
（务必在运行 ``echo`` 的终端中输入 ``Ctrl+C``）。

现在尝试退出 turtlesim 窗口或退出 teleop，然后再次运行 ``ros2doctor``。
你将看到更多警告，指示不同话题的 ``publisher without subscriber`` 或 ``subscriber without publisher``，因为现在系统中的某个节点不可用了。

在拥有许多节点的复杂系统中，``ros2doctor`` 对于识别通信问题的可能原因将非常有价值。

3 获取完整报告
^^^^^^^^^^^^^^

虽然 ``ros2doctor`` 会告知你关于网络、系统等的警告，但使用 ``--report`` 参数运行它可以为你提供更多细节，以帮助你分析问题。

如果你收到关于网络设置的警告，并想找出配置中到底哪个部分导致了该警告，你可能需要使用 ``--report``。

当你需要提交支持工单以获得 ROS 2 帮助时，它也很有用。
你可以将报告中的相关部分复制粘贴到工单中，这样帮助你的人就能更好地理解你的环境并提供更好的帮助。

要获取完整报告，请在终端中输入以下命令：

.. code-block:: console

    $ ros2 doctor --report

这将返回一个分成五组的信息列表：

.. code-block:: console

  NETWORK CONFIGURATION
  ...

  PLATFORM INFORMATION
  ...

  RMW MIDDLEWARE
  ...

  ROS 2 INFORMATION
  ...

  TOPIC LIST
  ...

你可以将这里的信息与你运行 ``ros2 doctor`` 时得到的警告进行交叉核对。
例如，如果 ``ros2doctor`` 返回了（前面提到的）你的发行版“未完全支持或测试”的警告，你可能会查看报告的 ``ROS 2 INFORMATION`` 部分：

.. code-block:: console

  distribution name      : <distro>
  distribution type      : ros2
  distribution status    : prerelease
  release platforms      : {'<platform>': ['<version>']}

在这里你可以看到 ``distribution status`` 是 ``prerelease``，这解释了为什么它未被完全支持。


小结
----

``ros2doctor`` 会告知你 ROS 2 设置和运行系统中的问题。
你可以通过使用 ``--report`` 参数更深入地了解这些警告背后的信息。

请记住，``ros2doctor`` 不是一个调试工具；它不会帮助你处理代码中的错误或系统实现方面的问题。


相关内容
--------

`ros2doctor 的 README <https://github.com/ros2/ros2cli/tree/{REPOS_FILE_BRANCH}/ros2doctor>`__ 会告诉你更多关于不同参数的信息。
你可能也想浏览一下 ``ros2doctor`` 仓库，因为它相当适合初学者，是开始参与贡献的好地方。

下一步
------

你已完成入门级教程！
