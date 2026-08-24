在编辑器中打开所有 ``CHANGELOG.rst`` 文件。
你将看到 ``catkin_generate_changelog`` 已经根据提交消息自动生成了一个 forthcoming 部分：

.. code-block:: rst

   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   Changelog for package your_package
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Forthcoming
   -----------
   * you can modify this commit message
   * and this

清理提交消息列表，以简明扼要地传达自上次发布以来对包所做的值得注意的更改，并**提交所有 CHANGELOG.rst 文件。**
不要修改 ``Forthcoming`` 标题。
