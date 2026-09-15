发布轨道
========

.. contents:: 目录
   :depth: 2
   :local:

.. _what-is-a-track:

什么是轨道？
------------

Bloom 在首次发布软件包时要求用户输入配置信息。
把这些配置保存在发布仓库中是很有好处的，这样我们在后续发布时就不必再次手动输入那些不会变化的配置。

由于针对不同的 ROS 发行版发布软件包时，某些配置会有所不同，因此 bloom 使用 **发布轨道来存储每个发行版的发布配置。**
按照惯例，你应当创建与你要发布到的 ROS 发行版同名的轨道。

所有发布轨道配置都存储在你发布仓库 master 分支上的 ``tracks.yaml`` 中。

轨道配置
--------

各轨道配置会结合 bloom 的提示一并详细说明。

.. _release-repository-url:

发布仓库 url
^^^^^^^^^^^^

这是你发布仓库的 url，如果你的发布仓库托管在 ros2-gbp 上，其形式应为 ``https://github.com/ros2-gbp/my_repo-release.git``。

.. code-block:: bash

   No reasonable default release repository url could be determined from previous releases.
   Release repository url [press enter to abort]:

粘贴你的发布仓库 URL 并按 Enter。

Bloom 还可能就初始化新仓库向你提问，如下所示：

.. code-block:: bash

   Freshly initialized git repository detected.
   An initial empty commit is going to be made.
   Continue [Y/n]?

直接按 Enter 接受默认选项 yes 即可。

.. _repository-name:

仓库名称
^^^^^^^^

仓库名称本身并不重要，但建议将其设置为你的项目名称。

.. code-block:: bash

   Repository Name:
      upstream
         Default value, leave this as upstream if you are unsure
      <name>
         Name of the repository (used in the archive name)
      ['upstream']:

输入你的项目名称（例如 ``my_project``）并按 Enter。

.. _upstream-repository-uri:

上游仓库 URI
^^^^^^^^^^^^

**上游仓库** 是存放你源代码的仓库。
它很可能是托管在 GitHub 或 GitLab 等 git 托管服务上的你项目的 https 链接。

.. code-block:: bash

   Upstream Repository URI:
      <uri>
         Any valid URI. This variable can be templated, for example an svn url
         can be templated as such: "https://svn.foo.com/foo/tags/foo-:{version}"
         where the :{version} token will be replaced with the version for this release.
      [None]:

请确保 **使用 https 地址** （例如 ``https://github.com/my_organization/my_repo.git``），而不是 ssh 地址。

.. _upstream-vcs-type:

上游 VCS 类型
^^^^^^^^^^^^^

这是 `上游仓库 URI`_ 所使用的版本控制系统（VCS）类型。
你必须指明你的仓库所使用的 vcs 类型，可选项为 ``svn``、``git``、``hg`` 或 ``tar``。

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

这是你要发布的软件包的版本。
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

把它设为 ``:{auto}`` （默认值，也是推荐的设置）将根据开发分支的 package.xml 自动确定版本。

把它设为 ``:{ask}`` 会在你每次用 bloom 发布时弹出提示询问版本。

.. _release-tag:

发布标签
^^^^^^^^

发布标签（Release Tag）指的是你想从哪个标签或分支导入代码。

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

把它设为 ``:{version}`` （默认值，也是推荐的设置）将使发布标签与版本标签保持一致。

一种不太常见的做法是把它设为某个分支名，以便在发布时始终从上游项目拉取该分支。

另外，如果你希望每次发布时都被提示输入一个不同的标签，可以输入 ``:{ask}``。
如果上游项目频繁地打标签发布，而你想在每次发布时都引用新的标签，那么 ``:{ask}`` 会很有用。

.. _upstream-devel-branch:

上游开发分支
^^^^^^^^^^^^

上游开发分支是你的 :ref:`上游仓库 <upstream-repository-uri>` 中分支的名称。
如果你为每个 ROS 发行版使用不同的分支，那么该字段在每个发布轨道中都会不同。
当 :ref:`版本 <version>` 设为 ``:{auto}`` 时，会用它来确定你要发布的软件包的版本。

.. code-block:: bash

   Upstream Devel Branch:
      <vcs reference>
         Branch in upstream repository on which to search for the version.
         This is used only when version is set to ':{auto}'.
      [None]:

要从名为 ``{DISTRO}`` 的分支发布，请输入 ``{DISTRO}``。
将其保留为 ``None`` 会导致版本从你仓库的默认分支来确定（不推荐这样做）。

.. _ros-distro:

ROS 发行版
^^^^^^^^^^

这是你计划将软件包发布到的发行版。

.. code-block:: bash

   ROS Distro:
      <ROS distro>
         This can be any valid ROS distro, e.g. indigo, kinetic, lunar, melodic
      ['indigo']:

如果你计划发布到 ROS {DISTRO}，请输入 ``{DISTRO}``。

.. _patches-directory:

补丁目录
^^^^^^^^

这是存放对发布内容所做任何额外补丁的目录。

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

为发布添加额外补丁是一项很少使用的功能。
对于几乎所有软件包，此项都应保留默认值 ``None``。

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

在大多数情况下都可以保留默认值。
