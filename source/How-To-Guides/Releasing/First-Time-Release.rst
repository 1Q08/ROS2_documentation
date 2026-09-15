首次发布
========

本指南说明如何发布你此前从未发布过的 ROS 2 软件包。
由于发布 ROS 软件包时可选项众多，本指南意在覆盖最常见的场景，并不涵盖所有边缘情况。

.. contents:: 目录
   :depth: 1
   :local:

成为发布团队的一员
------------------

你必须是某个 :ref:`发布团队 <what-is-a-release-team>` 的一员。
如果你还不是某个发布团队的成员，请按照下列之一操作：

* :ref:`加入发布团队 <join-a-release-team>`
* :ref:`建立新的发布团队 <start-a-new-release-team>`

创建新的发布仓库
----------------

发布软件包需要一个 :ref:`发布仓库 <what-is-a-release-repository>`。
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

使用以下命令为你仓库中的每个软件包生成一个 ``CHANGELOG.rst`` 文件：

.. code-block:: console

   $ catkin_generate_changelog --all

.. include:: _Clean-Up-Changelog.rst

提升软件包版本
--------------

.. include:: _Bump-Package-Version.rst

Bloom 发布
----------

运行以下命令，并将 ``my_repo`` 替换为你的仓库名称：

.. code-block:: console

  $ bloom-release --new-track --rosdistro {DISTRO} --track {DISTRO} my_repo

.. tip::

   * ``--new-track`` 告诉 bloom 创建一个新的 :ref:`轨道 <what-is-a-track>` 并对其进行配置。
   * ``--rosdistro {DISTRO}`` 表示本次发布针对 ``{DISTRO}`` 发行版
   * ``--track {DISTRO}`` 表示你希望轨道名称为 ``{DISTRO}``


系统会提示你输入信息以配置新轨道。
在如下常见场景中：

* 你的软件包位于名为 ``my_repo`` 的仓库中
* 你要发布的是名为 ``main`` 的分支
* 仓库托管在 GitHub 上，地址为 ``https://github.com/my_organization/my_repo.git``
* 你的发布仓库位于 ``https://github.com/ros2-gbp/my_repo-release.git``

你应当按如下方式回应这些提示：

.. list-table::
   :header-rows: 1
   :widths: 1 2

   * - 配置项
     - 取值
   * - :ref:`发布仓库 URL <release-repository-url>`
     - ``https://github.com/ros2-gbp/my_repo-release.git``
   * - :ref:`仓库名称 <repository-name>`
     - ``my_repo``
   * - :ref:`上游仓库 URI <upstream-repository-uri>`
     - ``https://github.com/my_organization/my_repo.git``
   * - :ref:`上游 VCS 类型 <upstream-vcs-type>`
     -
   * - :ref:`版本 <version>`
     -
   * - :ref:`发布标签 <release-tag>`
     -
   * - :ref:`上游开发分支 <upstream-devel-branch>`
     - ``main``
   * - :ref:`ROS 发行版 <ros-distro>`
     -
   * - :ref:`补丁目录 <patches-directory>`
     -
   * - :ref:`发布仓库推送 URL <release-repository-push-url>`
     -

.. note::

  表格中的空单元格表示应使用默认值。
  只需按 Enter 键回应提示即可。

Bloom 会自动为你向 `rosdistro <https://github.com/ros/rosdistro>`_ 创建一个拉取请求。

.. note::

  默认情况下，bloom 会发布源仓库中的所有软件包。
  若要针对某个特定的 ``{DISTRO}`` 有选择地阻止某些软件包的发布，请在发布仓库的 ``master`` 分支中添加 ``{DISTRO}.ignored`` 文件。
  在每个文件中，每行列出一个软件包名称，以阻止该软件包的发布。
  `rosidl-release <https://github.com/ros2-gbp/rosidl-release>`_ 仓库可作为此配置的有用参考。

后续步骤
--------

.. include:: _Next-Steps.rst
