.. redirect-from::

  Contributing

.. _Contributing:

Contributing
============

.. contents:: 目录
   :depth: 1
   :local:

在你开始为 ROS 2 项目做贡献之前，有几件事需要牢记。

基本原则
--------

* 尊重前人的成果

  ROS 已经存在十多年，全世界的开发者都在使用它。
  在贡献时保持谦逊的态度和开放的心态。

* 尽早与 Open Robotics 互动

  * Open Robotics 充当 ROS 社区的守门人和倡导者。
    在 **设计阶段** 就依赖他们的专业知识和 **技术判断**。
  * 尽早与 Open Robotics 和社区展开讨论。
    长期的 ROS 贡献者可能对全局有更清晰的视野。
    如果你实现了一个功能并在未先与社区讨论的情况下就提交拉取请求，你可能面临被拒绝的风险，或者被要求大幅重新设计。
  * 在开始实现之前，先通过提交 issue 或在 Discourse 上交流想法通常是更好的做法。

* 尽可能采用社区最佳实践，而不是临时的流程

  在开发和贡献时，要站在最终用户的角度考虑他们的体验。
  避免使用可能无法被所有人访问的非标准工具或库。

* 从社区整体出发思考

  考虑全局。
  有开发者在使用不同的机器人，面临着不同的约束。
  ROS 需要满足整个社区的需求。

你可以通过多种方式为 ROS 2 项目做贡献。

讨论与支持
----------

为 ROS 2 做贡献最简单的方式之一就是参与社区讨论和支持。
你可以在 :doc:`联系 <../../Contact>` 页面上找到更多关于如何参与的信息。

贡献代码
--------

搭建你的开发环境
^^^^^^^^^^^^^^^^

要开始，你需要从源码安装；请按照适用于你平台的 :ref:`源码安装说明 <building-from-source>` 进行操作。

开发指南
^^^^^^^^

.. toctree::
   :titlesonly:
   :maxdepth: 1

   Contributing/Developer-Guide
   Contributing/Code-Style-Language-Versions
   Contributing/Quality-Guide
   Contributing/Build-Farms
   Contributing/Windows-Tips-and-Tricks
   Contributing/Contributing-to-code
   Contributing/Contributing-To-ROS-2-Documentation

可以开展哪些工作
^^^^^^^^^^^^^^^^

我们已经确定了一些可以由社区成员开展的任务：可以通过 `在 ROS 2 仓库中搜索标记为 "help wanted" 的 issue <https://github.com/search?q=user%3Aament+user%3Aros2+is%3Aopen+label%3A"help+wanted"&type=Issues>`__ 来列出它们。
如果你在该列表中看到想要开展的工作，请在该条目下评论，让其他人知道你已经着手处理。

我们还有一个标签，用于标记我们认为对首次贡献者更友好的 issue，即 `标记为 "good first issue" 的 issue <https://github.com/search?q=user%3Aament+user%3Aros2+is%3Aopen+label%3A%22good+first+issue%22&type=Issues>`__。
如果你有兴趣为 ROS 2 项目做贡献，我们鼓励你先看看这些 issue。
如果你想扩大范围，我们欢迎你对任何开放的 issue（或你提出的其他 issue）做出贡献，尤其是带有里程碑（表示它们是为下一个 ROS 2 发行版而设的）的任务（里程碑将是下一个发行版的名称，例如 'crystal'）。

如果你有修复 bug 或改进文档的代码要贡献，请将其以拉取请求的形式提交到相关的仓库。
对于较大的改动，最好在开始工作之前先在 `ROS 2 论坛 <https://discourse.openrobotics.org/c/ros/111>`__ 上讨论该提案，这样可以确认是否已有其他人在做类似的工作。
如果你的提案涉及 API 的改动，尤其建议在开始工作之前先讨论方案。

成为核心维护者
^^^^^^^^^^^^^^

ROS 2 维护者确保项目总体上有序推进。
维护者的职责包括：

* 审查传入的代码贡献，检查其风格、质量以及与仓库/ROS 2 总体目标的契合度。
* 确保 CI 保持绿灯。
* 合并满足上述质量和 CI 标准的拉取请求。
* 处理用户提交的 issue。

`ros2 <https://github.com/ros2>`__ 和 `ament <https://github.com/ament>`__ 组织中的每个仓库都有一组独立的维护者。
成为其中某个或多个仓库的维护者是一个仅限邀请的流程，通常包括以下步骤：

* 在过去一年内，对仓库有大量代码贡献。
* 在过去一年内，对传入仓库的拉取请求做了大量审查。

大约每 3 个月，ROS 2 团队会审查所有仓库中的贡献，并向新的维护者发出邀请。
邀请被接受后，新维护者将被要求完成一个关于 ROS 2 仓库机制和策略的简短培训流程。
培训流程完成后，新维护者将获得对相应仓库的写权限。
