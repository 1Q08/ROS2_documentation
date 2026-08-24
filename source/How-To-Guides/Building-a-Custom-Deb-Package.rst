.. redirect-from::

  Guides/Building-a-Custom-Debian-Package
  How-To-Guides/Building-a-Custom-Debian-Package

构建自定义 deb 包
=================

许多 Ubuntu 用户通过安装 :doc:`deb 包 <../Installation/Ubuntu-Install-Debs>` 在其系统上安装 ROS 2。
本指南提供了一组简短的指令，用于构建本地的自定义 deb 包。

.. contents:: 目录
   :local:

先决条件
--------

要成功构建自定义包，待构建包的所有依赖项都必须可在本地或 rosdep 中获得。
此外，包的所有依赖项都应在该包的 ``package.xml`` 文件中正确声明。

安装依赖项
----------

运行以下命令安装构建所需的实用工具：

.. code:: console

  $ sudo apt install python3-bloom python3-rosdep fakeroot debhelper dh-python

初始化 rosdep
-------------

通过以下调用初始化 rosdep 数据库：

.. code:: console

  $ sudo rosdep init
  $ rosdep update

请注意，如果过去已经初始化过，``rosdep init`` 命令可能会失败；这可以安全地忽略。

从包构建 deb
------------

运行以下命令构建 deb：

.. code:: console

  $ cd /path/to/pkg_source  # 这应该是包含 package.xml 的目录
  $ bloom-generate rosdebian
  $ fakeroot debian/rules binary

假设所有必需的依赖项都可用且编译成功，新包将出现在该目录的父目录中。
