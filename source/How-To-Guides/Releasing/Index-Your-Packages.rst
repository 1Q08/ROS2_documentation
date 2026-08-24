为你的包建立索引
================

你是否要将一个新的 ROS 包发布到某个 ROS 发行版中？
先为你的包建立索引，可以让流程更快。

将你的 ROS 包放入公共仓库
-------------------------

如果你还没有这样做，请将你的 ROS 包源代码放入一个公共 git 仓库中。
所有发布到 ROS 的包都必须是开源的。
你可以将代码托管在任何地方，但推荐使用 GitHub，因为它为你提供了启用拉取请求作业的选项。
以下是一些选择：

* `GitHub <https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository>`__ **推荐**
* `GitLab <https://docs.gitlab.com/ee/user/project/repository/>`__
* `Bitbucket <https://support.atlassian.com/bitbucket-cloud/docs/create-a-git-repository/>`__

为你的包提供 OSI 批准的许可证
-----------------------------
选择一个 `OSI 批准的许可证 <https://opensource.org/licenses>`__ 并提供给你的 ROS 包。
如果你难以决定，可以考虑使用大多数核心 ROS 2 包所使用的许可证：`Apache-2.0 许可证 <https://opensource.org/license/apache-2-0>`__。

对于你仓库中的每个 ``package.xml``，将许可证的 SPDX 短标识符放入你的 ``package.xml`` 的 ``<license>`` 标签中。

如果你的所有 ROS 包都使用相同的许可证，或者你的仓库中只有一个 ROS 包，请在你的仓库根目录创建一个名为 ``LICENSE`` 的文件，并将你选择的许可证文本放入其中。
如果你的仓库中的 ROS 包使用不同的许可证，请在每个 ``package.xml`` 文件旁边创建一个 ``LICENSE`` 文件。

为你的包提供符合 REP 144 的名称
-------------------------------
发布到 ROS 发行版中的包必须具有符合 `REP 144 <https://reps.openrobotics.org/rep-0144/>`__ 的名称。
请阅读完整的 REP 以了解这些规则。
如果你的某个 ROS 包名称不符合要求，请在继续之前更改该名称。

决定你想发布到哪个 ROS 发行版
-----------------------------
决定你想将你的 ROS 包发布到哪个 ROS 发行版。
至少，你应该将你的包发布到 `ROS Rolling <https://docs.ros.org/en/rolling>`__，这样你的 ROS 包就会被自动包含在下一个 ROS 版本中。
你可能还想发布到任何活跃的 ROS 发行版，但这由你决定。

创建一个 GitHub 账户
--------------------
如果你还没有 GitHub 账户，请`创建一个 <https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github>`__。
你不必在 GitHub 上托管你的 ROS 包源代码，但你需要一个账户来为包建立索引和发布包。

Fork 并克隆 ros/rosdistro
-------------------------
`Fork <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo>`__ `ros/rosdistro <https://github.com/ros/rosdistro/>`__ 仓库。
你只需在你的账户上执行一次这一步。
每次发布时都会用到这个 fork。

对你的 fork 进行更改
--------------------
还记得你决定要发布到哪些 ROS 发行版吗？
每个 ROS 发行版在 `ros/rosdistro <https://github.com/ros/rosdistro/>`__ 仓库中都有一个文件夹。
例如，ROS Rolling 文件夹的名称是 ``rolling``。
对于你想发布到的每个 ROS 发行版：

1. 填写以下模板
2. 将填写好的模板放入相应 ROS 发行版文件夹中的 ``distribution.yaml`` 文件中

.. code-block:: yaml

  YOUR-REPO-NAME:
    source:
      type: git
      url: https://YOUR-GIT-REPO-URL.git
      version: YOUR-BRANCH-NAME
    status: YOUR-STATUS

以下是如何填写每一项：

* YOUR-REPO-NAME: 这是一个任意的人类可读名称。
  对于托管在 GitHub 上的仓库，请使用你仓库的小写名称，不包括组织。
  例如，``https://github.com/ros2/rosidl`` 的仓库名称是 ``rosidl``。
* YOUR-GIT-REPO-URL: 这是人们可以用 ``git clone`` 克隆你仓库的 https URL。
  例如，``https://github.com/ros2/rosidl`` 的 git 仓库 URL 是 ``https://github.com/ros2/rosidl.git``。
  重要的是，这个 URL 要以 ``.git`` 结尾，否则将无法通过 linter。
* YOUR-BRANCH-NAME: 这是你仓库中用于将包发布到该 ROS 发行版的 git 分支。
  通常是以下之一：``main``、``master`` 或 ROS 发行版本身的名称。
  例如，`rosidl 仓库 <https://github.com/ros2/rosidl>`__ 使用 ``rolling`` 分支来存放要发布到 ROS Rolling 的更改。
* YOUR-STATUS: 这是 `REP 141 <https://reps.openrobotics.org/rep-0141/#distribution-file>`__ 列表中的一个状态。
  你很可能需要 ``maintained`` 或 ``developed``。

向 ros/rosdistro 打开一个拉取请求
---------------------------------
用你进行更改的分支，向 `ros/rosdistro <https://github.com/ros/rosdistro/>`__ `打开一个拉取请求 <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`__。
等待几天让它被审查。

接下来会发生什么
----------------
你现在已经完成了为你的 ROS 包建立索引所需的所有工作。
其中一位审查者会查看你的拉取请求，并决定它是否`满足审查指南 <https://github.com/ros/rosdistro/blob/master/REVIEW_GUIDELINES.md>`__。
审查者可能会原样批准你的更改，也可能给你可行的反馈。
一旦拉取请求满足审查指南，它将被合并，你的包将出现在 `ROS Index <https://index.ros.org/>`__ 上。

你已经完成了发布包的重要一步。
继续下一个指南：:doc:`首次发布 <First-Time-Release>`。
