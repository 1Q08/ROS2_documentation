.. redirect-from::

  Guides/Package-maintainer-guide
  How-To-Guides/Package-maintainer-guide

ROS 2 核心维护者指南
====================

ROS 2 核心中的每个包都有一个或多个负责该包整体健康状况的维护者。
本指南提供了一些关于 ROS 2 核心包维护者职责的信息。

.. contents:: 目录
   :local:

持续集成
--------

所有进入 ROS 2 核心仓库的代码都必须经过持续集成（Continuous Integration）。
ROS 2 目前有两个独立的 CI 系统，并且要求 PR 在合并之前必须同时通过这两个系统。

PR 构建 (https://build.ros2.org/view/Rpr)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 PR（拉取请求）构建会在每次打开拉取请求时自动运行。
这些构建仅针对此仓库（且仅限于此仓库）进行构建和测试。
这意味着它不会构建任何依赖项，也不会构建依赖于此仓库中包的任何仓库。
这些构建适合快速反馈，以查看更改是否通过了 linter、单元测试等。
它们存在两个主要问题：

* 这些构建无法跨多个仓库工作（因此无法用于添加或更改 API 等场景）
* 这些测试仅在 Linux 上运行（不会在 macOS 或 Windows 上运行）

为了解决这两个问题，还有 CI 构建。

CI 构建 (https://ci.ros2.org)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CI 构建不会在打开拉取请求时自动运行。
仓库的维护者之一必须前往 https://ci.ros2.org/job/ci_launcher/ 手动请求执行 CI 构建。

默认情况下，以这种方式运行作业会在所有平台（Linux、macOS 和 Windows）上构建并运行所有包（目前超过 300 个）的测试。
由于一次完整运行可能需要数小时并占用 CI 机器，建议此处的所有运行都限制要构建和测试的包数量。
这可以通过使用 colcon 参数 ``--packages-up-to``、``--packages-select``、``--packages-above-and-dependencies``、``--packages-above`` 等来实现。
有关可使用的标志的更多示例，请参见 `colcon 文档 <https://colcon.readthedocs.io/en/released/user/how-to.html#build-only-a-single-package-or-selected-packages>`__。
有关如何使用 CI 机器的更多文档，请访问 https://github.com/ros2/ci/blob/master/CI_BUILDERS.md。

合并拉取请求
------------

如果以下所有条件都成立，则可以合并拉取请求：

* DCO 机器人报告通过结果
* PR 构建报告通过结果
* CI 构建在所有平台上报告通过结果
* PR 已经过至少一名维护者的审查和批准

有关 PR 被审查时会发生什么的更多信息，请参见 :doc:`/The-ROS2-Project/Contributing/Contributing-to-code/Reviewing-a-PR`。

PR 合并后，它将自动在下一次 `nightlies <https://ci.ros2.org/view/nightly>`__ 中被构建。
强烈建议在合并拉取请求后检查 nightly，以确保没有发生回归。

保持 CI 绿色
------------

运行测试的 nightly 作业通常比针对单个拉取请求所做的要全面得多。
因此，nightly 中可能会出现 CI 作业中未发现的回归。
维护者有责任在以下位置检查其包是否存在回归：

* https://ci.ros2.org/view/nightly
* https://ci.ros2.org/view/packaging
* https://build.ros2.org/view/Rci
* https://build.ros2.org/view/Rdev

对于发现的任何问题，应在相关仓库上提交新的 issue 和/或拉取请求。

制作发布版本
------------

为了将新功能和错误修复交付给最终用户，维护者必须定期对仓库进行发布（也可以应其他维护者的要求按需发布）。

正如 :ref:`开发者指南 <semver>` 中所述，ROS 2 包的版本号遵循 semver。

在 ROS 术语中，一次发布包含两个不同的步骤：制作源代码发布，然后制作二进制发布。

源代码发布
^^^^^^^^^^

源代码发布会在相关仓库中创建变更日志（changelog）和标签（tag）。

该过程从使用以下命令生成或更新 CHANGELOG.rst 文件开始：

.. code-block:: console

  $ catkin_generate_changelog

如果仓库中的一个或多个包没有包含 CHANGELOG.rst，请添加 ``--all`` 选项来为每个包填充所有先前的提交记录。
``catkin_generate_changelog`` 命令只会用仓库中的提交日志填充文件。
由于这些提交日志并不总是适合作为变更日志，建议编辑 CHANGELOG.rst 使其更具可读性。
编辑完成后，务必将更新后的 CHANGELOG.rst 文件提交到仓库。

下一步是使用以下命令提升 package.xml 和变更日志文件中的版本号：

.. code-block:: console

  $ catkin_prepare_release

此命令将查找仓库中的所有包，检查变更日志是否存在，检查是否存在未提交的本地更改，递增 package.xml 文件中的版本号，并使用与 bloom 兼容的标签提交/打标签这些更改。
使用此命令是确保发布版本一致且与 bloom 兼容的最佳方式。
默认情况下，``catkin_prepare_release`` 会提升包的补丁版本号，例如 0.1.1 -> 0.1.2。
但是，它也可以提升次版本号或主版本号，甚至可以设置确切的版本号。
有关更多信息，请参见 ``catkin_prepare_release`` 的帮助输出。

假设上述操作成功，源代码发布就完成了。

二进制发布
^^^^^^^^^^

下一步是使用 ``bloom-release`` 命令创建二进制发布。
有关如何使用 bloom 的完整说明，请参见 http://wiki.ros.org/bloom。
要对仓库进行二进制发布，请运行：

.. code-block:: console

  $ bloom-release --track <rosdistro> --rosdistro <rosdistro> <repository_name>

例如，要将 ``rclcpp`` 仓库发布到 {DISTRO_TITLE} 发行版，命令如下：

.. code-block:: console

  $ bloom-release --track {DISTRO} --rosdistro {DISTRO} rclcpp

此命令将获取发布仓库，进行发布所需的更改，将更改推送到发布仓库，最后向 https://github.com/ros/rosdistro 打开一个拉取请求。

向已发布的发行版回溯移植
------------------------

所有传入的更改都应首先落在开发分支上。
一旦更改合并到开发分支，就可以考虑将其回溯移植到已发布的发行版。
但是，任何回溯移植的代码都不得破坏已发布发行版中的 `API <https://en.wikipedia.org/wiki/API>`__ 或 `ABI <https://en.wikipedia.org/wiki/Application_binary_interface>`__。
如果可以在不破坏 API 或 ABI 的情况下回溯移植更改，则应创建一个针对相应分支的新拉取请求。
新拉取请求应添加到 https://github.com/orgs/ros2/projects 上相应的发行版项目看板中。
新拉取请求应像之前一样执行所有步骤，但务必针对相应的发行版进行 CI 等操作。

回应 issue
----------

包维护者还应查看仓库中传入的 issue，并对用户遇到的问题进行分类（triage）。

对于看起来像问题的 issue，应关闭该 issue，并将用户引导至 `Robotics Stack Exchange <https://robotics.stackexchange.com/>`__。

如果某个 issue 看起来是问题，但与此特定仓库无关，则应使用 GitHub 的 "Transfer issue" 按钮将其移动到相应的仓库。

如果报告者没有提供足够的信息来确定问题的原因，则应向报告者索取更多信息。

如果这是一个新功能，请为 issue 打上 "help-wanted" 标签。

所有剩余的 issue 都应被复现，并确定它们是否确实是 bug。
如果确实是 bug，非常欢迎提供修复。

获取帮助
--------

在对包进行维护时，可能会遇到有关一般流程或单个 issue 的问题。

对于一般性问题，请遵循 :doc:`贡献指南 <../The-ROS2-Project/Contributing>`。

对于单个 issue 的问题，请标记 ROS 2 GitHub 团队 (@ros/team)，团队中的某个人会查看。
