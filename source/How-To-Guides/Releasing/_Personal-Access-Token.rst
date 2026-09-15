.. warning::

   如果你的计算机上已存在 ``~/.config/bloom`` 文件，说明你很可能以前做过这件事，因此应当跳过本小节。

在发布过程中，会执行多次需要密码认证的 HTTPS Git 操作。
为了避免反复被要求输入密码，这里会设置一个 `个人访问令牌（PAT） <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_。
如果你的 GitHub 账号启用了多重身份验证，那么你 **必须** 设置一个个人访问令牌。

请按以下步骤创建个人访问令牌：

#. 登录 GitHub 并打开 `Personal access tokens <https://github.com/settings/tokens>`_。
#. 点击 **Generate new token** 按钮。
#. 在下拉菜单中选择 **Generate new token (classic)**
#. 将 **Note** 设置为类似 ``Bloom token`` 的内容。
#. 将 **Expiration** 设置为 **No expiration**。
#. 勾选 ``public_repo`` 和 ``workflow`` 复选框。
#. 点击 **Generate token** 按钮。

创建令牌后，你会回到 *Personal access tokens* 页面。
**复制** 以绿色高亮显示的 **字母数字令牌**。

将你的 GitHub 用户名和 PAT 保存到一个名为 ``~/.config/bloom`` 的新文件中，格式如下：

.. code-block:: text

   {
      "github_user": "<your-github-username>",
      "oauth_token": "<token-you-created-for-bloom>"
   }

在你的 ``~/.gitconfig`` 中配置你的 GitHub 账号和 PAT，使其用于 `ros2-gbp <https://github.com/ros2-gbp>`_ 下的所有发布仓库：

.. code-block:: ini

    [credential "https://github.com/ros2-gbp"]
        username = x-access-token
        helper = "!f() { test \"$1\" = get && echo \"password=<token-you-created-for-bloom>\"; }; f"

你还可以为单个发布仓库使用不同的 GitHub 账号和 PAT：

.. code-block:: ini

    [credential "https://github.com/ros2-gbp/my_package-release.git"]
        username = x-access-token
        helper = "!f() { test \"$1\" = get && echo \"password=<other-token-you-created-for-bloom>\"; }; f"
