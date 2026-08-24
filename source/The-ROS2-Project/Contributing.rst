.. redirect-from::

  Contributing

.. _Contributing:

贡献
====

.. contents:: 目录
   :depth: 1
   :local:

在开始为 ROS 2 项目做贡献之前，需要记住以下几点。

宗旨
----

* 尊重前人的成果

  ROS 已经存在了十多年，被世界各地的开发者使用。
  在贡献时保持谦逊的态度和开放的心态。

* 尽早让 Open Robotics 参与

  * Open Robotics 充当 ROS 社区的守门人和倡导者。
    从设计阶段就依赖他们的专业知识和技术判断。
  * 尽早与 Open Robotics 和社区开始讨论。
    长期 ROS 贡献者可能对大局有更清晰的愿景。
    如果你在不先与社区讨论的情况下实现功能并发送拉取请求，你将冒着被拒绝的风险，或者可能被要求大幅重新思考你的设计。
  * 在开始实现之前，通常最好通过提交 issue 或使用 Discourse 来推广一个想法。

* 尽可能采用社区最佳实践，而不是临时的流程

  在开发和贡献时，考虑最终用户的体验。
  避免使用可能并非人人都能使用的非标准工具或库。

* 把社区作为一个整体来考虑

  考虑大局。
  有开发者用不同的约束构建不同的机器人。
  ROS 需要满足整个社区的需求。

你可以通过多种方式为 ROS 2 项目做贡献。

讨论和支持
----------

为 ROS 2 做贡献的一些最简单方式包括参与社区讨论和支持。
你可以在 :doc:`Contact <../../Contact>` 页面上找到更多关于如何参与的信息。

贡献代码
--------

设置你的开发环境
^^^^^^^^^^^^^^^^

要开始，你需要从源码安装；请针对你的平台遵循 :ref:`源码安装说明 <building-from-source>`。

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

做什么工作
^^^^^^^^^^

我们已经确定了一些社区成员可以完成的任务：可以通过 `在 ROS 2 仓库中搜索标记为“help wanted”的 issue <https://github.com/search?q=user%3Aament+user%3Aros2+is%3Aopen+label%3A"help+wanted"&type=Issues>`__ 列出它们。
如果你在列表中看到你想做的内容，请在该条目上评论，让别人知道你在关注它。

我们还有一个我们认为应该更适合首次贡献者的 issue 标签，`标记为“good first issue” <https://github.com/search?q=user%3Aament+user%3Aros2+is%3Aopen+label%3A%22good+first+issue%22&type=Issues>`__。
如果你有兴趣为 ROS 2 项目做贡献，我们鼓励你先看看那些 issue。
如果你想撒更广的网，我们欢迎对任何开放 issue（或你可能提出的其他 issue）做贡献，特别是那些带有里程碑、表示它们以下一个 ROS 2 版本为目标的里程碑任务（里程碑将是下一个版本的名称，例如 'crystal'）。

如果你有一些修复 bug 或改进文档的代码要贡献，请将其作为拉取请求提交到相关仓库。
对于较大的更改，最好在开始工作之前 `在 ROS 2 论坛上 <https://discourse.openrobotics.org/c/ros/111>`__ 讨论该提案，以便你能确定是否已经有其他人在做类似的工作。
如果你的提案涉及 API 更改，特别建议在开始工作之前先讨论方案。

成为核心维护者
^^^^^^^^^^^^^^

ROS 2 维护者确保项目总体上不断取得进展。
维护者的职责包括：

* 审查传入的代码贡献的风格、质量，以及它们与仓库 / ROS 2 目标的整体契合度。
* 确保 CI 持续保持绿色。
* 合并符合上述质量和 CI 标准的拉取请求。
* 处理用户提出的 issue。

`ros2 <https://github.com/ros2>`__ 和 `ament <https://github.com/ament>`__ 组织中的每个仓库都有一组独立的维护者。
成为其中一个或多个仓库的维护者是一个仅限邀请的过程，通常包括以下步骤：

* 在过去一年内，对该仓库有大量代码贡献。
* 在过去一年内，对该仓库传入的拉取请求进行大量审查。

大约每 3 个月，ROS 2 团队将审查所有仓库中的贡献，并向新维护者发出邀请。
一旦邀请被接受，新维护者将被要求参加一个关于 ROS 2 仓库机制和政策的简短培训流程。
培训流程完成后，新维护者将获得对相应仓库的写权限。
