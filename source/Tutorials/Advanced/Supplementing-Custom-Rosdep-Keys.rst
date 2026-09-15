补充自定义 rosdep 键
====================

.. contents:: 目录
    :depth: 2
    :local:

概述与动机
----------

如 :doc:`../Intermediate/Rosdep` 中所述，``rosdep`` 会在 ``package.xml`` 文件中查找 rosdep 键，并将它们映射到为所用 ROS 发行版和操作系统需要安装的软件包。
任何人都可以通过 `向 rosdistro 贡献 <https://github.com/ros/rosdistro/blob/master/CONTRIBUTING.md#rosdep-rules-contributions>`_ 来请求添加新的 rosdep 键。
当你有一些希望通过 ``rosdep`` 安装的依赖项（例如 ``apt`` 或 ``pip`` 软件包）时，这是首选的做法。

然而，在很多情况下，直接贡献你的键可能会很困难。
例如，如果该依赖项：

1. 在目标发行版的默认 APT（或 pip）仓库中不可用
2. 是专有库
3. 是只对你或你的组织有用的某些小众库
4. 是你 :doc:`自行构建并打包 <../../How-To-Guides/Building-a-Custom-Deb-Package>` 但不想与更广泛的 ROS 社区分享的 ROS 软件包

虽然可以选择 :doc:`完全分叉 rosdistro <../../How-To-Guides/Using-Custom-Rosdistro>` ，但如果你只想照常继续使用官方 ROS 发行版，只是在其之上额外定义一些 rosdep 键，那么这样做可能有些小题大做。
本教程将说明如何实现这一点。

不过需要提醒的是，请不要不加区分地使用这一方法。
它可能由于二进制不兼容而引发难以调试的问题，这些问题可能表现为静默失败、无法解释的崩溃或数据损坏。
如果你在启用了此功能的系统上向他人寻求帮助，请务必说明所有被添加或覆盖的内容。

预备知识：``rosdep`` 如何获取 rosdep 键
---------------------------------------

为了更好地理解我们将要做的事情，我们先来探讨一下 ``rosdep`` 工作原理的一些相关细节。

与 ``apt`` 等其他使用源列表来维护本地索引的工具类似，``rosdep`` 也不例外。
这些源存储在 ``/etc/ros/rosdep/sources.list.d`` 中。
这与 apt 将软件仓库存储在 ``/etc/apt/sources.list.d`` 中的方式类似。

默认情况下（作为首次设置 ``rosdep init`` 的一部分），你只有一个源文件：``/etc/ros/rosdep/sources.list.d/20-default.list``。
查看其内容，你会看到类似下面这样的条目：

.. code-block:: console

   $ cat /etc/ros/rosdep/sources.list.d/20-default.list
   ...
   yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/base.yaml
   yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/python.yaml
   ...

这些条目决定了调用 ``rosdep update`` 时 ``rosdep`` 从何处获取 rosdep 键及其映射（rosdep **规则**）。
调用时会从所有源文件中所有已声明的条目里编译相关内容，形成一个本地缓存的索引。
在安装或查找（“解析”）rosdep 键时就会使用这个本地索引。

例如，第一个条目（``base.yaml``）定义了 ``libopencv-dev`` 键（请参见 `这里 <https://github.com/ros/rosdistro/blob/72f24d6/rosdep/base.yaml#L5240-L5252>`_），这正是 ``rosdep`` 能够解析它的原因：

.. code-block:: console

   $ rosdep where-defined libopencv-dev
   https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/base.yaml
   $ rosdep resolve libopencv-dev
   #apt
   libopencv-dev

总而言之，它使 ``rosdep`` 能够将 ``libopencv-dev`` 键解析为同名的 ``apt`` 软件包。

请注意，从上面的输出可以看出，该命令是在 Ubuntu 或 Debian 操作系统上运行的。
在 RHEL 上，该键则会解析为 DNF 软件包 ``opencv-devel``：

.. code-block:: console

   $ rosdep resolve libopencv-dev --os=rhel:9
   #dnf
   opencv-devel

使用自定义源文件扩展 ``rosdep``
-------------------------------

希望上述内容已经清楚地说明，要让 ``rosdep`` 认识新的键需要做什么：添加一个新的自定义源文件！

作为一个简单示例，我们来添加一个新的源文件，让 ``rosdep`` 从保存在本机上的 YAML 文件中获取键。
打开你最喜欢的文本编辑器，并将以下内容写入 ``/etc/ros/rosdep/sources.list.d/30-custom.list`` （需要以 root 权限启动编辑器，例如通过 ``sudo``）：

.. code-block:: yaml

  yaml file:///etc/ros/rosdep/custom_rules.yaml

现在将以下内容写入 ``/etc/ros/rosdep/custom_rules.yaml`` 中：

.. code-block:: yaml

  awesome_library:
    ubuntu: [awesome_library]
  that_other_library:
    ubuntu:
      pip:
        packages: [another_library]

这定义了两条新的 rosdep 规则：

1. 键 ``awesome_library``，仅为 Ubuntu 定义，映射到同名的 ``apt`` 软件包
2. 键 ``that_other_library``，仅为 Ubuntu 定义，映射到名为 ``another_library`` 的 ``pip`` 软件包

运行 ``rosdep update`` 后，``rosdep`` 会发现新的 ``30-custom.list``，从而扫描 ``custom_rules.yaml`` 文件的内容。
现在 ``rosdep`` 已经配置好，可以识别这些新键以及它们应当映射到哪里：

.. code-block:: console

   $ rosdep resolve awesome_library
   #apt
   awesome_library
   $ rosdep resolve that_other_library
   #pip
   another_library

现在你只需将 ``<depend>awesome_library</depend>`` 添加到你的 ROS 软件包的 ``package.xml`` 中，``rosdep`` 就知道如何安装该依赖项了！

结束语
------

上面的简单示例只是暗示了自定义 rosdep 键所能实现的功能。

- **你的依赖项是托管在第三方 PPA 中的 APT 软件包吗？**
  这不是问题。
  由于 ``rosdep`` 所做的只是把键转换为 ``apt install`` 调用，APT 安装该软件包不会有什么问题（前提是你已添加了该 PPA）。
- **你的依赖项是托管在第三方索引中的 pip 软件包吗？**
  将该索引添加到你的 ``pip.conf`` 中，就可以顺利使用了。
- **源文件不必指向本机上的文件。**
  同时支持 ``file://`` 和 ``https://`` 语法（在 Linux 上，绝对路径以 ``/`` 开头，因此会出现像 ``file:///etc/rosdep/my.file`` 这样的三重斜杠）。
- **源按字母顺序加载。**
  如果你在 30 前缀中添加了冲突的规则，该规则不会被使用。
  如果你创建了前缀为 10 的源文件，它会覆盖默认列表（前缀 20）中的软件包。
  如果你使用的是从二进制仓库安装的软件包，强烈建议不要覆盖依赖声明，因为这很可能导致极难调试的二进制不兼容问题。
- **无法合并键。**
  例如，无法仅向已有的 rosdep 键添加 ``fedora`` 安装规则。
  视加载顺序而定，这样的规则要么被忽略，要么会完全覆盖整个 rosdep 键，移除所有其他安装器。

延伸阅读
--------

- https://docs.ros.org/en/independent/api/rosdep/html/rosdep_yaml_format.html
- https://docs.ros.org/en/independent/api/rosdep/html/contributing_rules.html
