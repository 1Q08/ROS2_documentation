为你的软件包建立索引
====================

你是否要将一个新的 ROS 软件包发布到某个 ROS 发行版中？
先为你的软件包建立索引，可以让这一过程更快。

将你的 ROS 软件包放入公共仓库
-----------------------------

如果你还没有这样做，请把你的 ROS 软件包的源代码放入一个公共 git 仓库中。
所有发布到 ROS 中的软件包都必须是开源的。
你可以把代码托管在任何地方，但推荐使用 GitHub，因为它让你可以选择启用拉取请求作业。
以下是一些选项：

* `GitHub <https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository>`__ **推荐**
* `GitLab <https://docs.gitlab.com/ee/user/project/repository/>`__
* `Bitbucket <https://support.atlassian.com/bitbucket-cloud/docs/create-a-git-repository/>`__

为你的软件包选用 OSI 批准的许可证
---------------------------------
选择一个 `OSI 批准的许可证 <https://opensource.org/licenses>`__ 并将其用于你的 ROS 软件包。
如果你难以决定，可以考虑使用大多数核心 ROS 2 软件包所采用的许可证：`Apache-2.0 许可证 <https://opensource.org/license/apache-2-0>`__。

对于你仓库中的每个 ``package.xml``，请把许可证的 SPDX 短标识符填入 ``package.xml`` 中的 ``<license>`` 标签。

如果你的所有 ROS 软件包使用同一许可证，或者你的仓库中只有一个 ROS 软件包，请在你的仓库根目录下创建一个名为 ``LICENSE`` 的文件，并将你所选许可证的文本写入其中。
如果你仓库中的 ROS 软件包使用不同的许可证，请在每个 ``package.xml`` 文件旁边都创建一个 ``LICENSE`` 文件。

为你的软件包取符合 REP 144 的名称
---------------------------------
发布到某个 ROS 发行版中的软件包，其名称必须符合 `REP 144 <https://reps.openrobotics.org/rep-0144/>`__。
请阅读完整的 REP 以了解相关规则。
如果你的某个 ROS 软件包名称不符合规则，请在继续之前先修改该名称。

决定你要发布到哪个 ROS 发行版
-----------------------------
决定你要把你的软件包发布到哪个 ROS 发行版中。
至少，你应当把你的软件包发布到 `ROS Rolling <https://docs.ros.org/en/rolling>`__，这样你的 ROS 软件包就会自动被纳入下一次 ROS 发布。
你也可以选择发布到任何仍在活跃的 ROS 发行版中，但这由你自己决定。

创建 GitHub 账号
----------------
如果你还没有，请 `创建一个 GitHub 账号 <https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github>`__。
你不必把 ROS 软件包的源代码托管在 GitHub 上，但要为软件包建立索引和发布，你需要一个账号。

复刻（fork）并克隆 ros/rosdistro
--------------------------------
`复刻（fork） <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo>`__ `ros/rosdistro <https://github.com/ros/rosdistro/>`__ 仓库。
你只需要在你的账号上执行一次这一步。
之后每次发布都会用到这个复刻。

修改你的复刻
------------
还记得你决定要发布到的那些 ROS 发行版吗？
每个 ROS 发行版在 `ros/rosdistro <https://github.com/ros/rosdistro/>`__ 仓库中都有一个文件夹。
例如，ROS Rolling 的文件夹名称是 ``rolling``。
对于你想发布到的每个 ROS 发行版：

1. 填写下面的模板
2. 将填写好的模板放入对应 ROS 发行版文件夹下的 ``distribution.yaml`` 文件中

.. code-block:: yaml

  YOUR-REPO-NAME:
    source:
      type: git
      url: https://YOUR-GIT-REPO-URL.git
      version: YOUR-BRANCH-NAME
    status: YOUR-STATUS

以下说明各项该如何填写：

* YOUR-REPO-NAME：这是一个任意的人类可读名称。
  对于托管在 GitHub 上的仓库，请使用你仓库的小写名称，但不包含组织名。
  例如，``https://github.com/ros2/rosidl`` 的仓库名称是 ``rosidl``。
* YOUR-GIT-REPO-URL：这是可以用 ``git clone`` 克隆你仓库的 https URL
  例如，``https://github.com/ros2/rosidl`` 的 git 仓库 URL 是 ``https://github.com/ros2/rosidl.git``。
  重要的是，该 URL 必须以 ``.git`` 结尾，否则将无法通过 linter 检查。
* YOUR-BRANCH-NAME：这是你仓库中要用来把软件包发布到该 ROS 发行版的 git 分支。
  通常为下列之一：``main``、``master`` 或该 ROS 发行版本身的名称。
  例如，`rosidl 仓库 <https://github.com/ros2/rosidl>`__ 使用 ``rolling`` 分支来保存要发布到 ROS Rolling 的改动。
* YOUR-STATUS：这是 `REP 141 <https://reps.openrobotics.org/rep-0141/#distribution-file>`__ 列表中的一个状态。
  你很可能想用 ``maintained`` 或 ``developed``。

向 ros/rosdistro 提交拉取请求
-----------------------------
向你修改所用的分支，向 `ros/rosdistro <https://github.com/ros/rosdistro/>`__ `提交一个拉取请求 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`__。
等待几天以接受审核。

接下来会发生什么
----------------
你现在已经完成了为 ROS 软件包建立索引所需的一切工作。
某位审核者会查看你的拉取请求，并判断它是否 `符合审核指南 <https://github.com/ros/rosdistro/blob/master/REVIEW_GUIDELINES.md>`__。
审核者可能会原样批准你的改动，也可能给你可执行的反馈。
一旦拉取请求符合审核指南，它就会被合并，你的软件包将会出现在 `ROS Index <https://index.ros.org/>`__ 上。

你已经完成了发布软件包过程中的一个重要步骤。
请继续阅读下一个指南：:doc:`首次发布 <First-Time-Release>`。
