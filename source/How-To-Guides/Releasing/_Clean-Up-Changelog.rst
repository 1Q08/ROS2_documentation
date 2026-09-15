在编辑器中打开所有 ``CHANGELOG.rst`` 文件。
你会看到 ``catkin_generate_changelog`` 已经根据提交信息自动生成了一个 forthcoming 小节：

.. code-block:: rst

   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   Changelog for package your_package
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Forthcoming
   -----------
   * you can modify this commit message
   * and this

请整理这份提交信息列表，简明扼要地说明自上次发布以来软件包发生的重要变化，然后 **提交所有 CHANGELOG.rst 文件。**
不要修改 ``Forthcoming`` 标题。
