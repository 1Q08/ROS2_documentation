.. _Help:

联系我们
========

.. _Using Robotics Stack Exchange:

获取支持
--------

不同类型的问题或讨论对应不同的沟通渠道；
请查看以下说明，确保选择正确的方式。

需要对系统进行故障排查？
请先在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上搜索，看看其他人是否遇到过类似问题，以及他们的解决方案是否适用于你。

如果没有找到答案，请在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上提出一个新问题。
请务必添加标签，至少添加 ``ros2`` 标签以及你所运行的发行版版本标签，例如 ``{DISTRO}``。
如果你的问题与本网站的文档相关，请添加 ``docs`` 之类的标签，或更具体的 ``tutorials`` 标签。

请不要直接联系开发者或维护者。
社区无法看到没有公开发布的问题或回答。
当整个社区都参与讨论并帮忙解答问题时，开源开发的效果才是最好的。
最好将所有问题发送到 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__，并将所有问题报告到问题跟踪器。

贡献支持
^^^^^^^^

ROS 2 用户来自广泛的技术背景，使用各种不同的操作系统，并且不一定具备 ROS（1 或 2）的相关经验。
因此，无论经验多少，用户都应积极参与贡献支持。

如果你在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上看到与你曾遇到的问题类似的情况，请考虑提供一些对你当时有所帮助的线索。
不必担心你的回答是否正确。
直接说明即可，必要时其他社区成员会参与进来。

问题反馈
--------

如果你发现了 bug、有改进建议，或遇到了针对某个软件包的问题，可以在 GitHub 上提交 issue。

例如，如果你正在按照这里的 :doc:`教程 <Tutorials>` 操作，却遇到了在你的系统上无法执行的指令，
你可以在 `ros2_documentation <https://github.com/ros2/ros2_documentation>`__ 仓库中提交 issue。

你可以在 `ROS 2 的 GitHub <https://github.com/ros2>`__ 上搜索各个 ROS 2 仓库。

在提交 issue 之前，请通过在 ros2 和 ament 两个 GitHub 组织中搜索来检查其他用户是否报告过类似问题：`示例搜索查询 <https://github.com/search?q=user%3Aros2+user%3Aament+turtlesim&type=Issues>`__。

接下来，检查 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__，看看是否已有其他人提出过你的问题或报告过你的 issue。

如果尚未被报告，请放心地在相应的仓库跟踪器中提交 issue。
如果不清楚某个问题应该使用哪个跟踪器，请将其提交到 `ros2/ros2 仓库 <https://github.com/ros2/ros2/issues>`__，我们会进行查看。

提交 issue 时，请务必：

* 提供足够的信息，以便他人理解该问题。

准确描述你当时正在做什么或试图做什么，以及究竟出了什么问题（如果有的话）。
如果是在按照某个教程或在线说明操作，请提供相应说明的链接。

* 使用描述性的标题或主题。
  反例："rviz doesn't work"（rviz 不能用）。
  正例："Rviz crashing looking for missing ``.so`` after latest apt update"（最新 apt 更新后 Rviz 因找不到 ``.so`` 而崩溃）
* 提供与问题相关的确切平台、软件、版本和环境信息。
  这包括软件的安装方式（从二进制包安装还是从源码安装），以及你所使用的 ROS 中间件/DDS 厂商（如果你知道的话）。
* 任何警告或错误信息。
  直接从打印这些信息的终端窗口中复制粘贴过来。
  请不要手动重新输入，也不要提供截图。
* 如果是 bug，请考虑提供一个 `简短、自包含、正确（可编译）的示例 <https://sscce.org/>`__。
* 在讨论任何编译/链接/安装问题时，还请提供编译器版本。

根据情况，还应包括你的：

* ROS 环境变量（env | grep ROS）
* 回溯信息（Backtraces）
* 相关配置文件
* 显卡型号和驱动版本
* rviz 的 Ogre.log（如果可能的话，使用 rviz -l 运行）
* 能够复现问题的 Bag 文件和代码示例
* 用于演示问题的 GIF 或视频

.. _Using ROS Discourse:

讨论
----

要与其他 ROS 2 社区成员展开讨论，请访问官方的 `Open Robotics Discourse <https://discourse.openrobotics.org/>`__。
Discourse 上的内容应该是高层次的；
它不是获取代码*问题*解答的地方，而是适合就最佳实践或改进标准发起对话的场所。

关于 ROS 2 开发和规划的讨论在 `Open Robotics Discourse 的 ROS 类别 <https://discourse.openrobotics.org/c/ros/111>`__ 中进行。
参与这些讨论是就 ROS 2 各项特性如何运作、如何实现发表意见的重要途径。

ROS 生态系统背后多元化的社区是其最宝贵的财富之一。
我们鼓励 ROS 社区的所有成员都参与到这些设计讨论中来，以便我们能够汲取社区成员的经验，并时刻牢记 ROS 的各种使用场景。

礼仪
----

假定"善意"：互联网上评论的含义或语气很容易被误解。
假定善意意味着对试图帮助你的人给予善意的推定，从而避免：冒犯出于好意的社区成员，以及破坏氛围。
即使对方的原始回复实际上并非出于善意，以"善意"为前提进行回应也几乎总能取得更好的效果。

请不要将你的问题重复发送：问题已被看到。
如果你没有收到回复，那很可能是还没有人有时间回答你。
或者，也可能是没有人知道答案。
无论如何，重复发送都是不礼貌的行为，无异于大声喊叫，很可能会惹恼很多人。
这也同样适用于交叉发帖（crossposting）。
尽量选择你认为最合适的论坛去提问。
如果你被指引到新的论坛，请附上旧讨论的链接。

在 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上，你可以编辑问题以补充更多细节。
你在问题中包含的细节越多，别人就越容易帮你找到解决方案，你也越有可能得到回复。

列出你的个人截止日期被认为是不礼貌的行为；负责解答问题的社区成员也有自己的截止日期。

不要乞求帮助。
只要有人愿意并且能够帮你解决问题，你通常都会得到回复。
催促更快地答复大多只会产生负面效果。

不要在帖子中添加无关内容。
帖子的内容应聚焦于当前话题，不应包含无关内容。
与话题无关的内容、链接和图片会被视为垃圾信息。

对于商业性帖子，另请参阅 `此讨论 <https://discourse.openrobotics.org/t/sponsorship-notation-in-posts-on-ros-org/2078>`_。

尽量减少引用付费墙之后的内容。
发布在 `Open Robotics Discourse <https://discourse.openrobotics.org/>`__ 和 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 上的内容"通常"应对所有用户免费且开放。
付费墙之后的链接（如私有期刊文章、教科书和付费新闻网站）虽然有用且相关，但可能并非所有用户都能访问。
在可能的情况下，主要来源应当免费且开放，付费内容仅起辅助作用。

应避免只发一个链接的帖子。
一般来说，只发一个链接的回答帮助较小，而且很容易被误认为垃圾信息。
此外，链接可能会随着时间推移失效或被替换。
将链接内容用自己的话复述，并附上一些上下文信息和出处，往往更有帮助。

私下联系
--------

如果你希望私下联系我们（例如，你的问题包含对所在组织或项目敏感的信息，或者涉及安全问题时），你可以直接发送邮件至 ``ros@osrfoundation.org``。
