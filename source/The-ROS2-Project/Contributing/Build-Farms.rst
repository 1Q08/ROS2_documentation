.. redirect-from::

  Contributing/Build-Farms

.. _BuildFarms:

============
ROS 构建农场
============

.. contents:: 目录
   :depth: 1
   :local:

ROS 构建农场是支持 ROS 生态的重要基础设施，由 `Open Robotics`_ 提供和维护。
它们为 ROS 1 和 ROS 2 软件包提供源码包和二进制包的构建、持续集成、测试和分析。
有两个面向开源软件包的托管实例：

#. https://build.ros.org/ 用于 ROS 1 软件包
#. https://build.ros2.org/ 用于 ROS 2 软件包

如果你打算使用所提供的任何基础设施，请考虑注册
`构建农场讨论论坛 <https://discourse.openrobotics.org/c/infrastructure-project/infra-buildfarm/20>`__，以便接收通知，
例如关于任何即将发生的更改的通知。


任务与部署
----------

ROS 构建农场执行若干种不同的任务。
对于每种任务类型，你都可以找到关于它们做什么以及如何工作的详细描述：

* `release jobs`_ 生成二进制软件包，例如 deb 软件包
* `devel jobs`_ 在单个仓库内按轮询方式构建和测试 ROS 软件包
* `pull_request jobs`_ 在单个仓库内由 webhook 触发构建和测试 ROS 软件包
* `CI jobs`_ 跨仓库构建和测试 ROS 软件包，可选择使用来自其他 CI 任务的制品来加速构建
* `doc jobs`_ 生成软件包的 API 文档并从 manifest 中提取信息
* `miscellaneous jobs`_ 执行维护任务并生成信息数据，以可视化构建农场及其生成制品的状态

创建与部署
...........

上述任务在软件包被 bloomed_（即为 ROS 1 或 ROS 2 发布）时创建和部署。
一旦 blooming 成功，并且某个软件包被纳入某个 ROS 发行版（通过向 rosdistro_ 提交 pull request），相应的任务就会产生。
任务的名称编码了它们的类型和用途：[1]_

* release jobs：

   * ``{distro}src_{platf}__{package}__{platform}__source`` 构建发布的源码软件包
   * ``{distro}bin_{platf}__{package}__{platform}__binary`` 构建发布的二进制软件包

   例如，rclcpp 在 ROS 2 Rolling 上（运行于 Ubuntu Noble amd64）的二进制打包任务名为 ``Rbin_uN64__rclcpp__ubuntu_noble_amd64__binary``。

* devel jobs：

   * ``{distro}dev__{package}__{platform}`` 为发布分支执行 CI 构建

* pull_request jobs

   * ``{distro}pr__{package}__{platform}`` 为 pull request 执行 CI 构建

   例如，rclcpp 在 ROS 2 Rolling 上（运行于 Ubuntu Noble amd64）的 PR 任务名为 ``Rpr__rclcpp__ubuntu_noble_amd64``。

执行
....

任务的执行取决于任务类型：

* `devel jobs`_ 将每次向相应分支提交时被触发，基于配置的频率轮询。
* `pull_request jobs`_ 将由上游 [2]_ 仓库相应 pull request 的 webhook 触发。
* `release jobs`_ 将在每次新软件包版本发布时触发一次，即该软件包的
  新的 rosdistro_ pull request 被接受时。
  源码任务由 rosdistro 发行版文件中的版本更改触发，二进制任务由其对应的源码任务触发。


常见问题 (FAQ) 与排障
---------------------

#. **我收到构建农场任务失败的 Jenkins 邮件；我该怎么做？**

   前往引发问题的任务。
   你可以在 Jenkins 邮件的顶部找到链接。
   进入构建任务的链接后，点击左侧的 *Console Output*，然后点击 *Full Log*。
   这将为你提供失败构建的完整控制台输出。
   尽量找出最顶层的错误，因为它通常最重要，而其他错误可能是后续错误。

   邮件底部可能会写
   ``'apt-src build [...]' failed. This is usually because of an error building the package.``
   这通常暗示缺少依赖，参见第 2 条。

#. **我似乎缺少某个依赖，如何找出是哪一个？**

   你基本上有两个选择：
   选项 a 更简单，但可能需要多次迭代；
   选项 b 更详尽，可以为你提供完整的信息以及本地调试。

   a) 检查引发问题的 release 任务（参见上一个问题）并定位 cmake 依赖问题。
      为此，浏览到 cmake 部分，例如在 Ubuntu/Debian 构建任务中通过左侧菜单导航到 *build binarydeb*
      部分。
      *CMake Error* 通常会提示某个 cmake 配置所需的依赖，但该依赖在 `package manifest`_ 中缺失。
      在 manifest 中修复依赖后，为你的软件包做一次新发布，并等待构建农场的反馈，或者……
   b) 为了获得完整信息和更快的本地调试，你可以 `在本地运行 release 任务 <run the release jobs locally>`_。
      这样可以在本地迭代 manifest，直到所有依赖都被修复。

#. **为什么 release 任务在 devel 任务 / 我的 github actions / 我的本地构建成功时会失败？**

   这有几个潜在原因。
   首先，release 任务针对最小化的 ROS 安装进行构建，以检查所有依赖是否都正确声明在 `package manifest`_ 中。
   Devel 任务 / github actions / 本地构建可能
   在已安装依赖的环境中执行，因此不会注意到依赖问题。
   其次，它们可能构建不同版本的源码。
   Devel 任务 / github actions / 本地构建通常构建来自
   *upstream* [2]_ 仓库的最新版本，而 `release jobs`_ 构建最新发布的源码，即相应 *release* 仓库 [3]_ 的 *upstream* 分支中的源码。


延伸阅读
--------

以下链接提供了关于构建农场的更多细节和见解：

* https://github.com/ros-infrastructure/ros_buildfarm/blob/master/doc/index.rst - 构建农场基础设施及所生成构建任务的一般文档
* http://wiki.ros.org/regression_tests#Setting_up_Your_Computer_for_Prerelease
* http://wiki.ros.org/buildfarm - ROS 1 构建农场的 ROS wiki 条目（部分 *已过时*）
* https://github.com/ros-infrastructure/cookbook-ros-buildfarm - 安装和配置 ROS 构建农场机器


.. [1] ``{distro}`` 是 ROS 发行版的首字母，``{platform}``（``{platf}``）
   指定为软件包构建的平台（及其短代码），``{package}`` 是
   正在构建的 ROS 软件包的名称。
.. [2] *upstream* 仓库是包含相应 ROS 1 / ROS 2 软件包原始源码的仓库。
.. [3] *release* 仓库是 ROS 2 基础设施用于发布软件包的仓库，
   参见 https://github.com/ros2-gbp/。

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
