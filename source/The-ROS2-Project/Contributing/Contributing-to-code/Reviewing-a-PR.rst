审查拉取请求（PR）——操作指南
============================

所有提交到 ROS 项目的代码和文档都必须在拉取请求中接受审查。
本文介绍如何准备并审查贡献者提交的拉取请求。
阅读本文后，你将能够确保拉取请求中的更改符合所要求的标准。

**领域：贡献、社区 | 内容类型：操作指南 | 经验：初级、中级、专家**

.. contents:: 目录
   :depth: 2
   :local:

概述
----

审查贡献者提交的拉取请求（PR）让你能够检查他们的更改是否符合相应的指南和标准。
欢迎任何人审查和批准拉取请求。
更改在被批准后即可合并。
只有目标仓库的 :doc:`Committer </The-ROS2-Project/Governance>` 才能把拉取请求合并到该仓库，而且在获得批准之前他们不会这样做。

前提条件
--------

代码或文档贡献者已经 :doc:`创建了拉取请求 </The-ROS2-Project/Contributing/Contributing-to-code/Making-a-PR>`，希望把他们的更改合并到 `某个 ROS 仓库 <https://github.com/ros2>`__。

步骤
----

1 准备审查
^^^^^^^^^^

* 欢迎任何人审查拉取请求。

  拉取请求通常需要两次审查才能被合并。

* 请把审查拉取请求视为一项由提交者和其他开发者共同参与的协作活动，而不是被动或单向的过程。
* 作为审查者：

  * 你可以就地做小改进，例如修正拼写错误或处理细小的风格问题。
  * 你应尽力在提交后一周内对拉取请求发表评论。

* 当你开始审查某个拉取请求时，请留下一条评论，让其他人知道你正在审查。

2 审查拉取请求
^^^^^^^^^^^^^^

#. 按照以下指南审查拉取请求：

   * 确认代码或文档更改对该仓库是合适的。
   * 验证代码正确且完整，并且范围限定为一项定义明确的更改。
   * 检查拉取请求是否以默认分支（通常是 ``rolling``）为目标。
   * 如果这些更改基于设计文档（例如 `REP <https://reps.openrobotics.org/>`__），请核实更改与该设计一致。
   * 对于代码更改，确保这些更改：

     * 遵循 :doc:`开发者指南 <../Developer-Guide>`。
     * 遵循 :doc:`代码风格指南 <../Code-Style-Language-Versions>`。
     * 为新功能或缺陷修复包含测试。

   * 对于文档更改，确保这些更改遵循 :doc:`文档指南 </The-ROS2-Project/Contributing/Contributing-To-ROS-2-Documentation>`。
   * 确认该拉取请求的持续集成（CI）运行能干净地通过。

#. 给出你的审查意见。

   你可以向提交者添加针对该拉取请求的审查意见，或直接在拉取请求中提出修改建议（`关于具体做法请参见 GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request>`__）。

#. 遵循以下指南，确保你的审查意见有用且可执行：

   * 先给出高层次的意见（例如，要求重构或更改设计），然后再给出关于具体细节的较低层次意见。
   * 考虑提供以下几类意见：

     * **正面反馈**——例如：

       ``这里的边界情况处理得很好——提前返回让逻辑清晰多了。``

     * **提问**——例如：

       ``只是想确认我没有漏掉某个需求，我们这里为什么使用自定义排序函数而不是 localeCompare？``

     * **建议**——例如：

       ``你可以用 Array.map 简化这个循环，让它更简洁：``

       .. code-block:: javascript

         const names = users.map(user => user.name)

     * **问题**——例如：

       ``这个函数没有处理 response 为 null 的情况，这可能导致运行时错误——请添加一个保护条件：``

       .. code-block:: javascript

         if (!response) {
           return [...];
         }

     * **日常整理**——与拉取请求主要目的无关、但有助于保持仓库健康的更改，例如：

       ``既然这个文件本来就要更新，能否顺便把顶部未使用的 formatDate 导入也删掉？``

     * **细节**——吹毛求疵的小细节，例如改进风格或可读性，例如：

       ``一个小的命名建议；user_list 可以改名为 users，以更好地体现它是一个集合。``

   * 清楚地说明你期望每条意见对应产生什么结果，包括该意见是否会阻止拉取请求合并，以及你认为该请求是可选的还是必需的。
   * 记得包含正面反馈，并对提交者所做的工作表示感谢，始终保持建设性。

3 批准并合并拉取请求
^^^^^^^^^^^^^^^^^^^^

在你审查完拉取请求并给出反馈后，提交者可以继续讨论或迭代他们的更改，向该 PR 添加新的提交。

当你对更改感到满意、它们已可合并时，请批准该拉取请求（`关于具体做法请参见 GitHub 文档 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews>`__）。

* 欢迎任何人审查拉取请求，即使它已经有了一次审查。
* 一个拉取请求必须至少有开发者（作者以外）的一次批准，在大多数情况下需要两次批准，才能被合并到目标分支。
* 只有目标仓库的 Committer 才能合并已批准的拉取请求。

  * 关于具有目标仓库合并权限的人员名单，请参见 :doc:`当前的 ROS Committer </The-ROS2-Project/Governance>`。

* 如果该拉取请求存在任何依赖项，请确保相关的依赖拉取请求按正确顺序合并。

相关内容
--------

* :ref:`ROS 开发通用原则 <general-principles>`
* :doc:`Making-a-PR`
* `关于拉取请求审查 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews>`__
