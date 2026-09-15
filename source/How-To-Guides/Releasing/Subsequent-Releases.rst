后续发布
========

本指南说明如何发布此前已经发布过的 ROS 软件包的新版本。

.. contents:: 目录
   :depth: 1
   :local:

成为发布团队的一员
------------------

如果你不是拥有发布仓库写权限的发布团队成员，请按照 :ref:`加入发布团队 <join-a-release-team>` 操作。

安装依赖
--------

.. include:: _Install-Dependencies.rst

设置个人访问令牌
----------------

.. include:: _Personal-Access-Token.rst

确保仓库是最新的
----------------

.. include:: _Ensure-Repositories-Are-Up-To-Date.rst

更新变更日志
------------

为了你的用户和开发者，请让变更日志保持简洁且及时更新。

.. code-block:: console

   $ catkin_generate_changelog

.. include:: _Clean-Up-Changelog.rst

提升软件包版本
--------------

.. include:: _Bump-Package-Version.rst

Bloom 发布
----------

运行以下命令，并将 ``my_repo`` 替换为你包含这些软件包的仓库名称：

.. code-block:: console

   $ bloom-release --rosdistro {DISTRO} my_repo

Bloom 会自动为你向 `rosdistro <https://github.com/ros/rosdistro>`_ 创建一个拉取请求。

.. note::

  默认情况下，bloom 会发布源仓库中的所有软件包。
  若要针对某个特定的 ``{DISTRO}`` 有选择地阻止某些软件包的发布，请在被阻止的发布仓库的 ``master`` 分支中添加 ``{DISTRO}.ignored`` 文件。
  在每个文件中，每行列出一个软件包名称，以阻止该软件包的发布。
  `rosidl-release <https://github.com/ros2-gbp/rosidl-release>`_ 仓库可作为此配置的有用参考。

后续步骤
--------

.. include:: _Next-Steps.rst
