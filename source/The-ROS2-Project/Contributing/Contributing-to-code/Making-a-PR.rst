创建 pull request（PR）——操作指南
=================================

Pull request 用于向 ROS 项目贡献代码和文档更改。
本文解释如何从你对 ROS 仓库的 fork 准备并创建 pull request。
有了这些信息，你将能够在 pull request 中提交聚焦的更改，准备好接受审查。

**领域：贡献、社区 | 内容类型：how-to | 经验：初级、中级、高级**

.. contents:: 目录
   :depth: 2
   :local:

概要
----

`Pull requests (PRs) <https://docs.github.com/en/pull-requests>`__ 是将你的更改合并到 ROS 仓库的提案。
创建 pull request 让你能够与其他 ROS 贡献者协作，在 ROS 维护者合并之前提供一个讨论和审查你代码更改的空间。
欢迎对 `任何 ROS 仓库 <https://github.com/ros2>`__ 提交 pull request。

关于贡献礼仪的更多信息，请参阅 :doc:`Contributing </The-ROS2-Project/Contributing>`。

先决条件
--------

#. 为你的代码更改 `创建 fork <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo>`__ 目标 ROS 仓库。
#. 在你 fork 的 `目标 ROS 仓库 <https://github.com/ros2>`__ 中，在从 **rolling** 分支派生的开发分支上完成你的代码更改。
#. 确保你的更改符合 ROS 指南。

   * 如果你的 pull request 是代码更改：

     * 确保你已遵循 :doc:`开发者指南 </The-ROS2-Project/Contributing/Developer-Guide>` 中的指导。
     * 检查你的代码符合 :doc:`代码风格指南 </The-ROS2-Project/Contributing/Code-Style-Language-Versions>` 的相关部分。
     * 确保你已 :ref:`运行测试 <colcon-run-the-tests>`，并对你的代码更改运行了适当的 linter。

   * 如果你的 pull request 是文档更改：

     * 确保你已遵循 :doc:`/The-ROS2-Project/Contributing/Contributing-To-ROS-2-Documentation` 中的指导。

步骤
----

1 准备 pull request
^^^^^^^^^^^^^^^^^^^

使用以下指南准备你的 pull request：

* **范围和聚焦**
   * 将每个 pull request 限制为单一、定义清晰的更改。
   * 将不相关的更改作为单独的 pull request 提交。
   * 保持补丁小，避免不必要或偶然的更改。
* **提交历史与 squash**
   * 将更改 squash 为最少量的清晰、语义化提交，以保留可读的项目历史。
   * 在 pull request 处于审查期间不要 squash 提交，因为审查者可能不会注意到更改，从而造成混淆。
   * 你可以在 pull request 处于审查期间创建新提交。
* **草稿 pull request**
   * 使用草稿 pull request 在工作进行中请求早期反馈。
   * 不要期望草稿 pull request 在你标记为就绪之前被正式审查或合并。
   * 如果你希望某个人对草稿 pull request 提供早期反馈，请在 pull request 描述或评论中提及他们（使用 ``@``）。
* **提及与引用**
   * 如果你的更改基于某个设计文档（例如 `REP <https://reps.openrobotics.org/>`__），请在 pull request 描述中提及其他参与设计的人，例如审查过该 REP 的人。
   * 如果你的 pull request 依赖另一个 pull request，请在 pull request 描述中清楚引用该依赖。
     确保使用 ``#`` 符号提及 pull request ID。
   * 如果你的更改计划与某个特定版本的 ROS 一起发布，请在 pull request 描述中包含该 ROS 版本。
* **记录你的代码更改**
   * 如果你的 pull request 是代码更改，尽量在同一个 pull request 中进行相关的文档更新（包括 API 文档、功能文档和发布说明）。

2 提交 pull request
^^^^^^^^^^^^^^^^^^^

#. 从你 fork 中包含更改的分支，向目标 ROS 仓库的 **rolling** 分支创建 pull request。
   你可以使用 GitHub CLI、GitHub Desktop 或 GitHub 网页界面创建 pull request。

   关于从 fork 创建 pull request 的更多信息，请参阅 `GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork>`__。

   关于各种可用的 pull request 方法的更多信息，请参阅 `GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`__。

#. 通过完成描述模板中显示的各部分来填写 pull request，包括：

   * **描述**：总结你的代码更改，按 ID 链接到相关 GitHub issue 和 PR，突出任何关键点或关注领域。
   * **Issue**：以 ``Fixes #(issue)`` 格式包含你的更改所修复的 GitHub issue 的 ID。
     这确保在 pull request 被合并时，该 issue 会自动关闭。
   * **生成式 AI**：如果这个 pull request 是使用生成式 AI 生成的，请指定模型和版本（例如 GitHub Copilot v3.2）。
   * **其他信息**：提供你认为对理解你的更改有用的任何上下文或细节。

#. 选中 `Allow edits by maintainers <https://github.blog/news-insights/product-news/improving-collaboration-with-forks/>`__ 复选框，以帮助 ROS 维护者在需要时直接进行小的更改。

提交 pull request 后，ROS 社区中的其他开发者和贡献者将审查你的更改，包括对照相关指南进行检查。

3 回复审查评论
^^^^^^^^^^^^^^

当其他开发者或贡献者向你的 pull request 添加审查评论或建议时，你会收到来自 GitHub 的通知。

你可以直接在 GitHub 中查看和讨论审查评论（`需要帮助请参阅 GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/viewing-a-pull-request-review>`__），并在需要时向你的分支添加更多提交来处理它们。
你也可以直接接受 pull request 中任何建议的更改，这会自动向你的分支添加一个新提交（`如何接受建议的更改请参阅 GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/incorporating-feedback-in-your-pull-request>`__）。

根据这些反馈讨论和迭代你的更改，根据需要修改和更新你的开发分支并添加新提交。
争取在一周内回复审查评论，这样你和审查者就不会丢失更改的上下文。

4 合并 pull request
^^^^^^^^^^^^^^^^^^^

在你处理完任何反馈后，你的 pull request 必须先获得目标 ROS 仓库 :doc:`Committer </The-ROS2-Project/Governance>` 的批准，然后才能合并。

当 Committer 批准你的 pull request 时，他们会将它合并到目标分支（通常是 **rolling**），你会收到来自 GitHub 的通知。

你的更改也可能会被回移到 ROS 的较旧发行版。

相关内容
--------

* :ref:`ROS 开发一般原则 <general-principles>`
* :doc:`Reviewing-a-PR`
