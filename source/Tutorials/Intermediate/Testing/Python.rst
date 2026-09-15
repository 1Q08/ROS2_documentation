.. TestingPython:

使用 Python 编写基本测试
========================

起点：我们假设你已经创建好了 :ref:`基本的 ament_python 软件包<CreatePkg>`，并想为其添加一些测试。

如果你使用的是 ament_cmake_python，请参阅 :doc:`ament_cmake_python 文档<../../../How-To-Guides/Ament-CMake-Python-Documentation>`，了解如何让测试可被发现。
测试的内容以及使用 ``colcon`` 调用测试的方式保持不变。

软件包设置
----------

setup.py
^^^^^^^^

你的 ``setup.py`` 必须在 ``setup(...)`` 调用中包含对 ``pytest`` 的测试依赖：

.. code-block:: python

    tests_require=['pytest'],

测试文件和文件夹
^^^^^^^^^^^^^^^^

你的测试代码需要放在软件包根目录下名为 ``tests`` 的文件夹中。

任何包含你想要运行的测试的文件都必须符合 ``test_FOO.py`` 的命名模式，其中 ``FOO`` 可以替换为任意内容。

示例软件包结构：
""""""""""""""""

.. code-block::

  awesome_ros_package/
    awesome_ros_package/
        __init__.py
        fozzie.py
    package.xml
    setup.cfg
    setup.py
    tests/
        test_init.py
        test_copyright.py
        test_fozzie.py


测试内容
--------

现在你可以尽情地编写测试。
关于 pytest 有 `大量资源 <https://docs.pytest.org>`__，但简而言之，你可以编写以 ``test_`` 为前缀的函数，并加入你想要的任何断言语句。


.. code-block:: python

  def test_math():
      assert 2 + 2 == 5   # This should fail for most mathematical systems

运行测试
--------

有关运行测试和检查测试结果的更多信息，请参阅 :doc:`关于如何从命令行运行测试的教程 <CLI>`。

特殊命令
--------

除了 :doc:`标准的 colcon 测试命令 <CLI>` 之外，你还可以在命令行上通过 ``--pytest-args`` 标志向 ``pytest`` 框架传递参数。
例如，你可以用以下方式指定要运行的函数名：


.. tabs::

  .. group-tab:: Linux/macOS

      .. code-block:: console

         $ colcon test --packages-select <name-of-pkg> --pytest-args -k name_of_the_test_function

  .. group-tab:: Windows

      .. code-block:: console

         $ colcon test --merge-install --packages-select <name-of-pkg> --pytest-args -k name_of_the_test_function

要在运行测试时查看 pytest 输出，请使用以下标志：

.. code-block:: console

  $ colcon test --event-handlers console_cohesion+
