====
镜像
====

.. contents:: 目录
   :depth: 3

文档镜像
--------

ROS 文档的镜像在 `主站 <http://docs.ros.org>`_ 不可用时充当备份，并且可以为地理位置更接近镜像的用户提供更快的访问速度。

Debian/Ubuntu（APT）仓库镜像
----------------------------

要使用这些镜像，请在你的 APT 配置中将官方的 ROS 仓库 URL 替换为下面列出的镜像 URL。

亚洲
^^^^

.. list-table::
   :widths: 30 20 50

   * - 清华大学（TUNA）
     - 中国
     - `https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu/ <https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu/>`_
   * - 中国科学技术大学（USTC）
     - 中国
     - `https://mirrors.ustc.edu.cn/ros2/ubuntu/ <https://mirrors.ustc.edu.cn/ros2/ubuntu/>`_
   * - 阿里云（Aliyun）
     - 中国
     - `https://mirrors.aliyun.com/ros2/ubuntu/ <https://mirrors.aliyun.com/ros2/ubuntu/>`_
   * - 齐鲁工业大学（QLU）
     - 中国
     - `https://mirrors.qlu.edu.cn/ros2/ubuntu/ <https://mirrors.qlu.edu.cn/ros2/ubuntu/>`_
   * - 重庆大学（CQU）
     - 中国
     - `https://mirrors.cqu.edu.cn/ros2/ubuntu/ <https://mirrors.cqu.edu.cn/ros2/ubuntu/>`_

欧洲
^^^^

.. list-table::
   :widths: 30 20 50

   * - 代尔夫特理工大学
     - 荷兰
     - `http://ftp.tudelft.nl/ros2/ubuntu/ <http://ftp.tudelft.nl/ros2/ubuntu/>`_

北美洲
^^^^^^

.. list-table::
   :widths: 30 20 50

   * - 马里兰大学（UMD）
     - 美国
     - `http://mirror.umd.edu/packages.ros.org/ros2/ubuntu/ <http://mirror.umd.edu/packages.ros.org/ros2/ubuntu/>`_
   * - nulled LLC
     - 美国
     - `http://mirror.nulled.llc/ros2/ubuntu/ <http://mirror.nulled.llc/ros2/ubuntu/>`_

大洋洲
^^^^^^

.. list-table::
   :widths: 30 20 50

   * - AARNet
     - 澳大利亚
     - `https://mirror.aarnet.edu.au/pub/ros2-packages/ubuntu/ <https://mirror.aarnet.edu.au/pub/ros2-packages/ubuntu/>`_

南美洲与非洲
^^^^^^^^^^^^

这些地区目前没有官方验证过的 ROS 2 镜像。
如果你在南美洲或非洲托管镜像并希望在此处列出，请参阅下面的 **托管镜像** 一节。

创建镜像
--------

如果你正在维护镜像，请加入 discourse.openrobotics.org 上的 Mirrors 类别：`https://discourse.openrobotics.org/c/infrastructure-project/infra-mirrors/ <https://discourse.openrobotics.org/c/infrastructure-project/infra-mirrors/>`_ ，以便获取反馈和及时更新。

使用镜像
^^^^^^^^

要使用镜像，请在 ``ros2-latest.list`` 文件中将 ``packages.ros.org`` 替换为镜像 URL：

.. code-block:: bash

   # Example for TUNA mirror
   sudo sed -i 's|http://packages.ros.org/ros2/ubuntu|https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu|g' /etc/apt/sources.list.d/ros2-latest.list
   sudo apt update

搭建镜像
--------

ROS 基础设施使用 ``rsync`` 分发软件包。
要创建 ROS 2 仓库的本地镜像：

1. **存储需求：** 确保你至少有 500GB 可用磁盘空间。
2. **同步命令：** 使用 ``rsync`` 从官方 OSUOSL 端点拉取：

.. code-block:: bash

   # Sync the main ROS 2 repository
   rsync -azv rsync.osuosl.org::ros2-main /your/local/path --delete

3. **维护：** 设置一个 ``cron`` 任务，每 6-12 小时同步一次。

将你的镜像加入此列表
^^^^^^^^^^^^^^^^^^^^

要获得官方收录，你的镜像必须满足以下要求：

* 支持 **HTTPS**。
* 至少每 24 小时同步一次。
* 提供一个用于基础设施告警的联系邮箱。

验证通过后，请针对本页面提交 Pull Request，或在 `Mirrors Discourse <https://discourse.openrobotics.org/c/infrastructure-project/infra-mirrors/>`_ 中发帖。

镜像 docs.ros.org
-----------------

镜像文档站点需要特定配置，以防止搜索引擎索引碎片化。
如果你有兴趣托管文档的区域镜像，请先通过 Discourse **联系基础设施团队**，然后再继续。
