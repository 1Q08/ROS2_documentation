.. TestingCLI:

从命令行运行 ROS 2 中的测试
===========================

前提条件
^^^^^^^^

你需要一个已设置好的工作空间，其中包含带有测试的软件包。

构建并运行测试
^^^^^^^^^^^^^^

要编译并运行测试，只需在工作空间根目录下运行来自 ``colcon`` 的 `test <https://colcon.readthedocs.io/en/released/reference/verb/test.html>`__ 动词（verb）。

.. code-block:: console

  $ colcon test --ctest-args tests [package_selection_args]

其中 ``package_selection_args`` 是可选的软件包选择参数，用于让 ``colcon`` 限定要构建和运行哪些软件包。
更多信息请参阅 `colcon 关于软件包选择参数的文档 <https://colcon.readthedocs.io/en/released/reference/package-selection-arguments.html>`__

在测试之前，:ref:`加载工作空间 <colcon-tutorial-source-the-environment>` 应该不是必需的。
``colcon test`` 会确保测试在正确的环境中运行、能够访问其依赖项等等。

检查测试结果
^^^^^^^^^^^^

要查看结果，只需运行来自 ``colcon`` 的 `test-result <https://colcon.readthedocs.io/en/released/reference/verb/test-result.html>`__ 动词（verb）。

.. code-block:: console

  $ colcon test-result --all

要查看具体哪些测试用例失败，请使用 ``--verbose`` 标志：

.. code-block:: console

  $ colcon test-result --all --verbose

使用 GDB 调试测试
^^^^^^^^^^^^^^^^^

有关使用 GDB 调试测试的详细指导，请参阅 :doc:`GDB 教程 <../../../How-To-Guides/Getting-Backtraces-in-ROS-2>`。
