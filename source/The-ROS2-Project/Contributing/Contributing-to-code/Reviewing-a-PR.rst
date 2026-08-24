审查 pull request（PR）——操作指南
=================================

所有传入 ROS 项目的代码和文档都必须在 pull request 中接受审查。
本文解释如何准备和审查贡献者提交的 pull request。
阅读本文后，你将能够确保 pull request 中的更改符合要求的标准。

**领域：贡献、社区 | 内容类型：how-to | 经验：初级、中级、高级**

.. contents:: 目录
   :depth: 2
   :local:

概要
----

审查贡献者的 pull request (PR) 让你能够检查他们的更改是否符合相应的指南和标准。
欢迎任何人审查和批准 pull request。
更改在被批准后即可合并。
只有目标仓库的 :doc:`Committer </The-ROS2-Project/Governance>` 才能将 pull request 合并到该仓库，而且在它被批准之前他们不会这样做。

先决条件
--------

代码或文档贡献者已 :doc:`创建 pull request </The-ROS2-Project/Contributing/Contributing-to-code/Making-a-PR>`，将其更改合并到 `某个 ROS 仓库 <https://github.com/ros2>`__。

步骤
----

1 准备审查
^^^^^^^^^^

* 欢迎任何人审查 pull request。

  一个 pull request 通常需要两次审查才能合并。

* 将审查 pull request 视为涉及提交者和其他开发者的协作活动，而不是被动或单向的过程。
* 作为审查者：

  * 你可以就地小幅改进代码或文档，例如修复拼写错误或处理小的风格问题。
  * 你应该尽最大努力在提交后一周内对 pull request 发表评论。

* 当你开始审查 pull request 时，留下评论让别人知道你在进行审查。

2 审查 pull request
^^^^^^^^^^^^^^^^^^^

#. 根据以下指南审查 pull request：

   * 确认代码或文档更改适合该仓库。
   * 验证代码正确且完整，并限定为单一、定义清晰的更改。
   * 检查 pull request 以默认分支（通常是 ``rolling``）为目标。
   * 如果更改基于设计文档（例如 `REP <https://reps.openrobotics.org/>`__），验证更改与设计一致。
   * 对于代码更改，确保更改：

     * 遵循 :doc:`开发者指南 <../Developer-Guide>`。
     * 遵循 :doc:`代码风格指南 <../Code-Style-Language-Versions>`。
     * 为新功能或 bug 修复包含测试。

   * 对于文档更改，确保更改遵循 :doc:`文档指导 </The-ROS2-Project/Contributing/Contributing-To-ROS-2-Documentation>`。
   * 确认该 pull request 的持续集成 (CI) 运行干净通过。

#. 提供你的审查评论。

   你可以向 pull request 为提交者添加审查评论，或直接在 pull request 中建议更改（`需要指导请参阅 GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request>`__）。

#. 遵循以下指南，确保你的审查评论有用且可执行：

   * 从高层评论开始（例如请求重构或设计更改），然后转向关于具体细节的底层评论。
   * 考虑提供以下类型的评论：

     * **正面反馈** — 例如：

       ``在这里处理边界情况做得很好——提前返回让逻辑更容易理解。``

     * **问题** — 例如：

       ``为了确认我没有遗漏某个需求，这里使用自定义排序函数而不是 localeCompare 有原因吗？``

     * **建议** — 例如：

       ``你可以使用 Array.map 简化这个循环，让它更简洁：``

       .. code-block:: javascript

         const names = users.map(user => user.name)

     * **问题** — 例如：

       ``这个函数没有处理 response 为 null 的情况，这可能会导致运行时错误——添加一个保护子句：``

       .. code-block:: javascript

         if (!response) {
           return [...];
         }

     * **清理性更改** — 与 pull request 主要目的无关、但有助于保持仓库健康的更改，例如：

       ``既然这个文件已经在更新，我们能否也移除顶部的未使用 formatDate 导入？``

     * **小细节** — 小的、吹毛求疵的细节，例如改进风格或可读性，例如：

       ``命名的小建议；user_list 可以命名为 users，以更好地反映它是一个集合。``

   * 清楚说明你期望每个评论的响应是什么，包括该评论是否会阻塞 pull request 的合并，以及你认为你的请求是可选的还是必需的。
   * 记得包含对提交者所做工作的正面反馈和感谢，并始终保持建设性。

3 批准和合并 pull request
^^^^^^^^^^^^^^^^^^^^^^^^^

在你审查了 pull request 并提供反馈后，提交者可以继续讨论或迭代他们的更改，向 PR 添加新提交。

当你对更改满意且它们准备好合并时，批准该 pull request（`需要指导请参阅 GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews>`__）。

* 欢迎任何人审查 pull request，即使它已经有审查。
* 一个 pull request 在被合并到目标分支之前，必须至少有一个批准，在大多数情况下需要来自开发者（作者以外）的两个批准。
* 只有目标仓库的 Committer 才能合并已批准的 pull request。

  * 请参阅 :doc:`当前 ROS Committers </The-ROS2-Project/Governance>` 获取对目标仓库有合并权限的人员名单。

* 如果 pull request 有任何依赖，请确保依赖的 pull request 按正确顺序合并。

相关内容
--------

* :ref:`ROS 开发一般原则 <general-principles>`
* :doc:`Making-a-PR`
* `关于 pull request 审查 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews>`__
