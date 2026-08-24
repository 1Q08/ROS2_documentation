.. TestingCLI:

在 ROS 2 中从命令行运行测试
===========================

先决条件
^^^^^^^^

你需要一个已设置好、且包中包含测试的工作空间。

构建并运行你的测试
^^^^^^^^^^^^^^^^^^

要编译并运行测试，只需在工作空间的根目录从 ``colcon`` 运行 `test <https://colcon.readthedocs.io/en/released/reference/verb/test.html>`__ 动词。

.. code-block:: console

  $ colcon test --ctest-args tests [package_selection_args]

其中 ``package_selection_args`` 是 ``colcon`` 的可选包选择参数，用于限制构建和运行哪些包。
在 `colcon 关于包选择参数的文档 <https://colcon.readthedocs.io/en/released/reference/package-selection-arguments.html>`__ 中找到更多信息。

在测试之前 :ref:`source 工作空间 <colcon-tutorial-source-the-environment>` 应该不是必需的。
``colcon test`` 确保测试在正确的环境中运行，能访问它们的依赖等。

检查测试结果
^^^^^^^^^^^^

要查看结果，只需从 ``colcon`` 运行 `test-result <https://colcon.readthedocs.io/en/released/reference/verb/test-result.html>`__ 动词。

.. code-block:: console

  $ colcon test-result --all

要查看失败的精确测试用例，使用 ``--verbose`` 标志：

.. code-block:: console

  $ colcon test-result --all --verbose

使用 GDB 调试测试
^^^^^^^^^^^^^^^^^

有关使用 GDB 调试测试的详细指导，请参阅 :doc:`GDB 教程 <../../../How-To-Guides/Getting-Backtraces-in-ROS-2>`。
