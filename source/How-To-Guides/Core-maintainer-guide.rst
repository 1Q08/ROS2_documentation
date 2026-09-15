.. redirect-from::

  Guides/Package-maintainer-guide
  How-To-Guides/Package-maintainer-guide

ROS 2 核心维护者指南
====================

ROS 2 核心中的每个软件包都有一名或多名维护者，负责该软件包的整体健康状况。
本指南提供了一些有关 ROS 2 核心软件包维护者职责的信息。

.. contents:: 目录
   :local:

持续集成
--------

所有进入 ROS 2 核心仓库的代码都必须经过持续集成（CI）。
ROS 2 目前有两个独立的 CI 系统，PR 必须同时通过这两者才能合并。

PR 构建（https://build.ros2.org/view/Rpr）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

每当有拉取请求（PR）打开时，ROS 2 的 PR 构建都会自动运行。
这些构建只对本仓库进行构建和测试，仅限本仓库。
这意味着它不会构建任何依赖项，也不会构建任何依赖本仓库中软件包的仓库。
这些构建非常适合快速反馈，用来查看修改是否通过了代码检查工具、单元测试等。
它们有两个主要问题：

* 这些构建无法跨多个仓库工作（因此不适用于添加或更改 API 等情况）
* 这些测试只在 Linux 上运行（不会在 macOS 或 Windows 上运行）

为了解决这两个问题，还有 CI 构建。

CI 构建（https://ci.ros2.org）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

当拉取请求打开时，CI 构建不会自动运行。
仓库的某位维护者必须访问 https://ci.ros2.org/job/ci_launcher/ 手动请求执行 CI 构建。

默认情况下，以这种方式运行任务会在所有平台（Linux、macOS 和 Windows）上为所有软件包（目前超过 300 个）进行构建和运行测试。
由于一次完整运行可能耗时数小时并占用 CI 机器，因此建议这里的所有运行都限制被构建和测试的软件包数量。
这可以通过使用 colcon 参数 ``--packages-up-to``、``--packages-select``、``--packages-above-and-dependencies``、``--packages-above`` 等来实现。
有关可用标志的更多示例，请参阅 `colcon 文档 <https://colcon.readthedocs.io/en/released/user/how-to.html#build-only-a-single-package-or-selected-packages>`__。
关于如何使用 CI 机制的更多文档见 https://github.com/ros2/ci/blob/master/CI_BUILDERS.md 。

合并拉取请求
------------

只有当以下条件全部满足时，拉取请求才可以合并：

* DCO 机器人报告结果为通过
* PR 构建报告结果为通过
* CI 构建在所有平台上报告结果为通过
* 该 PR 已经由至少一名维护者审查并批准

有关 PR 被审查时会发生什么的更多信息，请参阅 :doc:`/The-ROS2-Project/Contributing/Contributing-to-code/Reviewing-a-PR`。

PR 合并后，它会自动随下一次 `每日构建 <https://ci.ros2.org/view/nightly>`__ 一起构建。
强烈建议在合并拉取请求后检查每日构建，以确保没有引入回归。

保持 CI 绿色
------------

运行测试的每日任务通常比针对单个拉取请求所做的测试全面得多。
因此，每日构建中可能会出现 CI 任务中未曾发现的回归。
维护者有责任在以下位置检查其软件包是否出现回归：

* https://ci.ros2.org/view/nightly
* https://ci.ros2.org/view/packaging
* https://build.ros2.org/view/Rci
* https://build.ros2.org/view/Rdev

对于发现的任何问题，都应在相关仓库上提交新的 issue 和/或拉取请求。

发布版本
--------

为了把新功能和缺陷修复送达最终用户，维护者必须定期对仓库进行一次发布（其他维护者也可以按需请求发布）。

正如 :ref:`开发者指南 <semver>` 中所述，ROS 2 软件包的版本号遵循语义化版本规范（semver）。

在 ROS 术语中，一次发布包含两个不同的步骤：先做源码发布，然后做二进制发布。

源码发布
^^^^^^^^

源码发布会创建一个变更日志并在相关仓库中打一个标签。

该流程首先使用以下命令生成或更新 CHANGELOG.rst 文件：

.. code-block:: console

  $ catkin_generate_changelog

如果仓库中有一个或多个软件包不包含 CHANGELOG.rst，请加上 ``--all`` 选项来为每个软件包填充之前所有的提交。
``catkin_generate_changelog`` 命令只是简单地用仓库中的提交日志填充这些文件。
由于这些提交日志并不总是适合作为变更日志，建议编辑 CHANGELOG.rst 使其更易读。
编辑完成后，务必把更新后的 CHANGELOG.rst 文件提交到仓库。

下一步是使用以下命令更新 package.xml 和变更日志文件中的版本号：

.. code-block:: console

  $ catkin_prepare_release

该命令会查找仓库中的所有软件包，检查变更日志是否存在，检查是否有没有提交的本地修改，递增 package.xml 文件中的版本号，并以兼容 bloom 的标签提交/打标签这些修改。
使用该命令是确保发布版本一致且与 bloom 兼容的最佳方式。
默认情况下，``catkin_prepare_release`` 会递增软件包的补丁版本号，例如 0.1.1 -> 0.1.2 。
不过，它也可以递增次版本号或主版本号，甚至设置一个确切的版本号。
更多信息请参阅 ``catkin_prepare_release`` 的帮助输出。

假设以上操作成功，源码发布就完成了。

二进制发布
^^^^^^^^^^

下一步是使用 ``bloom-release`` 命令创建二进制发布。
关于如何使用 bloom 的完整说明，请参阅 http://wiki.ros.org/bloom 。
要对某个仓库进行二进制发布，请运行：

.. code-block:: console

  $ bloom-release --track <rosdistro> --rosdistro <rosdistro> <repository_name>

例如，要把 ``rclcpp`` 仓库发布到 {DISTRO_TITLE} 发行版，命令为：

.. code-block:: console

  $ bloom-release --track {DISTRO} --rosdistro {DISTRO} rclcpp

该命令会获取发布仓库，进行发布所需的必要更改，把更改推送到发布仓库，最后向 https://github.com/ros/rosdistro 提交一个拉取请求。

向后移植到已发布的发行版
------------------------

所有进入的更改都应首先落到开发分支上。
一旦更改被合并到开发分支，就可以考虑把它向后移植到已发布的发行版。
不过，任何向后移植的代码都不得破坏已发布发行版中的 `API <https://en.wikipedia.org/wiki/API>`__ 或 `ABI <https://en.wikipedia.org/wiki/Application_binary_interface>`__。
如果某个更改可以在不破坏 API 或 ABI 的情况下向后移植，那么就应该创建一个针对相应分支的新拉取请求。
新的拉取请求应添加到 https://github.com/orgs/ros2/projects 上相应的发行版项目看板中。
新的拉取请求应像之前一样完成所有步骤，但请确保 CI 等针对的是相应的发行版。

响应问题
--------

软件包维护者还应查看仓库上新增的 issue，并对用户遇到的问题进行分诊。

对于看起来像是提问的 issue，应关闭该 issue 并引导用户到 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__ 。

如果某个 issue 看起来是个问题，但与本仓库无关，则应使用 GitHub 的 “Transfer issue” 按钮将其转移到相应的仓库。

如果报告者没有提供足够的信息来确定问题的原因，应向报告者索取更多信息。

如果这是一个新功能需求，请给该 issue 打上 “help-wanted” 标签。

其余所有 issue 都应被复现，并判断它们是否真的是缺陷。
如果确实是缺陷，非常欢迎提供修复。

获取帮助
--------

在维护软件包的过程中，可能会遇到有关通用流程或单个 issue 的问题。

对于通用问题，请遵循 :doc:`贡献指南 <../The-ROS2-Project/Contributing>`。

对于单个 issue 的问题，请 @ 提及 ROS 2 GitHub 团队（@ros/team），团队中会有人来查看。
