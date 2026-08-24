包的每次发布都必须有一个高于上一次发布的唯一版本号。

运行：

.. code-block:: console

   $ catkin_prepare_release

该命令执行以下操作：

#. 在 ``package.xml`` 中增加包的版本号
#. 在 ``CHANGELOG.rst`` 中将标题 ``Forthcoming`` 替换为 ``version (date)``（例如 ``0.0.1 (2022-01-08)``）
#. 提交这些更改
#. 创建一个标签（例如 ``0.0.1``）
#. 将更改和标签推送到你的远程仓库

.. note::

   默认情况下，包的补丁版本号会被递增，例如从 ``0.0.0`` 到 ``0.0.1``。
   要改为递增次要版本或主要版本，请运行 ``catkin_prepare_release --bump minor`` 或 ``catkin_prepare_release --bump major``。
   更多详细信息，请参阅 ``catkin_prepare_release --help``。

.. note::

   如果你的仓库有诸如 ``Require a pull request before merging`` 之类的严格合并规则，你需要为 ``catkin_prepare_release`` 生成的更改/标签创建一个拉取请求并合并它，因为你无法直接推送到该分支。
   根据你仓库的拉取请求合并设置（例如 squash 合并或 rebase 合并），合并拉取请求可能会改变版本提交的 SHA。
   在这种情况下，你需要在合并后手动重新为版本提交打标签，以确保标签指向正确的提交。
