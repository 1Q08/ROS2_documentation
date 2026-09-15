.. BuildFarmTesting:

使用 ROS 构建农场测试你的代码
=============================

The `ROS 2 构建农场 <https://build.ros2.org/>`_ 功能非常强大。
除了生成二进制文件外，它还会在 PR 合并之前，通过编译并运行你的 ROS 软件包的所有测试来测试拉取请求。

有四个前提条件。

 * GitHub 用户 `@ros-pull-request-builder <https://github.com/ros-pull-request-builder>`_ 必须拥有该仓库的访问权限。
 * GitHub 仓库必须配置好 webhook。
 * `你的软件包必须被索引到 rosdistro 中 </How-To-Guides/Releasing/Index-Your-Packages>`
 * ``test_pull_requests`` 标志必须为 true。


GitHub 访问权限
---------------

你可以在 GitHub 组织级别授予 PR Builder 访问权限，也可以仅授予单个 GitHub 仓库。

GitHub 组织
^^^^^^^^^^^

#. 打开 `https://github.com/orgs/%YOUR_ORG%/people <https://github.com/orgs/%YOUR_ORG%/people>`_
   （并将 ``%YOUR_ORG%`` 替换为相应的组织）
#. 点击 ``Invite Member`` 并输入 ``ros-pull-request-builder``


GitHub 仓库
^^^^^^^^^^^

#. 打开 `https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/access <https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/access>`_
   （并将 ``%YOUR_ORG%/%YOUR_REPO$`` 替换为相应的组织/仓库）
#. 点击 ``Add people`` 并输入 ``ros-pull-request-builder``
#. 为其角色选择 ``Admin`` 或 ``Write``。
   （参见下一节）


Web 钩子
--------

如果你授予 ``ros-pull-request-builder`` 完整的管理员权限，它会自动设置这些钩子。

或者，你也可以只用 **write** 权限来设置它们，从而无需完整的管理员权限。

#. 打开 `https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/hooks/new <https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/hooks/new>`_）
#. 输入 ``"https://build.ros2.org/ghprbhook/`` 作为 Payload URL
#. 勾选以下选项：
    * Let me select individual events.
    * Issue comments
    * Pull requests


test_pull_requests
------------------

对于每个你想进行拉取请求测试的 ROS 发行版，你必须在 `rosdistro <https://github.com/ros/rosdistro/>`_ 的相应部分启用 ``test_pull_requests`` 标志。

 * **选项 1** - 在运行 `bloom </How-To-Guides/Releasing/Releasing-a-Package>` 时，你可以选择开启拉取请求测试。
 * **选项 2** - 你可以 **小心地** 手动编辑 rosdistro 仓库中的相应文件，并创建一个新的拉取请求。
   `示例 <https://github.com/ros/rosdistro/blob/3c295f76b0755989e9ed526c0b5f28a5f6a94da3/rolling/distribution.yaml#L4708>`_。
   `REP 143 中的文档 <http://docs.ros.org/en/independent/api/rep/html/rep-0143.html#distribution-file>`_。

请注意，在添加拉取请求后，通常要等到 nightly Jenkins 重新配置完成后才会创建该作业。
