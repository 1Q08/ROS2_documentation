.. _MaintainingSource:

维护源代码检出
==============

.. ifconfig:: smv_current_version != '' and smv_current_version != 'rolling'

  .. note::

     有关维护 ROS 2 **最新开发版本** 的源代码检出的说明，请参阅
     `维护 ROS 2 Rolling 的源代码检出 <../../rolling/Installation/Maintaining-a-Source-Checkout.html>`__

.. contents::
   :depth: 2
   :local:

如果你从源代码安装了 ROS 2，那么自你检出源代码以来，源代码可能已经发生了更改。
为了使你的源代码检出保持最新，你需要定期更新你的 ``ros2.repos`` 文件、下载最新的源代码，并重新构建你的工作空间。

更新你的仓库列表
----------------

每个 ROS 2 版本都包含一个 ``ros2.repos`` 文件，其中列出了该版本的仓库及其版本。


最新的 ROS 2 {DISTRO_TITLE} 分支
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你想检出 ROS 2 {DISTRO_TITLE} 的最新代码，可以通过运行以下命令获取相应的仓库列表：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ cd ~/ros2_{DISTRO}
       $ mv -i ros2.repos ros2.repos.old
       $ wget https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos

  .. group-tab:: macOS

    .. code-block:: console

       $ cd ~/ros2_{DISTRO}
       $ mv -i ros2.repos ros2.repos.old
       $ wget https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos

  .. group-tab:: Windows

    使用 Windows 命令行界面：

    .. code-block:: console

       $ cd \dev\ros2_{DISTRO}
       $ curl -sk https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos -o ros2.repos

    或者使用 powershell：

    .. code-block:: console

       $ cd \dev\ros2_{DISTRO}
       $ curl https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos -o ros2.repos


更新你的仓库
------------

你会注意到，在 `ros2.repos <https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos>`__ 文件中，每个仓库都有一个与之关联的 ``version``，它指向特定的提交哈希、标签或分支名。
这些版本可能指向新的标签/分支，而你的本地仓库副本由于已过时而无法识别它们。
因此，你应该使用以下命令更新已经检出的仓库：

.. code-block:: console

   $ vcs custom --args remote update

下载新的源代码
--------------

现在，你应该能够使用以下命令下载与新仓库列表关联的源代码：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ vcs import src < ros2.repos
       $ vcs pull src

  .. group-tab:: macOS

    .. code-block:: console

       $ vcs import src < ros2.repos
       $ vcs pull src

  .. group-tab:: Windows

   在 Windows 命令行界面中：

   .. code-block:: console

       $ vcs import --input ros2.repos src
       $ vcs pull src

   或者在 powershell 中：

   .. code-block:: console

       $ vcs import --input ros2.repos src
       $ vcs pull src

重新构建你的工作空间
--------------------

现在工作空间已经与最新源代码保持同步，请移除之前的安装并重新构建你的工作空间，例如：

.. code-block:: console

   $ colcon build --symlink-install

检查你的源代码检出
------------------

在开发过程中，你可能已经偏离了导入仓库列表时工作空间的原始状态。
如果你想知道工作空间中这组仓库的版本，可以使用以下命令导出这些信息：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ cd ~/ros2_{DISTRO}
       $ vcs export src > my_ros2.repos

  .. group-tab:: macOS

    .. code-block:: console

       $ cd ~/ros2_{DISTRO}
       $ vcs export src > my_ros2.repos

  .. group-tab:: Windows

    .. code-block:: console

       $ cd \dev\ros2_{DISTRO}
       $ vcs export src > my_ros2.repos

然后，可以将这个 ``my_ros2.repos`` 文件分享给其他人，以便他们能够重现你工作空间中仓库的状态。
