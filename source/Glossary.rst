术语表
======

.. include:: ../global_substitutions.txt

本说明文档中使用的术语表：

.. glossary::

   API
       API（应用程序编程接口）是由“应用程序”提供的接口，在本例中通常是共享库或其他语言相应的共享资源。
       API 由若干文件组成，这些文件定义了使用接口的软件与提供接口的软件之间的契约。
       在 C 和 C++ 中，这些文件通常表现为头文件；在 Python 中则表现为 Python 文件。
       无论哪种情况，重要的是 API 应在文档中分组并加以描述，并且应声明为公开或私有。
       公开接口受变更规则约束，公开接口的变更会促使提供这些接口的软件更新版本号。

   client_library
       客户端库是一种 :term:`API`，它使用话题、服务和动作等基础中间件概念提供对 ROS 图的访问。

   package
       一个单一的软件单元，包括源代码、构建系统文件、文档、测试以及其他相关资源。

   REP
        机器人增强提案（Robotics Enhancement Proposal）。
        一份为 ROS 社区描述某项增强、标准化或约定的文档。
        相关的 REP 批准流程允许社区对提案反复迭代，直到达成某种共识，届时该提案可被批准并实施，随后成为文档。
        所有 REP 都可以从 `REP 索引 <https://reps.openrobotics.org/>`_ 查看。

   VCS
       版本控制系统，例如 CVS、SVN、git、mercurial 等……

   rclcpp
       ROS 的 C++ 专用 :term:`客户端库 <client_library>`。
       这包括任何与中间件相关的 API，以及基于消息、服务和动作等接口定义生成相关 C++ 数据结构的机制。

   repository
       通常使用 git 或 mercurial 等 :term:`VCS` 管理的一组包，通常托管在 GitHub 或 BitBucket 之类的站点上。
       在本文档的语境中，仓库通常包含一个或多个某种类型的 |packages|。
