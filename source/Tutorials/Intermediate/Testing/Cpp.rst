.. TestingCpp:

使用 GTest 编写 C++ 基础测试
============================

起点：我们假设你已经设置好了一个 :ref:`基础的 ament_cmake 包<CreatePkg>`，并且你想向其中添加一些测试。

在本教程中，我们将使用 `gtest <https://google.github.io/googletest/primer.html>`__。

包设置
------

源代码
^^^^^^
我们将从一个名为 ``test/tutorial_test.cpp`` 的文件中的代码开始。

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
将以下行添加到 ``package.xml``

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

测试代码被包裹在 ``if/endif`` 块中，以避免尽可能不构建测试。
``ament_add_gtest`` 的功能很像 ``add_executable``，所以你需要像通常那样调用 ``target_include_directories`` 和 ``target_link_libraries``。
``target_link_libraries`` 调用被注释掉显示，因为 ``name_of_local_library`` 是一个占位符，仅当你的测试依赖于本包中构建的库时，取消注释它并用你 ``add_library()`` 调用中的实际目标名称替换 ``name_of_local_library``。


运行测试
--------

有关运行测试和检查测试结果的更多信息，请参阅 :doc:`关于如何从命令行运行测试的教程 <CLI>`。
