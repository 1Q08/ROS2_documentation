首次发布
========

本指南解释如何发布你以前没有发布过的 ROS 2 包。
由于发布 ROS 包时有众多选项，本指南旨在覆盖最常见的场景，而不会涵盖每一个边角情况。

.. contents:: 目录
   :depth: 1
   :local:

加入发布团队
------------

你必须属于某个 :ref:`发布团队 <what-is-a-release-team>`。
如果你还不是发布团队的一员，请按照以下任一操作：

* :ref:`加入发布团队 <join-a-release-team>`
* :ref:`组建新发布团队 <start-a-new-release-team>`

创建新的发布仓库
----------------

发布包需要一个 :ref:`发布仓库 <what-is-a-release-repository>`。
请按照 :ref:`创建新的发布仓库 <create-a-new-release-repository>` 操作。

安装依赖
--------

.. include:: _Install-Dependencies.rst

设置个人访问令牌
----------------

.. include:: _Personal-Access-Token.rst

确保仓库是最新的
----------------

.. include:: _Ensure-Repositories-Are-Up-To-Date.rst

生成变更日志
------------

使用以下命令为你仓库中的每个包生成一个 ``CHANGELOG.rst`` 文件：

.. code-block:: console

   $ catkin_generate_changelog --all

.. include:: _Clean-Up-Changelog.rst

提升包的版本号
--------------

.. include:: _Bump-Package-Version.rst

Bloom 发布
----------

运行以下命令，将 ``my_repo`` 替换为你的仓库名称：

.. code-block:: console

  $ bloom-release --new-track --rosdistro {DISTRO} --track {DISTRO} my_repo

.. tip::

   * ``--new-track`` 告诉 bloom 创建一个新的 :ref:`track <what-is-a-track>` 并配置它。
   * ``--rosdistro {DISTRO}`` 表示此发布是针对 ``{DISTRO}`` 发行版的
   * ``--track {DISTRO}`` 表示你希望 track 名称为 ``{DISTRO}``


系统会提示你输入信息以配置新的 track。
在如下常见场景中：

* 你的包位于一个名为 ``my_repo`` 的仓库中
* 你正在发布一个名为 ``main`` 的分支
* 该仓库托管在 GitHub 上的 ``https://github.com/my_organization/my_repo.git``
* 你的发布仓库位于 ``https://github.com/ros2-gbp/my_repo-release.git``

你应该按如下方式回答提示：

.. list-table::
   :header-rows: 1
   :widths: 1 2

   * - Configuration
     - Value
   * - :ref:`Release Repository url <release-repository-url>`
     - ``https://github.com/ros2-gbp/my_repo-release.git``
   * - :ref:`Repository Name <repository-name>`
     - ``my_repo``
   * - :ref:`Upstream Repository URI <upstream-repository-uri>`
     - ``https://github.com/my_organization/my_repo.git``
   * - :ref:`Upstream VCS Type <upstream-vcs-type>`
     -
   * - :ref:`Version <version>`
     -
   * - :ref:`Release Tag <release-tag>`
     -
   * - :ref:`Upstream Devel Branch <upstream-devel-branch>`
     - ``main``
   * - :ref:`ROS Distro <ros-distro>`
     -
   * - :ref:`Patches Directory <patches-directory>`
     -
   * - :ref:`Release Repository Push URL <release-repository-push-url>`
     -

.. note::

  表格中的空单元格表示应使用默认值。
  只需按 Enter 键来回答提示即可。

Bloom 会自动为你针对 `rosdistro <https://github.com/ros/rosdistro>`_ 创建一个拉取请求。

.. note::

  默认情况下，bloom 会发布源仓库中的所有包。
  若要为特定的 ``{DISTRO}`` 有选择地阻止某些包的发布，请在发布仓库的 ``master`` 分支中添加 ``{DISTRO}.ignored`` 文件。
  在每个文件中，每行列出一个包的名称，以阻止该包的发布。
  `rosidl-release <https://github.com/ros2-gbp/rosidl-release>`_ 仓库可以作为此配置的有用参考。

后续步骤
--------

.. include:: _Next-Steps.rst
