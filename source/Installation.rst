.. _InstallationGuide:
.. _RollingInstall:

安装
====

安装 ROS 2 {DISTRO_TITLE_FULL} 的选项：

.. toctree::
   :hidden:
   :glob:

   Installation/Ubuntu-Install-Debs
   Installation/Windows-Install-Binary
   Installation/RHEL-Install-RPMs
   Installation/Alternatives
   Installation/Maintaining-a-Source-Checkout
   Installation/Testing
   Installation/RMW-Implementations
   Installation/ROS-2-Mirrors

.. _binary-package-platforms:

二进制包
--------

二进制包仅为 `REP-2000 <https://reps.openrobotics.org/rep-2000/#rolling-ridley-june-2020---ongoing>`__ 中列出的 Tier 1 操作系统构建。
如果你使用的不是以下任何操作系统，则可能需要从源代码构建，或使用 :doc:`容器解决方案 <How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers>` 在你的平台上运行 ROS 2。

我们为以下平台提供 ROS 2 二进制包：

* Ubuntu Linux（amd64 / aarch64）- Noble Numbat（24.04）

  * :doc:`deb 包 <Installation/Ubuntu-Install-Debs>` （推荐）
  * :doc:`二进制归档 <Installation/Alternatives/Ubuntu-Install-Binary>`

* Red Hat Enterprise Linux 9（amd64）

  * :doc:`RPM 包 <Installation/RHEL-Install-RPMs>` （推荐）
  * :doc:`二进制归档 <Installation/Alternatives/RHEL-Install-Binary>`

* Windows 10（amd64）

  * :doc:`Windows 二进制包（VS 2019） <Installation/Windows-Install-Binary>`

.. _building-from-source:

从源代码构建
------------

我们支持在以下平台上从源代码构建 ROS 2：

* :doc:`Ubuntu Linux 24.04 <Installation/Alternatives/Ubuntu-Development-Setup>`
* :doc:`Windows 10 <Installation/Alternatives/Windows-Development-Setup>`
* :doc:`RHEL-9/Fedora <Installation/Alternatives/RHEL-Development-Setup>`
* :doc:`macOS <Installation/Alternatives/macOS-Development-Setup>`

应选择哪种安装方式？
--------------------

无论是从二进制包安装还是从源代码构建，最终都能得到一个功能完整、可正常使用的 ROS 2 安装。
各选项之间的差异取决于你打算用 ROS 2 做什么。

**二进制包** 适用于一般用途，提供已构建好的 ROS 2 安装。
对于想要立即上手、直接使用现成 ROS 2 的人来说，这是理想选择。

Linux 用户安装二进制包有两种选择：

- 软件包（deb 或 RPM，取决于平台）
- 二进制归档

从软件包安装是推荐的方法，因为它会自动安装必要的依赖项，并随常规系统更新一起更新。
但是，安装 deb 包需要 root 权限。
如果你没有 root 权限，二进制归档是次优选择。

选择从二进制包安装的 Windows 用户只有二进制归档这一种选项
（deb 包仅适用于 Ubuntu/Debian）。

**从源代码构建** 面向希望修改或显式省略 ROS 2 基础部分内容的开发者。
对于不支持二进制包的平台，也推荐使用这种方式。
从源代码构建还能让你选择安装绝对最新版本的 ROS 2。

要为 ROS 2 核心做贡献？
^^^^^^^^^^^^^^^^^^^^^^^

如果你计划直接为 ROS 2 核心软件包做贡献，可以安装 :doc:`最新的开发版源码 <Installation/Alternatives/Latest-Development-Setup>`，其安装说明与 :ref:`Rolling 发行版 <rolling_distribution>` 相同。
