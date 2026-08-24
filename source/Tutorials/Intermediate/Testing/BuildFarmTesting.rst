.. BuildFarmTesting:

使用 ROS 构建农场测试你的代码
=============================

`ROS 2 构建农场 <https://build.ros2.org/>`_ 非常强大。
除了创建二进制文件，它还会在 PR 合并之前，通过编译和运行你的 ROS 包的所有测试来测试拉取请求。

有四个先决条件。

 * GitHub 用户 `@ros-pull-request-builder <https://github.com/ros-pull-request-builder>`_ 必须能访问仓库。
 * GitHub 仓库必须设置好 webhooks。
 * `你的包必须在 rosdistro 中已索引 </How-To-Guides/Releasing/Index-Your-Packages>`
 * ``test_pull_requests`` 标志必须为 true。


GitHub 访问权限
---------------

你可以在 GitHub 组织级别给 PR Builder 访问权限，也可以只给单个 GitHub 仓库。

GitHub 组织
^^^^^^^^^^^

#. 打开 `https://github.com/orgs/%YOUR_ORG%/people <https://github.com/orgs/%YOUR_ORG%/people>`_
   （同时将 ``%YOUR_ORG%`` 替换为适当的组织）
#. 点击 ``Invite Member`` 并输入 ``ros-pull-request-builder``


GitHub 仓库
^^^^^^^^^^^

#. 打开 `https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/access <https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/access>`_
   （同时将 ``%YOUR_ORG%/%YOUR_REPO$`` 替换为适当的组织/仓库）
#. 点击 ``Add people`` 并输入 ``ros-pull-request-builder``
#. 为他们的角色选择 ``Admin`` 或 ``Write``。
   （参见下一节）


WebHooks
--------

如果你给 ``ros-pull-request-builder`` 授予完全的管理权限，它会自动设置 hooks。

或者，你可以通过只用 **write** 权限设置它们来避免需要完全的管理权限。

#. 打开 `https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/hooks/new <https://github.com/%YOUR_ORG%/%YOUR_REPO%/settings/hooks/new>`_)
#. 输入 ``"https://build.ros2.org/ghprbhook/`` 作为 Payload URL
#. 勾选以下选项：
    * Let me select individual events.
    * Issue comments
    * Pull requests


test_pull_requests
------------------

对于你希望进行拉取请求测试的每个 ROS distro，你必须在 `rosdistro <https://github.com/ros/rosdistro/>`_ 的适当部分中启用 ``test_pull_requests`` 标志。

 * **选项 1** - 你在运行 `bloom </How-To-Guides/Releasing/Releasing-a-Package>` 时可以选择打开拉取请求测试。
 * **选项 2** - 你可以**小心地**手动编辑 rosdistro 仓库中的适当文件，并创建一个新的拉取请求。
   `示例 <https://github.com/ros/rosdistro/blob/3c295f76b0755989e9ed526c0b5f28a5f6a94da3/rolling/distribution.yaml#L4708>`_。
   `在 REP 143 中记录 <http://docs.ros.org/en/independent/api/rep/html/rep-0143.html#distribution-file>`_。

注意，在拉取请求添加后，作业通常要到夜间 Jenkins 重新配置后才会创建。
