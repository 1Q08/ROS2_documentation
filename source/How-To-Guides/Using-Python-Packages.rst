.. redirect-from::

  Guides/Using-Python-Packages
  Tutorials/Using-Python-Packages

.. _PythonPackages:

在 ROS 2 中使用 Python 包
=========================

**目标：** 说明如何与 ROS 2 生态中的其他 Python 包进行互操作。

.. contents:: Contents
    :depth: 2
    :local:

.. note::

    一个需要注意的提醒：如果你打算使用预打包的二进制文件
    （无论是 ``deb`` 文件，还是二进制归档发行版），Python 解释器必须与
    构建原始二进制文件时使用的解释器一致。
    如果你打算使用 ``virtualenv`` 或 ``pipenv``\ 之类的东西，请务必使用系统解释器。
    如果你使用 ``conda`` 之类的东西，解释器很可能与系统解释器不一致，
    并且会与 ROS 2 二进制文件不兼容。

通过 ``rosdep`` 安装
--------------------

引入第三方 Python 包的最快方式是使用它们对应的 rosdep 键（如果可用的话）。
可以通过以下地址检查 ``rosdep`` 键：

* https://github.com/ros/rosdistro/blob/master/rosdep/base.yaml
* https://github.com/ros/rosdistro/blob/master/rosdep/python.yaml

这些 ``rosdep`` 键可以添加到你的 ``package.xml`` 文件中，
这将向构建系统表明你的包（以及依赖的包）依赖这些键。
在一个新的工作空间中，你也可以通过以下命令快速安装所有 rosdep 键：

.. code-block:: console

    $ rosdep install -yr --from-paths ./path/to/your/workspace

如果你感兴趣的包目前还没有 ``rosdep`` 键，
可以按照 `rosdep 键贡献指南`_ 来添加它们。

要了解关于 ``rosdep`` 工具及其工作原理的更多信息，请查阅 `rosdep 文档`_。

通过包管理器安装
----------------

如果你不想创建 rosdep 键，但该包在你的系统包管理器
（例如 ``apt``）中可用，你可以通过这种方式安装并使用该包：

.. code-block:: console

    $ sudo apt install python3-serial

如果该包在 `Python 软件包索引 (PyPI) <https://pypi.org/>`_ 上可用，
并且你想在系统上全局安装：

.. code-block:: console

    $ python3 -m pip install -U pyserial

如果该包在 PyPI 上可用，并且你想安装到本地用户：

.. code-block:: console

    $ python3 -m pip install -U --user pyserial

通过虚拟环境安装
----------------

首先，创建一个 Colcon 工作空间：

.. code-block:: console

    $ mkdir -p ~/colcon_venv/src
    $ cd ~/colcon_venv/

然后设置你的虚拟环境：

.. code-block:: console

    $ virtualenv -p python3 ./venv # 创建一个虚拟环境并激活它
    $ source ./venv/bin/activate
    $ touch ./venv/COLCON_IGNORE # 确保 colcon 不会尝试构建该 venv

接下来，在你想要使用的虚拟环境中安装 Python 包：

.. code-block:: console

    $ python3 -m pip install gtsam pyserial… etc

现在你可以构建工作空间，并运行依赖虚拟环境中已安装包的 Python 节点了。

.. code-block:: console

    $ source /opt/ros/{DISTRO}/setup.bash # Source {DISTRO_TITLE} 并构建
    $ colcon build

.. note::

    如果你希望使用 Bloom 发布你的包，你应该把所需的包添加到 ``rosdep`` 中，
    参见 `rosdep 键贡献指南`_。

.. _rosdep 键贡献指南: http://docs.ros.org/en/independent/api/rosdep/html/contributing_rules.html

.. _rosdep 文档: http://docs.ros.org/en/independent/api/rosdep/html/
