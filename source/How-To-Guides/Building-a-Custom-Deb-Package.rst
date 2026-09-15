.. redirect-from::

  Guides/Building-a-Custom-Debian-Package
  How-To-Guides/Building-a-Custom-Debian-Package

构建自定义 deb 软件包
=====================

许多 Ubuntu 用户通过安装 :doc:`deb 软件包 <../Installation/Ubuntu-Install-Debs>` 在其系统上安装 ROS 2。
本指南给出一组简短说明，用于构建本地的自定义 deb 软件包。

.. contents:: 目录
   :local:

前提条件
--------

要成功构建自定义软件包，待构建软件包的所有依赖项都必须在本地或 rosdep 中可用。
此外，该软件包的所有依赖项都应在软件包的 ``package.xml`` 文件中正确声明。

安装依赖项
----------

运行以下命令来安装构建所需的工具：

.. code:: console

  $ sudo apt install python3-bloom python3-rosdep fakeroot debhelper dh-python

初始化 rosdep
-------------

通过调用以下命令来初始化 rosdep 数据库：

.. code:: console

  $ sudo rosdep init
  $ rosdep update

请注意，如果过去已经初始化过 ``rosdep init`` 命令可能会失败；这可以安全地忽略。

从软件包构建 deb
----------------

运行以下命令来构建 deb：

.. code:: console

  $ cd /path/to/pkg_source  # this should be the directory that contains the package.xml
  $ bloom-generate rosdebian
  $ fakeroot debian/rules binary

假设所有必需的依赖项都可用且编译成功，新软件包将出现在此目录的父目录中。
