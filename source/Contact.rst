.. _Help:

联系
====

.. _Using Robotics Stack Exchange:

支持
----

不同类型的问题或讨论对应不同的沟通渠道；
请查阅下面的说明，确保您选择了正确的方式。

需要帮助排查系统问题？
首先，在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上搜索，看看是否其他人也遇到过类似问题，以及他们的解决方案对您是否有效。

如果没有，请在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上提出新问题。
务必添加标签，至少包括 ``ros2`` 标签和您所使用的发行版版本，例如 ``{DISTRO}``。
如果您的问题与这里的文档有关，请添加类似 ``docs`` 的标签，或更具体地添加 ``tutorials``。

请不要直接联系开发者/维护者。
社区无法看到未公开提出或回答的问题或答案。
当整个社区都参与讨论并帮助回答问题的时候，开源开发的效果最好。
最好把所有问题都发送到 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__，并将所有问题报告到问题追踪器。

贡献支持
^^^^^^^^

ROS 2 用户来自各种不同的技术背景，使用各种不同的操作系统，并且不一定具有任何 ROS（1 或 2）经验。
因此，无论经验多少，用户参与贡献支持都很重要。

如果您在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上看到与您自己遇到过的问题类似的问题，请考虑提供一些对您的情况有帮助的线索。
不要担心您不确定自己的回答是否正确。
只需说明这一点，其他社区成员会在必要时参与进来。

问题
----

如果您发现了 bug、有改进建议，或有针对某个特定包的问题，您可以在 GitHub 上提交 issue。

例如，如果您正在阅读 :doc:`这里的教程 <Tutorials>`，并遇到某条在您的系统上无法工作的说明，
您可以在 `ros2_documentation <https://github.com/ros2/ros2_documentation>`__ 仓库中提交 issue。

您可以在 `ROS 2 的 GitHub <https://github.com/ros2>`__ 上搜索各个 ROS 2 仓库。

在提交 issue 之前，请先在 ros2 和 ament 这两个 GitHub 组织中搜索，检查是否已有其他用户报告过类似问题：`搜索查询示例 <https://github.com/search?q=user%3Aros2+user%3Aament+turtlesim&type=Issues>`__。

接下来，请查看 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__，看看是否有人已经提出过您的问题或报告过您的 issue。

如果尚未被报告，欢迎您在相应仓库的追踪器中提交 issue。
如果不清楚某个特定问题该使用哪个追踪器，请将其提交到 `ros2/ros2 仓库 <https://github.com/ros2/ros2/issues>`__，我们会查看它。

提交 issue 时，请务必：

* 包含足够的信息，以便他人理解该问题。

准确描述您当时在做什么或正试图做什么，以及具体出了什么错（如果有的话）。
如果是按照教程或在线说明操作，请提供指向具体说明的链接。

* 使用描述性的标题或主题行。
  差：“rviz 不工作”。
  好：“Rviz crashing looking for missing ``.so`` after latest apt update”
* 包含与问题相关的确切平台、软件、版本和环境信息。
  这包括您安装软件的方式（从二进制包还是从源代码）以及您使用的 ROS 中间件/DDS 厂商（如果您知道的话）。
* 任何警告或错误。
  请直接从输出它们的终端窗口剪切并粘贴。
  请不要重新输入或提供截图。
* 如果是 bug，请考虑提供一个 `简短、自包含、正确（可编译）的示例 <https://sscce.org/>`__。
* 在讨论任何编译/链接/安装问题时，还请提供编译器版本

可视情况一并附上您的：

* ROS 环境变量（env | grep ROS）
* 回溯信息
* 相关配置文件
* 显卡型号和驱动版本
* 如有可能，rviz 的 Ogre.log（以 rviz -l 运行）
* 能重现问题的 bag 文件和代码示例
* 演示问题的 Gif 或视频

.. _Using ROS Discourse:

讨论
----

要与其他 ROS 2 社区成员发起讨论，请访问官方的 `Open Robotics Discourse <https://discourse.openrobotics.org/>`__。
Discourse 上的内容应该是高层次的；
它不是用来解答关于代码的 *问题* 的，但适合发起关于最佳实践或改进标准的对话。

有关 ROS 2 开发和计划的讨论在 `Open Robotics Discourse 的 ROS 分类 <https://discourse.openrobotics.org/c/ros/111>`__ 中进行。
参与这些讨论是对 ROS 2 各项功能如何工作和实现发表意见的重要方式。

ROS 生态背后的多元化社区是它最大的资产之一。
我们鼓励 ROS 社区的所有成员参与这些设计讨论，以便我们能够利用社区成员的经验，并在思考中兼顾 ROS 多样化的使用场景。

礼仪
----

假定‘善意’：网络上评论的含义或语气很容易被误解。
假定善意能让您对那些试图帮助您的人多一分宽容，从而避免：侮辱善意的社区成员，以及破坏氛围。
在回复时假定‘善意’几乎总是效果更好，即使最初的回复实际上并非出于善意。

请不要多次发送您的问题：问题已被看到。
如果您没有得到回复，那么很可能是没有人有时间回答您。
也可能是没有人知道答案。
无论如何，再次发送都是不好的做法，如同大声喊叫，很可能会激怒很多人。
这同样适用于跨平台发帖。
尽量选择您认为最合适的论坛并在那里提问。
如果您被引导到新的论坛，请提供指向旧讨论的链接。

在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上，您可以编辑自己的问题以提供更多细节。
您在问题中包含的细节越多，其他人就越容易帮您找到解决方案，您也就越有可能得到回复。

列出您的个人截止日期被视为不好的做法；回答问题的社区成员也有自己的截止日期。

不要乞求帮助。
如果有人愿意并且有能力帮助您解决问题，您通常会得到回复。
要求更快得到答案，大多会产生负面影响。

不要在帖子中添加无关内容。
帖子的内容应聚焦于当前主题，不应包含无关内容。
与主题无关的内容、链接和图片会被视为垃圾信息。

关于商业性帖子，另请参见 `这个讨论 <https://discourse.openrobotics.org/t/sponsorship-notation-in-posts-on-ros-org/2078>`_。

尽量减少引用付费墙后的内容。
发布在 `Open Robotics Discourse <https://discourse.openrobotics.org/>`__ 和 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上的内容“通常”应当是免费且对所有用户开放的。
指向付费墙后内容的链接（例如非公开的期刊文章、教科书和付费新闻网站）虽然可能有帮助且相关，但并非所有用户都能访问。
在可能的情况下，主要来源应当免费开放，付费内容只发挥辅助作用。

应避免只发一个链接的帖子。
一般来说，只发一个链接作为回答帮助较小，而且很容易与垃圾信息混淆。
此外，链接可能随时间失效或被替换。
用自己的话转述链接内容，并配合一些上下文信息和出处，往往有用得多。

私下联系
--------

如果您想私下联系我们（例如，您的问题包含对您所在组织或项目敏感的信息，或涉及安全问题），可以直接发邮件至 ``ros@osrfoundation.org``。
