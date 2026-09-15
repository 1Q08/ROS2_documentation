软件包的每一次发布都必须有一个比上一版本更高的唯一版本号。

运行：

.. code-block:: console

   $ catkin_prepare_release

它会执行以下操作：

#. 提升 ``package.xml`` 中的软件包版本
#. 将 ``CHANGELOG.rst`` 中的标题 ``Forthcoming`` 替换为 ``version (date)`` （例如 ``0.0.1 (2022-01-08)``）
#. 提交这些改动
#. 创建一个标签（例如 ``0.0.1``）
#. 将改动和标签推送到你的远程仓库

.. note::

   默认情况下，软件包的补丁版本号会递增，例如从 ``0.0.0`` 变为 ``0.0.1``。
   如果要改为递增次版本号或主版本号，请运行 ``catkin_prepare_release --bump minor`` 或 ``catkin_prepare_release --bump major``。
   更多细节请参见 ``catkin_prepare_release --help``。

.. note::

   如果你的仓库有严格的分支合并规则（例如 ``Require a pull request before merging``），你将需要为 ``catkin_prepare_release`` 生成的改动/标签创建一个拉取请求，然后再合并它，因为你无法直接推送到该分支。
   根据你仓库的拉取请求合并设置（例如压缩合并或变基合并），合并拉取请求可能会改变版本提交的 SHA。
   在这种情况下，你需要在合并后手动重新为版本提交打标签，以确保标签指向正确的提交。
