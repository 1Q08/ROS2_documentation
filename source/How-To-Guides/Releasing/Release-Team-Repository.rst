发布团队 / 仓库
===============

.. contents:: 目录
   :depth: 2
   :local:

本页解释在 `ros2-gbp <https://github.com/ros2-gbp>`_ 上托管你的发布仓库的推荐方法。

什么是 ROS 2 GBP？
------------------

`ros2-gbp <https://github.com/ros2-gbp>`_ 是一个托管 ROS 包发布仓库的 GitHub 组织。
它还在 https://github.com/ros2-gbp/ros2-gbp-github-org 中维护着发布团队列表、每个发布团队的成员列表以及由发布团队维护的发布仓库列表。
与 ros2-gbp-github-org 的交互通过发起 GitHub issue 完成。
建议你尽早请求加入发布团队并设置发布仓库，因为 ros2-gbp 维护者可能需要一些时间才能响应你的请求。

.. _what-is-a-release-team:

什么是发布团队？
----------------

发布团队是一个 `GitHub 团队 <https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams>`_，由负责一个或多个仓库发布流程的一群人组成。
发布团队通常由一个组织、一个工作组甚至一个人组成，并以他们所代表的团队或小组命名。
发布团队及其关联发布仓库的列表维护在 `ros2-gbp-github-org <https://github.com/ros2-gbp/ros2-gbp-github-org>`_ 中。

**你必须是你计划为其发布项目所属发布团队的一员。**
如果你打算在现有团队下发布仓库，请按照 :ref:`加入发布团队 <join-a-release-team>` 操作。
如果你打算组建一个新团队，请按照 :ref:`组建新发布团队 <start-a-new-release-team>` 操作。

.. _join-a-release-team:

加入发布团队
^^^^^^^^^^^^

如果你的项目已经存在发布团队，但你不是其中一员，请填写 `Update Release Team Membership issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=update_release_team_membership.md&title=Update+release+team+membership>`_ 问题模板。

.. _start-a-new-release-team:

组建新发布团队
^^^^^^^^^^^^^^

如果你的项目尚不存在发布团队，请填写 `New Release Team issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=new_release_team.md&title=Add+release+team>`_ 问题模板以请求创建一个。

.. _what-is-a-release-repository:

什么是发布仓库？
----------------

发布仓库是一个这样的仓库：

* 存储从发布流程生成的文件，供 ROS buildfarm 使用
* 缓存发布流程中的配置，以简化该仓库未来的后续发布

拥有一个与源代码仓库分离的发布仓库是在 ROS 2 中进行发布的必要条件。

.. _create-a-new-release-repository:

创建新的发布仓库
^^^^^^^^^^^^^^^^

如果你的仓库对 ROS 社区来说是全新的，你应该首先在 `ros/rosdistro <https://github.com/ros/rosdistro>`_ 上打开一个拉取请求，为你的仓库添加一个 ``source`` 条目（例如 https://github.com/ros/rosdistro/pull/39513）。
rosdistro 数据库的审查流程将确保你的仓库和包在发布前符合 `REP 144 包命名约定 <https://reps.openrobotics.org/rep-0144/>`_ 和其他要求。
一旦你的包名获得批准并合并，如果你的项目还没有发布仓库，请填写 `Add New Release Repositories issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=new_release_repository.md&title=Add+new+release+repositories>`_ 问题模板。

如果我现有的发布仓库不在 ros2-gbp 上怎么办？
--------------------------------------------

在 ros2-gbp 存在之前发布的包，其发布仓库可能托管在其他地方。
现在强烈建议将发布仓库放在这个专门的 GitHub 组织中。
如果你正在将 ROS 1 包移植到 ROS 2，并计划首次将你的包发布到 ROS 2 中，请按照标准流程为你的 ROS 2 发布请求一个新的发布仓库。
如果你之前已经为 ROS 2 发布过你的包，在发起 `Add New Release Repositories issue <https://github.com/ros2-gbp/ros2-gbp-github-org/issues/new?assignees=&labels=&template=new_release_repository.md&title=Add+new+release+repositories>`_ 时，请\ **指定你当前的发布仓库 url**，其余部分按照标准流程操作。

.. note::

   **当将你的包发布到 Rolling 发行版时，你必须使用托管在 ros2-gbp 组织中的发布仓库**。
   如果你不打算将仓库发布到 Rolling，则托管在其他地方的发布仓库对稳定发行版仍然受支持。
   由于由 Rolling 创建的稳定发行版将从 ros2-gbp 组织中的发布仓库开始，建议你对所有 ROS 2 发行版都使用 ros2-gbp 发布仓库，以避免发布信息碎片化。

   未来，ros2-gbp 发布仓库可能会成为所有发行版的硬性要求，而为所有 ROS 2 发行版维护一个单一的发布仓库，可以简化 Rolling 发行版维护者和包维护者的发布维护工作。
