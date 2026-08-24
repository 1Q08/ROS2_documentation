.. redirect-from::

    Tutorials/Run-2-nodes-in-a-single-docker-container
    Tutorials/Run-2-nodes-in-two-separate-docker-containers
    Guides/Run-2-nodes-in-two-separate-docker-containers

在 Docker 中运行 ROS 2 节点 [社区贡献]
======================================

在单个 Docker 容器中运行两个节点
--------------------------------

拉取带有标签 "{DISTRO}-desktop" 的 ROS Docker 镜像。

.. code-block:: console

   $ docker pull osrf/ros:{DISTRO}-desktop


在交互模式下于容器中运行该镜像。

.. code-block:: console

   $ docker run -it osrf/ros:{DISTRO}-desktop

现在你最好的朋友是 ``ros2`` 命令行帮助。

.. code-block:: console

   $ ros2 --help

例如，列出所有已安装的包。

.. code-block:: console

   $ ros2 pkg list
   (you will see a list of packages)


例如，列出所有可执行文件：

.. code-block:: console

   $ ros2 pkg executables
   (you will see a list of <package> <executable>)


在此容器中运行一个包含 2 个 C++ 节点（1 个话题订阅者 ``listener``，1 个话题发布者 ``talker``）的最小示例，它们来自包 ``demo_nodes_cpp``：

.. code-block:: console

   $ ros2 run demo_nodes_cpp listener &
   $ ros2 run demo_nodes_cpp talker

在两个独立的 Docker 容器中运行两个节点
--------------------------------------

打开一个终端。
在交互模式下于容器中运行镜像，并使用 ``ros2 run`` 启动一个话题发布者（来自包 ``demo_nodes_cpp`` 的可执行文件 ``talker``）：

.. code-block:: console

   $ docker run -it --rm osrf/ros:{DISTRO}-desktop ros2 run demo_nodes_cpp talker

打开第二个终端。
在交互模式下于容器中运行镜像，并使用 ``ros2 run`` 启动一个话题订阅者（来自包 ``demo_nodes_cpp`` 的可执行文件 ``listener``）：

.. code-block:: console

   $ docker run -it --rm osrf/ros:{DISTRO}-desktop ros2 run demo_nodes_cpp listener

作为命令行调用的替代方案，你可以创建一个 ``docker-compose.yml`` 文件（此处为版本 2），内容如下（最小内容）：

.. code-block:: yaml

   version: '2'

   services:
     talker:
       image: osrf/ros:{DISTRO}-desktop
       command: ros2 run demo_nodes_cpp talker
     listener:
       image: osrf/ros:{DISTRO}-desktop
       command: ros2 run demo_nodes_cpp listener
       depends_on:
         - talker

要运行这些容器，请在同一目录中调用 ``docker compose up``。
你可以使用 ``Ctrl+C`` 关闭这些容器。
