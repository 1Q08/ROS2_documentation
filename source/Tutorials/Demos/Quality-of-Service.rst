.. redirect-from::

    Quality-of-Service
    Tutorials/Quality-of-Service

为有损网络使用服务质量设置
==========================

.. contents:: 目录
   :depth: 2
   :local:

背景
----

请阅读 `关于 QoS 设置 <../../Concepts/Intermediate/About-Quality-of-Service-Settings>` 的文档页面，了解 ROS 2 中可用支持的背景信息。

在本演示中，我们将生成一个发布摄像头图像的节点，以及另一个订阅该图像并在屏幕上显示的节点。
然后我们将模拟它们之间的有损网络连接，并展示不同的服务质量设置如何处理这种糟糕的链路。


前置条件
--------
本教程假设你有一个 :doc:`可工作的 ROS 2 安装 <../../Installation>` 和 OpenCV。
有关其安装说明，请参阅 `OpenCV 文档 <http://docs.opencv.org/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html#table-of-content-introduction>`__。
你还需要 ROS 软件包 ``image_tools``。

.. tabs::

   .. group-tab:: Linux Binaries

      .. code-block:: console

        $ sudo apt-get install ros-{DISTRO}-image-tools

   .. group-tab:: 从源代码

      使用与你的安装匹配的分支克隆并构建 demos 仓库。

      .. code-block:: console

        $ git clone https://github.com/ros2/demos.git -b {REPOS_FILE_BRANCH}


运行演示
--------

在运行演示之前，请确保你有一个可用的摄像头连接到你的计算机。

安装 ROS 2 后，source 你的设置文件：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ . <path to ROS 2 install space>/setup.bash

  .. group-tab:: macOS

    .. code-block:: console

       $ . <path to ROS 2 install space>/setup.bash

  .. group-tab:: Windows

    .. code-block:: console

       $ call <path to ROS 2 install space>/local_setup.bat

然后运行：

.. code-block:: console

   $ ros2 run image_tools showimage

暂时还不会发生任何事。
``showimage`` 是一个订阅者节点，正在等待 ``image`` 话题上的发布者。

注意：你之后必须用 ``Ctrl-C`` 关闭 ``showimage`` 进程。
你不能只是关闭窗口。

在一个单独的终端中，source 安装文件并运行发布者节点：

.. code-block:: console

   $ ros2 run image_tools cam2image

这将从你的摄像头发布图像。
如果你的计算机没有连接摄像头，有一个命令行选项可以发布预定义图像。


.. code-block:: console

   $ ros2 run image_tools cam2image --ros-args -p burger_mode:=True
   [INFO] [1715662452.055277255] [cam2image]: Publishing image #1
   [INFO] [1715662452.119336061] [cam2image]: Publishing image #2
   [INFO] [1715662452.187315139] [cam2image]: Publishing image #3
   ...

一个标题为 “view” 的窗口会弹出，显示你的摄像头画面。
在第一个窗口中，你会看到订阅者的输出：

.. code-block:: console

   [INFO] [1715662452.188906764] [showimage]: Received image #camera_frame
   Received image #camera_frame
   [INFO] [1715662452.252836919] [showimage]: Received image #camera_frame
   Received image #camera_frame
   [INFO] [1715662452.320878578] [showimage]: Received image #camera_frame
   Received image #camera_frame
   ...

.. note::

   macOS 用户：如果这些示例无法运行，或者你收到类似 ``ddsi_conn_write failed -1`` 的错误，那么你需要增大系统范围的 UDP 数据包大小：

   .. code-block:: console

      $ sudo sysctl -w net.inet.udp.recvspace=209715
      $ sudo sysctl -w net.inet.udp.maxdgram=65500

   这些更改在重启后不会保留。
   如果你想让更改持久化，请将这些行添加到 ``/etc/sysctl.conf`` （如果文件不存在则先创建）：

   .. code-block:: bash

      net.inet.udp.recvspace=209715
      net.inet.udp.maxdgram=65500

命令行选项
^^^^^^^^^^

在你的其中一个终端中，给原始命令加上 -h 标志：


.. code-block:: console

   $ ros2 run image_tools showimage -h



添加网络流量
^^^^^^^^^^^^

.. warning::

  本演示的这一部分在 RTI 的 Connext DDS 和 Fast-DDS 上无法工作。
  当在同一主机上运行多个节点时，这些 DDS 实现会使用共享内存以及回环接口。
  降低回环接口的吞吐量不会影响共享内存，因此两个节点之间的流量不会受到影响。

.. note::

   下一部分是 Linux 专属的。

   不过，对于 macOS 和 Windows，你可以分别使用 “Network Link Conditioner” 工具（xcode 工具套件的一部分）和 `“Clumsy” <http://jagt.github.io/clumsy/index.html>`_ 实现类似效果，但本教程不涵盖它们。

我们将使用 Linux 网络流量控制工具 ``tc`` （`man 手册页 <http://linux.die.net/man/8/tc>`_）。

.. code-block:: console

   $ sudo tc qdisc add dev lo root netem loss 5%

这个神奇的咒语将在本地回环设备上模拟 5% 的数据包丢失。
如果你使用更高分辨率的图像（例如 ``--ros-args -p width:=640 -p height:=480``），你可能想尝试更低的数据包丢失率（例如 ``1%``）。

接下来我们启动 ``cam2image`` 和 ``showimage``，我们很快就会注意到两个程序似乎都减慢了图像传输的速率。
这是由默认 QoS 设置的行为引起的。
在有损信道上强制可靠性意味着发布者（本例中为 ``cam2image``）会重新发送网络数据包，直到收到消费者（即 ``showimage``）的确认。

现在让我们尝试运行这两个程序，但使用更合适的设置。
首先，我们将使用 ``-p reliability:=best_effort`` 选项来启用尽力而为（best effort）通信。
现在发布者只会尝试投递网络数据包，不期望消费者的确认。
我们现在看到 ``showimage`` 一侧的某些帧被丢弃了，因此运行 ``showimage`` 的 shell 中的帧号不再连续：


.. image:: https://raw.githubusercontent.com/ros2/demos/{REPOS_FILE_BRANCH}/image_tools/doc/qos-best-effort.png
   :target: https://raw.githubusercontent.com/ros2/demos/{REPOS_FILE_BRANCH}/image_tools/doc/qos-best-effort.png
   :alt: Best effort image transfer


完成后，记得删除排队规则：

.. code-block:: console

   $ sudo tc qdisc delete dev lo root netem loss 5%
