创建拉取请求（PR）——操作指南
============================

拉取请求用于向 ROS 项目贡献代码和文档更改。
本文介绍如何从你 fork 的 ROS 仓库准备并创建一个拉取请求。
掌握这些信息后，你将能够通过拉取请求提交聚焦的更改，以便接受审查。

**领域：贡献、社区 | 内容类型：操作指南 | 经验：初级、中级、专家**

.. contents:: 目录
   :depth: 2
   :local:

概述
----

`拉取请求（PR） <https://docs.github.com/en/pull-requests>`__ 是把你的更改合并到 ROS 仓库的提案。
创建拉取请求使你能够与其他 ROS 贡献者协作，在 ROS 维护者合并你的代码更改之前，提供一个讨论和审查这些更改的空间。
欢迎向 `任何 ROS 仓库 <https://github.com/ros2>`__ 提交拉取请求。

关于贡献礼仪的更多信息，请参见 :doc:`贡献 </The-ROS2-Project/Contributing>`。

前提条件
--------

#. 为目标 ROS 仓库 `创建一个 fork <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo>`__，用于放置你的代码更改。
#. 在 `目标 ROS 仓库 <https://github.com/ros2>`__ 的 fork 中，从 **rolling** 分支切出一个开发分支并完成你的代码更改。
#. 确保你的更改符合 ROS 指南。

   * 如果你的拉取请求是代码更改：

     * 确保你遵循了 :doc:`开发者指南 </The-ROS2-Project/Contributing/Developer-Guide>` 中的指导。
     * 检查你的代码是否符合 :doc:`代码风格指南 </The-ROS2-Project/Contributing/Code-Style-Language-Versions>` 中相关章节的要求。
     * 确保你针对代码更改 :ref:`运行了测试 <colcon-run-the-tests>` 和相应的 linter。

   * 如果你的拉取请求是文档更改：

     * 确保你遵循了 :doc:`/The-ROS2-Project/Contributing/Contributing-To-ROS-2-Documentation` 中的指导。

步骤
----

1 准备拉取请求
^^^^^^^^^^^^^^

使用以下指南来准备你的拉取请求：

* **范围与聚焦**
   * 每个拉取请求只处理一项定义明确的更改。
   * 把不相关的更改作为单独的拉取请求提交。
   * 保持补丁小巧，避免不必要或附带性的更改。
* **提交历史与压缩**
   * 将更改压缩为数量最少、清晰且语义明确的提交，以保持项目历史可读。
   * 拉取请求处于审查过程中时不要压缩提交，因为审查者可能注意不到这些更改，从而导致困惑。
   * 在拉取请求接受审查期间，你可以创建新的提交。
* **草稿拉取请求**
   * 在工作进行中时，可以使用草稿拉取请求来征求早期反馈。
   * 在你将草稿拉取请求标记为就绪之前，不要期望它会得到正式审查或被合并。
   * 如果你想就某个草稿拉取请求获得特定人员的早期反馈，请在拉取请求描述或评论中用 ``@`` 提及他们。
* **提及与引用**
   * 如果你的更改基于设计文档（例如 `REP <https://reps.openrobotics.org/>`__），请在拉取请求描述中提及参与该设计的其他人员，例如审阅过该 REP 的人。
   * 如果你的拉取请求依赖另一个拉取请求，请在拉取请求描述中清楚地引用该依赖项。
     务必使用 ``#`` 记号提及拉取请求 ID。
   * 如果你的更改计划随某个特定的 ROS 版本发布，请在拉取请求描述中包含该 ROS 版本。
* **记录你的代码更改**
   * 如果你的拉取请求是代码更改，请尽量在同一个拉取请求中完成相关的文档更新（包括 API 文档、功能文档和发行说明）。

2 提交拉取请求
^^^^^^^^^^^^^^

#. 从你 fork 中包含更改的分支向目标 ROS 仓库的 **rolling** 分支创建一个拉取请求。
   你可以使用 GitHub CLI、GitHub Desktop 或 GitHub 网页界面创建拉取请求。

   关于如何从 fork 创建拉取请求的更多信息，请参见 `GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork>`__。

   关于各种可用拉取请求创建方式的更多信息，请参见 `GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`__。

#. 通过填写描述模板中显示的各节来完善拉取请求，其中包括：

   * **Description（描述）**：概述你的代码更改，按 ID 链接相关的 GitHub issue 和 PR，并突出任何关键点或需要关注的地方。
   * **Issue**：以 ``Fixes #(issue)`` 的格式包含你的更改所修复的 GitHub issue ID。
     这可以确保该 issue 在拉取请求被合并时自动关闭。
   * **Generative AI（生成式 AI）**：如果该拉取请求是使用生成式 AI 生成的，请说明模型和版本（例如 GitHub Copilot v3.2）。
   * **Additional information（附加信息）**：提供任何你认为有助于理解你更改的上下文或细节。

#. 勾选 `允许维护者编辑 <https://github.blog/news-insights/product-news/improving-collaboration-with-forks/>`__ 复选框，以便在需要时帮助 ROS 维护者直接做出小的修改。

提交拉取请求后，ROS 社区中的其他开发者和贡献者会审查你的更改，包括对照相关指南进行检查。

3 回应审查意见
^^^^^^^^^^^^^^

当其他开发者或贡献者对你的拉取请求添加审查意见或建议时，你会收到来自 GitHub 的通知。

你可以直接在 GitHub 中查看和讨论审查意见（如需帮助请参见 `GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/viewing-a-pull-request-review>`__），并在需要时向你的分支添加更多提交来处理它们。
你也可以直接在拉取请求中接受任何建议的更改，这会自动向你的分支添加一个新的提交（关于如何接受建议的更改，请参见 `GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/incorporating-feedback-in-your-pull-request>`__）。

根据这些反馈讨论并迭代你的更改，按需用新的提交修改和更新你的开发分支。
尽量在一周内回复审查意见，以免你和审查者失去对更改的上下文。

4 合并拉取请求
^^^^^^^^^^^^^^

在你处理完所有反馈后，你的拉取请求必须得到 :doc:`目标 ROS 仓库的 Committer </The-ROS2-Project/Governance>` 的批准才能被合并。

当 Committer 批准你的拉取请求后，他们会把它合并到目标分支（通常是 **rolling**），你会收到来自 GitHub 的通知。

你的更改也可能被回溯移植（backport）到更早的 ROS 发行版。

相关内容
--------

* :ref:`ROS 开发通用原则 <general-principles>`
* :doc:`Reviewing-a-PR`
