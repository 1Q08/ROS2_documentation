.. TestingCpp:

使用 C++ 与 GTest 编写基本测试
==============================

起点：我们假设你已经创建好了 :ref:`基本的 ament_cmake 软件包<CreatePkg>`，并想为其添加一些测试。

在本教程中，我们将使用 `gtest <https://google.github.io/googletest/primer.html>`__。

软件包设置
----------

源代码
^^^^^^
我们先将代码放在名为 ``test/tutorial_test.cpp`` 的文件中

.. code-block:: c++

    #include <gtest/gtest.h>

    TEST(package_name, a_first_test)
    {
      ASSERT_EQ(4, 2 + 2);
    }

    int main(int argc, char ** argv)
    {
      testing::InitGoogleTest(&argc, argv);
      return RUN_ALL_TESTS();
    }


package.xml
^^^^^^^^^^^
将以下行添加到 ``package.xml`` 中

.. code-block:: c++

    <test_depend>ament_cmake_gtest</test_depend>

CMakeLists.txt
^^^^^^^^^^^^^^

.. code-block:: cmake

    if(BUILD_TESTING)
      find_package(ament_cmake_gtest REQUIRED)
      ament_add_gtest(${PROJECT_NAME}_tutorial_test test/tutorial_test.cpp)
      target_include_directories(${PROJECT_NAME}_tutorial_test PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
      )
      # target_link_libraries(${PROJECT_NAME}_tutorial_test name_of_local_library)
    endif()

测试代码被包裹在 ``if/endif`` 块中，以便尽可能避免构建测试。
``ament_add_gtest`` 的功能与 ``add_executable`` 类似，因此你需要像往常一样调用 ``target_include_directories`` 和 ``target_link_libraries``。
``target_link_libraries`` 调用被注释掉，是因为 ``name_of_local_library`` 是一个占位符；仅当你的测试依赖本软件包中构建的库时，才取消注释并将其替换为 ``add_library()`` 调用中实际的 target 名称。


运行测试
--------

有关运行测试和检查测试结果的更多信息，请参阅 :doc:`关于如何从命令行运行测试的教程 <CLI>`。
