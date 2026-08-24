.. warning::

   如果你的计算机上存在文件 ``~/.config/bloom``，那么你很可能之前已经做过这一步，因此应该跳过本节。

在发布过程中，会执行多次需要密码认证的 HTTPS Git 操作。
为了避免反复被要求输入密码，我们将设置一个 `个人访问令牌（PAT） <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_。
如果你的 GitHub 账户设置了多因素认证，你 **必须** 设置一个个人访问令牌。

按照以下步骤创建一个个人访问令牌：

#. 登录 GitHub 并前往 `Personal access tokens <https://github.com/settings/tokens>`_。
#. 点击 **Generate new token** 按钮。
#. 在下拉菜单中，选择 **Generate new token (classic)**
#. 将 **Note** 设置为类似 ``Bloom token`` 的内容。
#. 将 **Expiration** 设置为 **No expiration**。
#. 勾选 ``public_repo`` 和 ``workflow`` 复选框。
#. 点击 **Generate token** 按钮。

创建令牌后，你将返回到 *Personal access tokens* 页面。
**复制** 以绿色高亮显示的字母数字令牌。

将你的 GitHub 用户名和 PAT 保存到一个名为 ``~/.config/bloom`` 的新文件中，格式如下：

.. code-block:: text

   {
      "github_user": "<your-github-username>",
      "oauth_token": "<token-you-created-for-bloom>"
   }

在你的 ``~/.gitconfig`` 中配置，让 `ros2-gbp <https://github.com/ros2-gbp>`_ 下所有发布仓库都使用你的 GitHub 账户和 PAT：

.. code-block:: ini

    [credential "https://github.com/ros2-gbp"]
        username = x-access-token
        helper = "!f() { test \"$1\" = get && echo \"password=<token-you-created-for-bloom>\"; }; f"

你还可以为各个发布仓库使用不同的 GitHub 账户和 PAT：

.. code-block:: ini

    [credential "https://github.com/ros2-gbp/my_package-release.git"]
        username = x-access-token
        helper = "!f() { test \"$1\" = get && echo \"password=<other-token-you-created-for-bloom>\"; }; f"
