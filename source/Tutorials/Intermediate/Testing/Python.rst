.. TestingPython:

使用 Python 编写基础测试
========================

起点：我们假设你已经设置好了一个 :ref:`基础的 ament_python 包<CreatePkg>`，并且你想向其中添加一些测试。

如果你使用的是 ament_cmake_python，请参阅 :doc:`ament_cmake_python 文档<../../../How-To-Guides/Ament-CMake-Python-Documentation>` 了解如何使测试可发现。
测试内容和用 ``colcon`` 调用保持不变。

包设置
------

setup.py
^^^^^^^^

你的 ``setup.py`` 必须在调用 ``setup(...)`` 时对 ``pytest`` 有一个测试依赖：

.. code-block:: python

    tests_require=['pytest'],

测试文件和文件夹
^^^^^^^^^^^^^^^^

你的测试代码需要放在包根目录下一个名为 ``tests`` 的文件夹中。

任何包含你想运行的测试的文件都必须具有 ``test_FOO.py`` 模式，其中 ``FOO`` 可以用任何东西替换。

示例包布局：
""""""""""""

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

你现在可以随心所欲地编写测试。
有 `大量关于 pytest 的资源 <https://docs.pytest.org>`__，但简而言之，你可以编写带有 ``test_`` 前缀的函数，并包含任何你喜欢的 assert 语句。


.. code-block:: python

  def test_math():
      assert 2 + 2 == 5   # This should fail for most mathematical systems

运行测试
--------

有关运行测试和检查测试结果的更多信息，请参阅 :doc:`关于如何从命令行运行测试的教程 <CLI>`。

特殊命令
--------

除了 :doc:`标准的 colcon 测试命令 <CLI>`，你还可以使用 ``--pytest-args`` 标志从命令行向 ``pytest`` 框架指定参数。
例如，你可以使用以下命令指定要运行的函数名称


.. tabs::

  .. group-tab:: Linux/macOS

      .. code-block:: console

         $ colcon test --packages-select <name-of-pkg> --pytest-args -k name_of_the_test_function

  .. group-tab:: Windows

      .. code-block:: console

         $ colcon test --merge-install --packages-select <name-of-pkg> --pytest-args -k name_of_the_test_function

要在运行测试时看到 pytest 输出，使用这些标志：

.. code-block:: console

  $ colcon test --event-handlers console_cohesion+
