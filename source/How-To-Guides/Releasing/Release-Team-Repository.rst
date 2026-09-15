发布团队 / 仓库
===============

.. contents:: 目录
   :depth: 2
   :local:

本页说明将发布仓库托管在 `ros2-gbp <https://github.com/ros2-gbp>`_ 上的推荐方法。

什么是 ROS 2 GBP？
------------------

`ros2-gbp <https://github.com/ros2-gbp>`_ 是一个托管 ROS 软件包发布仓库的 GitHub 组织。
它还在 https://github.com/ros2-gbp/ros2-gbp-github-org 中维护发布团队列表、每个发布团队的成员列表，以及各发布团队所维护的发布仓库列表。
与 ros2-gbp-github-org 的交互通过提交 GitHub issue 来完成。
建议你尽早申请加入发布团队并设置发布仓库，因为 ros2-gbp 维护者响应你的请求可能需要一些时间。

.. _what-is-a-release-team:

什么是发布团队？
----------------

发布团队是一个 `GitHub 团队 <https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams>`_，由一群负责一个或多个仓库发布流程的人员组成。
发布团队通常由某个组织、某个工作组，甚至某个个人组成，并以它们所代表的团队或小组命名。
发布团队列表及其对应的发布仓库维护在 `ros2-gbp-github-org <https://github.com/ros2-gbp/ros2-gbp-github-org>`_ 中。

**你必须是你要为其发布项目的那个发布团队的一员。**
如果你打算以某个现有团队的名义发布该仓库，请按照 :ref:`加入发布团队 <join-a-release-team>` 操作。
如果你打算建立一个新的团队，请按照 :ref:`建立新的发布团队 <start-a-new-release-team>` 操作。

.. _join-a-release-team:

加入发布团队
^^^^^^^^^^^^

如果你的项目已有发布团队，但你并不是其中一员，请填写 `更新发布团队成员资格 issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=update_release_team_membership.md&title=Update+release+team+membership>`_ 模板。

.. _start-a-new-release-team:

建立新的发布团队
^^^^^^^^^^^^^^^^

如果你的项目还没有发布团队，请填写 `新建发布团队 issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=new_release_team.md&title=Add+release+team>`_ 模板，请求创建一个。

.. _what-is-a-release-repository:

什么是发布仓库？
----------------

发布仓库是一种仓库，它

* 存储发布流程生成的文件，供 ROS 构建农场使用
* 缓存发布流程中的配置，以便将来简化该仓库的后续发布

在 ROS 2 中，要发布就必须有一个独立于源代码仓库的发布仓库。

.. _create-a-new-release-repository:

创建新的发布仓库
^^^^^^^^^^^^^^^^

如果你的仓库对 ROS 社区来说是全新的，你应当先在 `ros/rosdistro <https://github.com/ros/rosdistro>`_ 上提交一个拉取请求，为你的仓库添加一个 ``source`` 条目（例如 https://github.com/ros/rosdistro/pull/39513）。
rosdistro 数据库的审核流程将确保你的仓库和软件包在发布前符合 `REP 144 软件包命名约定 <https://reps.openrobotics.org/rep-0144/>`_ 及其他要求。
一旦你的软件包名称获得批准并被合并，如果你的项目还没有发布仓库，请填写 `新增发布仓库 issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=new_release_repository.md&title=Add+new+release+repositories>`_ 模板。

如果我已有的发布仓库不在 ros2-gbp 上怎么办？
--------------------------------------------

在 ros2-gbp 出现之前发布的软件包，其发布仓库可能托管在别处。
现在强烈建议将发布仓库放在这个专门的 GitHub 组织中。
如果你正在把一个 ROS 1 软件包移植到 ROS 2，并打算首次把你的软件包发布到 ROS 2 中，请按照标准流程为你的 ROS 2 发布申请一个新的发布仓库。
如果你此前已经为 ROS 2 发布过你的软件包，那么在提交 `新增发布仓库 issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=new_release_repository.md&title=Add+new+release+repositories>`_ 时，**请注明你当前的发布仓库 url**，其余部分按照标准流程操作。

.. note::

   **当把你的软件包发布到 Rolling 发行版时，你必须使用托管在 ros2-gbp 组织中的发布仓库**。
   如果你不打算把该仓库发布到 Rolling，那么对于稳定发行版，托管在别处的发布仓库仍然受支持。
   由于从 Rolling 创建出来的稳定发行版将以 ros2-gbp 组织中的发布仓库作为起点，因此建议你对所有 ROS 2 发行版都使用 ros2-gbp 发布仓库，以避免发布信息碎片化。

   ros2-gbp 发布仓库将来可能会成为所有发行版的硬性要求，而为所有 ROS 2 发行版只维护一个发布仓库，可以简化 Rolling 发行版维护者和软件包维护者双方的发布维护工作。
