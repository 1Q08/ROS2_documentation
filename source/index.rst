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


**机器人操作系统（ROS）是一组用于构建机器人应用的软件库和工具。**
从驱动程序和最先进的算法到强大的开发者工具，ROS 拥有您下一个机器人项目所需的各种开源工具。

:ref:`进一步了解 ROS <AboutROS>`

自 2007 年 ROS 诞生以来，机器人领域和 ROS 社区都发生了很大变化。
ROS 2 项目的目标就是适应这些变化，发扬 ROS 1 的优点，改进其不足之处。

**您在寻找某个特定 ROS 包（如 MoveIt、image_proc 或 octomap）的文档吗？**
请参阅 `ROS 索引 <https://index.ros.org/?search_packages=true#{DISTRO}>`__ 或查看 `各包文档索引 <https://docs.ros.org/en/{DISTRO}/p/>`__。

本站包含 ROS 2 的文档。
如果您在寻找 ROS 1 文档，请查看 `ROS wiki <https://wiki.ros.org>`__。

如果您在研究中使用了 ROS 2，请参阅 :doc:`引用文献 <Citations>` 来引用 ROS 2。

入门
----

* :doc:`安装 <Installation>`

  - 首次设置 ROS 2 的说明

* :doc:`教程 <Tutorials>`

  - 新用户最佳的起点！
  - 动手示例项目，帮助您循序渐进地掌握必备技能

* :doc:`操作指南 <How-To-Guides>`

  - 无需通读 :doc:`教程 <Tutorials>`，即可快速获得“我该怎么做……？”这类问题的答案

* :doc:`核心概念 <Concepts>`

  - 对 :doc:`教程 <Tutorials>` 中涉及的核心 ROS 2 概念的高层次讲解

* :doc:`联系 <Contact>`

  - 解答您的问题，或发起讨论的论坛


ROS 2 项目
----------

如果您对 ROS 2 项目的进展感兴趣：

* :doc:`参与贡献 <The-ROS2-Project/Contributing>`

  - 向 ROS 2 贡献代码、文档和其他改进的最佳实践与方法，以及将现有 ROS 1 文档迁移到 ROS 2 的说明

* :doc:`发行版 <Releases>`

  - ROS 2 的过去、现在和将来的发行版

* :doc:`功能状态 <The-ROS2-Project/Features>`

  - 当前发行版中的功能

* :doc:`功能想法 <The-ROS2-Project/Feature-Ideas>`

  - 尚未积极开发的锦上添花的功能想法

* :doc:`路线图 <The-ROS2-Project/Roadmap>`

  - ROS 2 开发计划中的工作

* :doc:`ROSCon 演讲 <The-ROS2-Project/ROSCon-Content>`

  - 社区关于 ROS 2 的演讲

* :doc:`项目治理 <The-ROS2-Project/Governance>`

  - 关于 ROS 技术指导委员会、工作组和即将举办的活动信息

* :doc:`营销 <The-ROS2-Project/Marketing>`

  - 可下载的营销材料
  - `关于 ROS 商标的信息 <https://www.ros.org/blog/media/>`__

* :doc:`采用者 <The-ROS2-Project/Adopters>`

  - 使用 ROS 的组织和项目

ROS 社区资源
------------

如果您需要帮助、有想法，或希望为项目做贡献，请访问我们的 ROS 社区资源。

* `ROS 官方 Zulip 频道：讨论与支持 <https://openrobotics.zulipchat.com/>`__ (ROS 1, ROS 2)

* `Robotics Stack Exchange —— 社区问答网站 <https://robotics.stackexchange.com/>`__ (ROS 1, ROS 2)

  - 更多信息请参阅 :ref:`联系页面 <Using Robotics Stack Exchange>`

* `Open Robotics Discourse <https://discourse.openrobotics.org/>`__ (ROS 1, ROS 2)

  - ROS 社区一般性讨论和公告的论坛
  - 更多信息请参阅 :ref:`联系页面 <Using ROS Discourse>`

* `ROS 索引 <https://index.ros.org/>`__ (ROS 1, ROS 2)

  - 所有包的索引列表（即 ROS 包的 `Python 包索引（PyPI） <https://pypi.org/>`_\ ）
  - 查看某个包支持哪些 ROS 发行版
  - 链接到包的仓库、API 文档或网站
  - 查看包的许可证、构建类型、维护者、状态和依赖
  - 在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上获取包的更多信息

* `ROS 资源状态页面 <https://status.openrobotics.org/>`__ (ROS 1, ROS 2)

  - 查看 Discourse 或 ROS 构建农场等 ROS 资源的当前状态。

* `ROS 基础设施项目页面 <https://infrastructure.openrobotics.org/>`__ (ROS 1, ROS 2)

  - ROS 基础设施项目维护 `ROS 构建农场 <https://build.ros2.org/>`__，它构建 `ROS 索引 <https://index.ros.org/>`__ 上可获取的二进制包。
  - ROS 基础设施项目还开发和维护通常与 ROS 相关的工具，如 `Bloom <https://bloom.readthedocs.io/>`__ 和 `Colcon <https://colcon.readthedocs.io/en/released/>`__。

ROS 项目通用资源
----------------

* `Robotics Enhancement Proposals (REPs) <https://reps.openrobotics.org/>`__ (ROS 1, ROS 2)

  - 关于新设计和约定的提案

* `ROS Robots <https://robots.ros.org/>`__ (ROS 1, ROS 2)

  - 展示社区的机器人项目
  - 关于如何贡献机器人的说明

* `ROS Wiki <https://wiki.ros.org/>`__ (ROS 1)

  - ROS 1 文档和用户可修改的内容
  - 至少会持续维护到最后一个 ROS 1 发行版停止支持（EOL）

* `ROS.org <https://www.ros.org/>`__ (ROS 1, ROS 2)

  - ROS 1 和 ROS 2 产品的着陆页，包含 ROS 的高层次介绍以及指向其他 ROS 站点的链接

活动
----

* `ROS 官方 Vimeo 频道 <https://vimeo.com/osrfoundation>`__ (ROS 1, ROS 2)

  - ROSCon 演讲、社区与工作组会议以及项目演示的视频。

* `ROSCon 网站 <https://roscon.ros.org/>`__ (ROS 1, ROS 2)

  - ROSCon 是我们一年一度的 ROS 开发者大会。
  - 该页面还列出了 ROSConJP、ROSConFr 等区域性 ROS 活动。

* `开源机器人基金会官方活动日历 <https://calendar.google.com/calendar/u/0/embed?src=agf3kajirket8khktupm9go748@group.calendar.google.com&ctz=America/Los_Angeles>`__

  - 该日历用于 OSRF 官方活动和工作组会议。

* `开源机器人基金会社区日历 <https://calendar.google.com/calendar/embed?src=c_3fc5c4d6ece9d80d49f136c1dcd54d7f44e1acefdbe87228c92ff268e85e2ea0%40group.calendar.google.com&ctz=America%2FLos_Angeles>`__

  - 该日历用于非官方的 ROS 社区活动。
  - `在此提交您的活动 <https://bit.ly/OSRFCalendarForm>`__。

其他
----
* `购买 ROS 官方周边 <https://spring.ros.org/>`__

* ROS 社交媒体

  - Twitter 上的 `@OpenRoboticsOrg <https://twitter.com/OpenRoboticsOrg>`__ 和 `@ROSOrg <https://twitter.com/ROSOrg>`__
  - `LinkedIn 上的 Open Robotics <https://www.linkedin.com/company/open-source-robotics-foundation>`__

* 访问 `开源机器人基金会网站 <https://www.openrobotics.org/>`__

  - 向开源机器人基金会的可抵税慈善捐款可通过 `DonorBox <https://donorbox.org/support-open-robotics?utm_medium=qrcode&utm_source=qrcode>`__ 进行。

已弃用
------
* `ROS Answers <https://answers.ros.org/questions/>`__ (ROS 1, ROS 2)

  - ROS Answers 曾是 ROS 社区的问答网站，直到 2023 年 8 月。
  - ROS Answers 目前作为只读资源提供。

* `ROS 2 Docs <https://docs.ros2.org>`_

  - 截至 Galactic（含）的 API 文档

* `ROS 2 Design <http://design.ros2.org/>`__

  - ROS 2 开发背后的早期设计决策
  - 新的设计提案应通过 `机器人增强提案（REPs） <https://reps.openrobotics.org/>`__ 提交
