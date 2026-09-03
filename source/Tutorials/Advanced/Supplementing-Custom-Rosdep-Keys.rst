补充自定义 rosdep key
=====================

.. contents:: 目录
    :depth: 2
    :local:

概述与动机
----------

如 :doc:`../Intermediate/Rosdep` 中所解释的，``rosdep`` 会在 ``package.xml`` 文件中查找 rosdep key，并将它们映射到要为当前 ROS 发行版和操作系统安装的软件包。
任何人都可以通过 `向 rosdistro 贡献 <https://github.com/ros/rosdistro/blob/master/CONTRIBUTING.md#rosdep-rules-contributions>`_ 请求添加新的 rosdep key。
当你有一些依赖（例如一个 ``apt`` 或 ``pip`` 包）希望能够通过 ``rosdep`` 安装时，这是首选的做法。

但是，在很多情况下，直接贡献你的 key 可能会很困难。
例如，如果该依赖：

1. 在目标发行版的默认 APT（或 pip）仓库中不可用
2. 是一个专有库
3. 是一些只对你或你的组织有用的小众库
4. 是你 :doc:`自己构建并打包 <../../How-To-Guides/Building-a-Custom-Deb-Package>` 的 ROS 包，但不想与更广泛的 ROS 社区分享

虽然可以选择 :doc:`整体 fork rosdistro <../../How-To-Guides/Using-Custom-Rosdistro>`，但如果你只是想照常使用官方 ROS 发行版，仅在其之上额外定义一些 rosdep key，那么 fork 可能就有些小题大做了。
本教程解释了如何实现这一点。

不过需要提醒一句，请不要滥用这种方法。
它可能会导致极难调试的问题，因为二进制不兼容可能表现为静默失败、无法解释的崩溃或数据损坏。
而且，如果你在一个启用了此功能的系统上向任何人求助，请务必解释清楚所有被添加或覆盖的内容。

预备知识：``rosdep`` 如何获取 rosdep key
----------------------------------------

为了更好地理解我们即将做的事情，让我们先探索一些关于 ``rosdep`` 工作方式的相关细节。

``rosdep`` 类似于 ``apt`` 等其他工具，它们都使用源列表来维护本地索引。
这些源存储在 ``/etc/ros/rosdep/sources.list.d`` 中。
这与 apt 将仓库存储在 ``/etc/apt/sources.list.d`` 的方式类似。

默认情况下（作为首次设置 ``rosdep init`` 的一部分），你只有一个源文件：``/etc/ros/rosdep/sources.list.d/20-default.list``。
检查其内容，你会看到如下条目：

.. code-block:: console

   $ cat /etc/ros/rosdep/sources.list.d/20-default.list
   ...
   yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/base.yaml
   yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/python.yaml
   ...

这些条目决定了在调用 ``rosdep update`` 时，``rosdep`` 从哪里获取 rosdep key 及其映射（rosdep **规则**）。
调用时，``rosdep`` 会将所有源文件中所有已声明条目的相关内容编译成一个本地缓存索引。
之后，在安装或查找（“解析”）rosdep key 时就会使用这个本地索引。

例如，第一个条目（``base.yaml``）定义了 ``libopencv-dev`` key（参见 `此处 <https://github.com/ros/rosdistro/blob/72f24d6/rosdep/base.yaml#L5240-L5252>`_），正是这一点让 ``rosdep`` 能够解析它：

.. code-block:: console

   $ rosdep where-defined libopencv-dev
   https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/base.yaml
   $ rosdep resolve libopencv-dev
   #apt
   libopencv-dev

总之，它使 ``rosdep`` 能够将 ``libopencv-dev`` key 解析为同名的 ``apt`` 包。

请注意，从上面的输出可以推断，该命令是在 Ubuntu 或 Debian 操作系统上运行的。
在 RHEL 上，该 key 会解析为 DNF 包 ``opencv-devel``：

.. code-block:: console

   $ rosdep resolve libopencv-dev --os=rhel:9
   #dnf
   opencv-devel

使用自定义源文件扩展 ``rosdep``
-------------------------------

希望上述内容已清楚地说明，要让 ``rosdep`` 理解新的 key 需要做什么：添加一个新的自定义源文件！

作为一个简单示例，让我们添加一个新的源文件，告诉 ``rosdep`` 从存储在本地机器上的一个 YAML 文件获取 key。
打开你最喜欢的文本编辑器，将以下内容写入 ``/etc/ros/rosdep/sources.list.d/30-custom.list``\ （编辑器需要以 root 权限启动，例如通过 ``sudo``）：

.. code-block:: yaml

  yaml file:///etc/ros/rosdep/custom_rules.yaml

现在将以下内容写入 ``/etc/ros/rosdep/custom_rules.yaml``：

.. code-block:: yaml

  awesome_library:
    ubuntu: [awesome_library]
  that_other_library:
    ubuntu:
      pip:
        packages: [another_library]

这定义了两条新的 rosdep 规则：

1. key ``awesome_library``，仅针对 Ubuntu 定义，映射到同名的 ``apt`` 包
2. key ``that_other_library``，仅针对 Ubuntu 定义，映射到名为 ``another_library`` 的 ``pip`` 包

运行 ``rosdep update`` 后，``rosdep`` 会检测到新的 ``30-custom.list``，促使它扫描 ``custom_rules.yaml`` 文件的内容。
现在 ``rosdep`` 已设置好，可以识别这些新 key 以及它们应映射到什么：

.. code-block:: console

   $ rosdep resolve awesome_library
   #apt
   awesome_library
   $ rosdep resolve that_other_library
   #pip
   another_library

现在你所要做的就是在 ROS 包的 ``package.xml`` 中添加 ``<depend>awesome_library</depend>``，``rosdep`` 就会知道如何安装该依赖！

结束语
------

上面的简单示例只是示意了自定义 rosdep key 的可能性。

- **你的依赖是托管在第三方 PPA 中的 APT 包吗？**
  没有问题。
  由于 ``rosdep`` 所做的只是将 key 转换为 ``apt install`` 调用，APT 安装该包不会有任何问题（前提是你已添加了该 PPA）。
- **你的依赖是托管在第三方索引中的 pip 包吗？**
  将该索引添加到你的 ``pip.conf`` 中，就可以使用了。
- **源文件不必指向本地机器上的文件。**
  同时支持 ``file://`` 和 ``https://`` 语法（在 Linux 上，绝对路径以 ``/`` 开头，因此会形成三个斜杠，如 ``file:///etc/rosdep/my.file``）。
- **源按字母顺序加载。**
  如果你在 30 前缀中添加了一条冲突的规则，它将不会被使用。
  如果你创建了一个 10 前缀的源文件，它将覆盖默认列表（前缀 20）中的包。
  如果你使用的是从二进制仓库安装的包，强烈建议不要覆盖依赖声明，因为这很可能导致极难调试的二进制不兼容问题。
- **无法合并 key。**
  无法例如只向现有的 rosdep key 添加一条 ``fedora`` 安装规则。
  根据加载顺序，这样的规则要么被忽略，要么会完全覆盖整个 rosdep key，移除所有其他安装器。

延伸阅读
--------

- https://docs.ros.org/en/independent/api/rosdep/html/rosdep_yaml_format.html
- https://docs.ros.org/en/independent/api/rosdep/html/contributing_rules.html
