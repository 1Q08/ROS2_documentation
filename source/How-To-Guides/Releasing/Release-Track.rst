发布 Track
==========

.. contents:: 目录
   :depth: 2
   :local:

.. _what-is-a-track:

什么是 Track？
--------------

Bloom 要求用户在首次发布包时输入配置信息。
将这些配置存储在发布仓库中是很有益的，这样我们就不必为后续发布手动输入不会改变的配置。

由于在针对不同 ROS 发行版发布包时，某些配置会有所不同，bloom 使用**发布 track 来按发行版存储发布配置**。
按照约定，你应该创建与你正在发布所针对的 ROS 发行版同名的 track。

所有发布 track 配置都存储在你发布仓库 master 分支上的 ``tracks.yaml`` 中。

Track 配置
----------

下面结合 bloom 的提示更详细地解释 track 配置。

.. _release-repository-url:

发布仓库 url
^^^^^^^^^^^^

这是你发布仓库的 url，如果你的发布仓库托管在 ros2-gbp 上，其形式应为 ``https://github.com/ros2-gbp/my_repo-release.git``。

.. code-block:: bash

   No reasonable default release repository url could be determined from previous releases.
   Release repository url [press enter to abort]:

粘贴你的发布仓库 URL 并按 Enter 键。

Bloom 可能还会询问你是否初始化新仓库，如下所示：

.. code-block:: bash

   Freshly initialized git repository detected.
   An initial empty commit is going to be made.
   Continue [Y/n]?

只需按 Enter 键接受默认的 yes。

.. _repository-name:

仓库名称
^^^^^^^^

仓库名称是简单的，但建议将其设置为你的项目名称。

.. code-block:: bash

   Repository Name:
      upstream
         Default value, leave this as upstream if you are unsure
      <name>
         Name of the repository (used in the archive name)
      ['upstream']:

输入你的项目名称（例如 ``my_project``）并按 Enter 键。

.. _upstream-repository-uri:

上游仓库 URI
^^^^^^^^^^^^

**上游仓库** 是你的源代码所在的仓库。
这很可能是指向你托管在诸如 GitHub 或 GitLab 之类的 git 托管服务上的项目的 https 链接。

.. code-block:: bash

   Upstream Repository URI:
      <uri>
         Any valid URI. This variable can be templated, for example an svn url
         can be templated as such: "https://svn.foo.com/foo/tags/foo-:{version}"
         where the :{version} token will be replaced with the version for this release.
      [None]:

确保你 **使用 https 地址** （例如 ``https://github.com/my_organization/my_repo.git``）而不是 ssh 地址。

.. _upstream-vcs-type:

上游 VCS 类型
^^^^^^^^^^^^^

这是 `上游仓库 URI`_ 的版本控制系统（VCS）类型。
你必须指定你的仓库所使用的 vcs 类型，可选 ``svn``、``git``、``hg`` 或 ``tar``。

.. code-block:: bash

   Upstream VCS Type:
      svn
         Upstream URI is a svn repository
      git
         Upstream URI is a git repository
      hg
         Upstream URI is a hg repository
      tar
         Upstream URI is a tarball
      ['git']:

大多数仓库会使用 git，但一些遗留仓库可能使用 hg 或 svn。

.. _version:

版本
^^^^

这是你正在发布的包的版本。
（例如 ``1.0.3``）

.. code-block:: bash

   Version:
      :{ask}
         This means that the user will be prompted for the version each release.
         This also means that the upstream devel will be ignored.
      :{auto}
         This means the version will be guessed from the devel branch.
         This means that the devel branch must be set, the devel branch must exist,
         and there must be a valid package.xml in the upstream devel branch.
      <version>
         This will be the version used.
         It must be updated for each new upstream version.
      [':{auto}']:

将其设置为 ``:{auto}`` （默认值，也是推荐的设置）将从 devel 分支的 package.xml 自动确定版本。

将其设置为 ``:{ask}`` 会在你每次用 bloom 运行发布时弹出提示，要求输入版本。

.. _release-tag:

发布标签
^^^^^^^^

发布标签指的是你想从哪里导入代码的标签或分支。

.. code-block:: bash

   Release Tag:
      :{version}
         This means that the release tag will match the :{version} tag.
         This can be further templated, for example: "foo-:{version}" or "v:{version}"

         This can describe any vcs reference. For git that means {tag, branch, hash},
         for hg that means {tag, branch, hash}, for svn that means a revision number.
         For tar this value doubles as the sub directory (if the repository is
         in foo/ of the tar ball, putting foo here will cause the contents of
         foo/ to be imported to upstream instead of foo itself).
      :{ask}
         This means the user will be prompted for the release tag on each release.
      :{none}
         For svn and tar only you can set the release tag to :{none}, so that
         it is ignored.  For svn this means no revision number is used.
      [':{version}']:

将其设置为 ``:{version}`` （默认值，也是推荐的设置）将使发布标签与版本标签匹配。

一种不太常见的设置是将其设置为一个分支名称，以便在发布时始终从上游项目拉取该分支。

或者，如果你想在每次发布时都被提示输入不同的标签，请输入 ``:{ask}``。
如果上游项目频繁发布带标签的版本，并且你希望每次发布时都引用新标签，那么 ``:{ask}`` 会很有用。

.. _upstream-devel-branch:

上游开发分支
^^^^^^^^^^^^

上游开发分支是你的 :ref:`上游仓库 <upstream-repository-uri>` 中的分支名称。
如果你为每个 ROS 发行版使用单独的分支，那么每个发布 track 的此字段都会不同。
当 :ref:`版本 <version>` 设置为 ``:{auto}`` 时，它用于确定你正在发布的包的版本。

.. code-block:: bash

   Upstream Devel Branch:
      <vcs reference>
         Branch in upstream repository on which to search for the version.
         This is used only when version is set to ':{auto}'.
      [None]:

要从名为 ``{DISTRO}`` 的分支发布，请输入 ``{DISTRO}``。
将其保留为 ``None`` 会导致版本从你仓库的默认分支确定（不建议这样做）。

.. _ros-distro:

ROS 发行版
^^^^^^^^^^

这是你计划将包发布到的发行版。

.. code-block:: bash

   ROS Distro:
      <ROS distro>
         This can be any valid ROS distro, e.g. indigo, kinetic, lunar, melodic
      ['indigo']:

如果你计划发布到 ROS {DISTRO}，请输入 ``{DISTRO}``。

.. _patches-directory:

补丁目录
^^^^^^^^

这是存放对发布所做的任何额外补丁的目录。

.. code-block:: bash

   Patches Directory:
      <path in bloom branch>
         This can be any valid relative path in the bloom branch. The contents
         of this folder will be overlaid onto the upstream branch after each
         import-upstream.  Additionally, any package.xml files found in the
         overlay will have the :{version} string replaced with the current
         version being released.
      :{none}
         Use this if you want to disable overlaying of files.
      [None]:

为发布添加额外补丁是一个很少用到的功能。
对于几乎所有包，这都应保留为默认值 ``None``。

.. _release-repository-push-url:

发布仓库推送 URL
^^^^^^^^^^^^^^^^

.. code-block:: bash

   Release Repository Push URL:
      :{none}
         This indicates that the default release url should be used.
      <url>
         (optional) Used when pushing to remote release repositories. This is only
         needed when the release uri which is in the rosdistro file is not writable.
         This is useful, for example, when a releaser would like to use a ssh url
         to push rather than a https:// url.
      [None]:

在大多数情况下可以保留为默认值。
