.. redirect-from::

  Contributing/Build-Farms

.. _BuildFarms:

============
ROS 构建农场
============

.. contents:: 目录
   :depth: 1
   :local:

ROS 构建农场是支撑 ROS 生态系统的重要基础设施，由 `Open Robotics`_ 提供并维护。
它们为 ROS 1 和 ROS 2 软件包提供源码包与二进制包的构建、持续集成、测试与分析。
面向开源软件包有两个托管实例：

#. https://build.ros.org/ 用于 ROS 1 软件包
#. https://build.ros2.org/ 用于 ROS 2 软件包

如果你打算使用所提供的任何基础设施，请考虑订阅
`构建农场讨论论坛 <https://discourse.openrobotics.org/c/infrastructure-project/infra-buildfarm/20>`__ 以接收通知，
例如关于任何即将发生的更改的通知。


作业与部署
----------

ROS 构建农场执行若干种不同的作业。
对于每种作业类型，你都能找到关于它们做什么以及如何工作的详细说明：

* `release jobs`_ 生成二进制包，例如 deb 包
* `devel jobs`_ 以轮询方式构建并测试单个仓库内的 ROS 软件包
* `pull_request jobs`_ 由 webhook 触发，构建并测试单个仓库内的 ROS 软件包
* `CI jobs`_ 跨仓库构建并测试 ROS 软件包，并可选地使用其他 CI 作业的产物来加速构建
* `doc jobs`_ 生成软件包的 API 文档，并从清单中提取信息
* `miscellaneous jobs`_ 执行维护任务，并生成用于可视化构建农场及其产物状态的信息数据

创建与部署
..........

当软件包被 bloom 之后（即发布供 ROS 1 或 ROS 2 使用），上述作业会被创建和部署。
一旦 bloom 成功、软件包被纳入某个 ROS 发行版（通过对 rosdistro_ 的拉取请求），相应的作业就会被生成。
作业的名称编码了它们的类型和用途：[1]_

* release 作业：

   * ``{distro}src_{platf}__{package}__{platform}__source`` 构建发布的源码包
   * ``{distro}bin_{platf}__{package}__{platform}__binary`` 构建发布的二进制包

   例如，rclcpp 在 ROS 2 Iron 上（运行于 Ubuntu Jammy amd64）的二进制打包作业名为 ``Ibin_uJ64__rclcpp__ubuntu_jammy_amd64__binary``。

* devel 作业：

   * ``{distro}dev__{package}__{platform}`` 为用于发布的对应分支执行一次 CI 构建

* pull_request 作业

   * ``{distro}pr__{package}__{platform}`` 为某个拉取请求执行一次 CI 构建

   例如，rclcpp 在 ROS 2 Iron 上（运行于 Ubuntu Jammy amd64）的 PR 作业名为 ``Ipr__rclcpp__ubuntu_jammy_amd64``。

执行
....

作业的执行取决于作业的类型：

* `devel jobs`_ 会在每次向相应分支提交时，按照配置的频率轮询触发。
* `pull_request jobs`_ 由上游 [2]_ 仓库相应拉取请求的 webhook 触发
* `release jobs`_ 在每次发布新的软件包版本时触发一次，即为该软件包接受了一个新的
  rosdistro_ 拉取请求。
  源码作业由 rosdistro 发行版文件中的版本变更触发，二进制作业则由其对应的源码作业触发。


常见问题（FAQ）与故障排查
-------------------------

#. **我收到了构建农场作业失败产生的 Jenkins 邮件；我该怎么办？**

   前往触发该问题的作业。
   你可以在 Jenkins 邮件顶部找到链接。
   在通过链接进入构建作业后，点击左侧的 *Console Output*，然后点击 *Full Log*。
   这会给出失败构建的完整控制台输出。
   尝试找到最靠上的错误，因为它通常最重要，其他错误可能是它的连带结果。

   邮件末尾可能会写着
   ``'apt-src build [...]' failed. This is usually because of an error building the package.``
   这通常暗示存在缺失的依赖，参见第 2 条。

#. **我似乎缺少一个依赖，如何查明是哪一个？**

   你基本上有两种选择：
   选项 a 更简单，但可能需要反复迭代多次；
   选项 b 更繁琐，但能让你获得完整的信息并且可以在本地调试。

   a) 检查触发该问题的发布作业（见上一个问题），定位 cmake 依赖问题。
      为此，浏览到 cmake 部分，例如在 Ubuntu/Debian 构建作业的情况下，通过左侧菜单导航到 *build binarydeb*
      部分。
      *CMake Error* 通常会暗示 cmake 配置所要求但在 `package manifest`_ 中缺失的依赖。
      在清单中修复依赖后，对你的软件包做一次新的发布，然后等待构建农场的反馈，或者……
   b) 要获得完整信息并更快地在本地调试，你可以 `在本地运行发布作业 <run the release jobs locally_>`__。
      这让你可以在本地反复迭代清单，直到所有依赖都被修复。

#. **为什么 devel 作业 / 我的 github actions / 我的本地构建成功时，发布作业却失败了？**

   这可能有几个原因。
   首先，发布作业是针对一个最小化的 ROS 安装进行构建的，以检查所有依赖是否都已
   在 `package manifest`_ 中正确声明。
   devel 作业 / github actions / 本地构建可能
   是在已经安装了这些依赖的环境中执行的，因此不会
   注意到依赖问题。
   其次，它们构建的可能是不同版本的源代码。
   虽然 devel 作业 / github actions / 本地构建通常构建来自
   *upstream* [2]_ 仓库的最新版本，但 `release jobs`_ 构建的是最新发布的源代码，即 *release* 仓库 [3]_ 中相应 *upstream* 分支里的源代码。


延伸阅读
--------

以下链接提供了关于构建农场的更多细节和见解：

* https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/index.rst - 构建农场基础设施及所生成构建作业的通用
  文档
* http://wiki.ros.org/regression_tests#Setting_up_Your_Computer_for_Prerelease
* http://wiki.ros.org/buildfarm - ROS 1 构建农场的 ROS wiki 条目（部分内容已 *过时*）
* https://github.com/ros-infrastructure/cookbook-ros-buildfarm - 安装并配置 ROS 构建
  农场机器


.. [1] ``{distro}`` 是 ROS 发行版的首字母，``{platform}``（``{platf}``）
   表示软件包所针对构建的平台（及其短代码），``{package}`` 则是
   正在构建的 ROS 软件包名称。
.. [2] *upstream* 仓库是包含相应 ROS 1 / ROS 2 软件包原始源代码的仓库。
.. [3] *release* 仓库是 ROS 2 基础设施用于发布
   软件包的仓库，参见 https://github.com/ros2-gbp/。

.. _`release jobs`:
   https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/jobs/release_jobs.rst
.. _`devel jobs`:
   https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/jobs/devel_jobs.rst
.. _`pull_request jobs`:
   https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/jobs/devel_jobs.rst
.. _`CI jobs`:
   https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/jobs/ci_jobs.rst
.. _`doc jobs`:
   https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/jobs/doc_jobs.rst
.. _`miscellaneous jobs`:
   https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/jobs/miscellaneous_jobs.rst
.. _bloomed:
   http://wiki.ros.org/bloom
.. _rosdistro:
   https://github.com/ros/rosdistro
.. _`run the release jobs locally`:
   https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/jobs/release_jobs.rst#run-the-release-job-locally
.. _`Open Robotics`:
   https://www.openrobotics.org/
.. _`job descriptions above`:
   #jobs-and-deployment
.. _`package manifest`:
   http://wiki.ros.org/Manifest
