术语表
======

.. include:: ../global_substitutions.txt

本文档中使用的术语表：

.. glossary::

   API
       应用程序编程接口（Application Programming Interface）是由某个"应用程序"提供的接口，这里的"应用程序"通常是一个共享库或其他语言相应的共享资源。
       API 由若干文件组成，这些文件在使用该接口的软件与提供该接口的软件之间定义了契约。
       这些文件在 C 和 C++ 中通常表现为头文件，在 Python 中则表现为 Python 文件。
       无论是哪种情况，重要的是 API 应当分组并在文档中加以说明，并且应声明为公开（public）或私有（private）。
       公开接口受变更规则约束，公开接口的变更会促使提供该接口的软件发布新的版本号。

   client_library
       客户端库（client library）是一种 :term:`API`，它使用话题（Topics）、服务（Services）和动作（Actions）等基础中间件概念来提供对 ROS 图的访问。

   package
       一个独立的软件单元，包括源代码、构建系统文件、文档、测试以及其他相关资源。

   REP
       机器人增强提案（Robotics Enhancement Proposal）。
       一种描述 ROS 社区的增强、标准化或约定的文档。
       相关的 REP 批准流程允许社区对提案进行反复迭代，直到达成某种共识；届时提案可以被正式批准并实施，随后成为文档。
       所有 REP 都可以在 `REP 索引 <https://reps.openrobotics.org/>`_ 中查看。

   VCS
       版本控制系统（Version Control System），例如 CVS、SVN、git、mercurial 等。

   rclcpp
       面向 ROS 的 C++ 专属 :term:`客户端库 <client_library>`。
       这包括任何与中间件相关的 API，以及基于消息（Messages）、服务（Services）和动作（Actions）等接口定义生成 C++ 数据结构的相关消息生成。

   repository
       通常使用 :term:`VCS` （如 git 或 mercurial）进行管理、并通常托管在 GitHub 或 BitBucket 等站点上的软件包集合。
       在本文档的语境中，仓库通常包含一种或多种类型的 |packages|。
