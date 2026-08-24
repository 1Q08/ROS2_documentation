.. redirect-from::

  Docs-Guide

ROS 2 文档
==========

.. toctree::
   :titlesonly:
   :maxdepth: 1
   :hidden:

   About-ROS
   Installation
   Releases
   Tutorials
   How-To-Guides
   Concepts
   Contact
   The-ROS2-Project
   Package-Docs
   Related-Projects
   Glossary
   Citations


**机器人操作系统（ROS）是一套用于构建机器人应用的软件库和工具。**
从驱动程序、前沿算法到强大的开发者工具，ROS 为你下一个机器人项目提供了所需的开源工具。

:ref:`进一步了解 ROS <AboutROS>`

自 2007 年 ROS 问世以来，机器人领域和 ROS 社区都发生了许多变化。
ROS 2 项目的目标是适应这些变化，继承 ROS 1 的优点，并改进其不足。

**你是在寻找某个特定 ROS 软件包（如 MoveIt、image_proc 或 octomap）的文档吗？**
请查看 `ROS Index <https://index.ros.org/?search_packages=true#{DISTRO}>`__，或浏览 `这个逐包文档索引 <https://docs.ros.org/en/{DISTRO}/p/>`__。

本站包含 ROS 2 的文档。
如果你在寻找 ROS 1 的文档，请查看 `ROS wiki <https://wiki.ros.org>`__。

如果你在工作中使用了 ROS 2，请参阅 :doc:`引用 <Citations>` 来引用 ROS 2。

开始上手
--------

* :doc:`安装 <Installation>`

  - 首次设置 ROS 2 的说明

* :doc:`教程 <Tutorials>`

  - 新用户的最佳起点！
  - 动手实践示例项目，帮助你循序渐进地掌握必要技能

* :doc:`How-To-Guides`

  - 快速解答你的"我该如何……？"
    问题，而无需通读 :doc:`教程 <Tutorials>`

* :doc:`概念 <Concepts>`

  - 对 :doc:`教程 <Tutorials>` 中涉及的 ROS 2 核心概念的高层次讲解

* :doc:`联系我们 <Contact>`

  - 解答你的问题，或提供一个发起讨论的论坛


ROS 2 项目
----------

如果你关注 ROS 2 项目的发展：

* :doc:`贡献 <The-ROS2-Project/Contributing>`

  - 为 ROS 2 贡献代码、文档和其他改进的最佳实践与方法，以及将现有 ROS 1 文档迁移到 ROS 2 的说明

* :doc:`发行版 <Releases>`

  - 过去、现在和未来的 ROS 2 发行版

* :doc:`功能状态 <The-ROS2-Project/Features>`

  - 当前版本中的功能

* :doc:`功能构想 <The-ROS2-Project/Feature-Ideas>`

  - 一些锦上添花但尚未积极开发的功能构想

* :doc:`路线图 <The-ROS2-Project/Roadmap>`

  - ROS 2 开发计划中的工作

* :doc:`ROSCon 演讲 <The-ROS2-Project/ROSCon-Content>`

  - 社区关于 ROS 2 的演讲

* :doc:`项目治理 <The-ROS2-Project/Governance>`

  - 关于 ROS 技术指导委员会、工作组和即将举办的活动信息

* :doc:`宣传材料 <The-ROS2-Project/Marketing>`

  - 可下载的宣传材料
  - `关于 ROS 商标的信息 <https://www.ros.org/blog/media/>`__

* :doc:`采用者 <The-ROS2-Project/Adopters>`

  - 使用 ROS 的组织和项目

ROS 社区资源
------------

如果你需要帮助、有想法，或想为项目做贡献，请访问我们的 ROS 社区资源。

* `官方 ROS Zulip 频道（讨论与支持） <https://openrobotics.zulipchat.com/>`__ （ROS 1、ROS 2）

* `Robotics Stack Exchange - 社区问答网站 <https://robotics.stackexchange.com/>`__ （ROS 1、ROS 2）

  - 更多信息请参见 :ref:`联系我们页面 <Using Robotics Stack Exchange>`

* `Open Robotics Discourse <https://discourse.openrobotics.org/>`__ （ROS 1、ROS 2）

  - 面向 ROS 社区的一般性讨论和公告论坛
  - 更多信息请参见 :ref:`联系我们页面 <Using ROS Discourse>`

* `ROS Index <https://index.ros.org/>`__ （ROS 1、ROS 2）

  - 所有软件包的索引列表（相当于 ROS 软件包的 `Python Package Index (PyPI) <https://pypi.org/>`_）
  - 查看某个软件包支持哪些 ROS 发行版
  - 链接到软件包的仓库、API 文档或网站
  - 查看软件包的许可证、构建类型、维护者、状态和依赖项
  - 在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上获取软件包的更多信息

* `ROS 资源状态页面 <https://status.openrobotics.org/>`__ （ROS 1、ROS 2）

  - 查看 Discourse 或 ROS 构建农场等 ROS 资源的当前状态。

* `ROS 基础设施项目页面 <https://infrastructure.openrobotics.org/>`__ （ROS 1、ROS 2）

  - ROS 基础设施项目维护着 `ROS 构建农场 <https://build.ros2.org/>`__，它构建了 `ROS Index <https://index.ros.org/>`__ 上提供的二进制包。
  - ROS 基础设施项目还开发并维护通常与 ROS 相关联的工具，如 `Bloom <https://bloom.readthedocs.io/>`__ 和 `Colcon <https://colcon.readthedocs.io/en/released/>`__。

ROS 通用项目资源
----------------

* `Robotics Enhancement Proposals (REPs) <https://reps.openrobotics.org/>`__ （ROS 1、ROS 2）

  - 针对新设计和约定的提案

* `ROS Robots <https://robots.ros.org/>`__ （ROS 1、ROS 2）

  - 展示来自社区的机器人项目
  - 关于如何贡献机器人的说明

* `ROS Wiki <https://wiki.ros.org/>`__ （ROS 1）

  - ROS 1 文档和用户可修改的内容
  - 至少在最后一个 ROS 1 发行版到达 EOL 之前保持活跃

* `ROS.org <https://www.ros.org/>`__ （ROS 1、ROS 2）

  - ROS 1 和 ROS 2 的产品落地页，提供 ROS 的高层次介绍以及指向其他 ROS 站点的链接

活动
----

* `官方 ROS Vimeo 频道 <https://vimeo.com/osrfoundation>`__ （ROS 1、ROS 2）

  - ROSCon 演讲、社区和工作组会议以及项目演示的视频。

* `ROSCon 网站 <https://roscon.ros.org/>`__ （ROS 1、ROS 2）

  - ROSCon 是我们一年一度的 ROS 开发者大会。
  - 该页面还列出了 ROSConJP 和 ROSConFr 等地区性 ROS 活动。

* `Open Source Robotics Foundation 官方活动日历 <https://calendar.google.com/calendar/u/0/embed?src=agf3kajirket8khktupm9go748@group.calendar.google.com&ctz=America/Los_Angeles>`__

  - 此日历用于 OSRF 官方活动和工作组会议。

* `Open Source Robotics Foundation 社区日历 <https://calendar.google.com/calendar/embed?src=c_3fc5c4d6ece9d80d49f136c1dcd54d7f44e1acefdbe87228c92ff268e85e2ea0%40group.calendar.google.com&ctz=America%2FLos_Angeles>`__

  - 此日历用于非官方的 ROS 社区活动。
  - `在此提交你的活动 <https://bit.ly/OSRFCalendarForm>`__。

其他资源
--------

* `购买官方 ROS 周边 <https://spring.ros.org/>`__

* ROS 在社交媒体上

  - Twitter 上的 `@OpenRoboticsOrg <https://twitter.com/OpenRoboticsOrg>`__ 和 `@ROSOrg <https://twitter.com/ROSOrg>`__
  - `Open Robotics 在 LinkedIn <https://www.linkedin.com/company/open-source-robotics-foundation>`__

* 访问 `Open Source Robotics Foundation 网站 <https://www.openrobotics.org/>`__

  - 向 Open Source Robotics Foundation 提供的可抵税慈善捐款可通过 `DonorBox <https://donorbox.org/support-open-robotics?utm_medium=qrcode&utm_source=qrcode>`__ 进行。

已废弃
------
* `ROS 2 Design <http://design.ros2.org/>`__

  - ROS 2 开发早期的设计决策
  - 新的设计提案应通过 `Robotics Enhancement Proposals (REPs) <https://reps.openrobotics.org/>`__ 提交
