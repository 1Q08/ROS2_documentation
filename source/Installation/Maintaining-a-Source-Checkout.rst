.. _MaintainingSource:

维护源码检出
============

.. ifconfig:: smv_current_version != '' and smv_current_version != 'rolling'

  .. note::

     有关维护 ROS 2 **最新开发版本** 源码检出的说明，请参阅
     `维护 ROS 2 Rolling 的源码检出 <../../rolling/Installation/Maintaining-a-Source-Checkout.html>`__

.. contents::
   :depth: 2
   :local:

如果你从源码安装了 ROS 2，那么自你检出源码以来，源代码可能已经发生了变化。
为了让你的源码检出保持最新，你需要定期更新 ``ros2.repos`` 文件、下载最新的源码并重新构建工作空间。

更新仓库列表
------------

每个 ROS 2 发行版都包含一个 ``ros2.repos`` 文件，其中列出了该发行版对应的仓库及其版本。


最新的 ROS 2 {DISTRO_TITLE} 分支
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你希望检出 ROS 2 {DISTRO_TITLE} 的最新代码，可以通过运行以下命令获取相关的仓库列表：

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

你会注意到，在 `ros2.repos <https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos>`__ 文件中，每个仓库都关联了一个 ``version``，它指向特定的提交哈希、标签或分支名。
由于这些版本可能引用了你本地仓库的旧副本无法识别的新标签/分支，因此你需要先更新已经检出的仓库，运行以下命令：

.. code-block:: console

   $ vcs custom --args remote update

下载新的源代码
--------------

现在你应该能够通过以下命令下载与新仓库列表相关的源码：

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

   In a Windows command line interface:

   .. code-block:: console

       $ vcs import --input ros2.repos src
       $ vcs pull src

   Or in powershell:

   .. code-block:: console

       $ vcs import --input ros2.repos src
       $ vcs pull src

重新构建你的工作空间
--------------------

现在工作空间已更新到最新源码，删除之前的安装并重新构建工作空间，例如：

.. code-block:: console

   $ colcon build --symlink-install

检查你的源码检出
----------------

在开发过程中，你的工作空间可能与导入仓库列表时的原始状态有所不同。
如果你想知道工作空间中各仓库的版本，可以使用以下命令导出这些信息：

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

这个 ``my_ros2.repos`` 文件随后可以分享给他人，以便他们复现你工作空间中仓库的状态。
