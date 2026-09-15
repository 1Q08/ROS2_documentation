.. redirect-from::

    Tutorials/Building-ROS2-Package-with-eclipse-2021-06

使用 Eclipse 2021-06 构建软件包
===============================

.. contents:: 目录
   :depth: 2
   :local:

你无法使用 eclipse 创建 ROS 2 软件包，需要使用命令行工具来创建。
请按照 :doc:`创建软件包 <../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>` 教程操作。

创建好项目后，你就可以编辑源代码并使用 eclipse 构建它。

我们启动 eclipse 并选择一个 eclipse-workspace。

.. image:: images/eclipse_work_dir.png
   :target: ../../_images/eclipse_work_dir.png
   :alt: eclipse_work_dir

我们创建一个 C++ 项目

.. image:: images/eclipse_create_c++_project.png
   :target: ../../_images/eclipse_create_c++_project.png
   :alt: eclipse_create_c++_project


.. image:: images/eclipse_c++_project_select_type.png
   :target: ../../_images/eclipse_c++_project_select_type.png
   :alt: eclipse_c++_project_select_type

可以看到我们已经有了 C++ 的 include 路径。

.. image:: images/eclipse_c++_project_includes.png
   :target: ../../_images/eclipse_c++_project_includes.png
   :alt: eclipse_c++_project_includes


现在我们导入自己的 ROS 2 项目。
代码仍然留在原来的位置。

.. image:: images/eclipse_import_project.png
   :target: ../../_images/eclipse_import_project.png
   :alt: eclipse_import_project

.. image:: images/eclipse_import_filesystem.png
   :target: ../../_images/eclipse_import_filesystem.png
   :alt: eclipse_import_filesystem


.. image:: images/eclipse_import_select_my_package.png
   :target: ../../_images/eclipse_import_select_my_package.png
   :alt: eclipse_import_select_my_package



我们在源代码中可以看到，C++ 的 include 已经解析成功，但 ROS 2 的还没有。

.. image:: images/eclipse_c++_wo_ros_includes.png
   :target: ../../_images/eclipse_c++_wo_ros_includes.png
   :alt: eclipse_c++_wo_ros_includes


.. image:: images/eclipse_c++_path_and_symbols.png
   :target: ../../_images/eclipse_c++_path_and_symbols.png
   :alt: eclipse_c++_path_and_symbols


.. image:: images/eclipse_c++_add_directory_path.png
   :target: ../../_images/eclipse_c++_add_directory_path.png
   :alt: eclipse_c++_add_directory_path


现在我们看到 ROS 2 的 include 也已经解析成功。

.. image:: images/eclipse_c++_indexer_ok.png
   :target: ../../_images/eclipse_c++_indexer_ok.png
   :alt: eclipse_c++_indexer_ok


添加 Builder colcon，这样我们就可以通过右键单击项目并选择 "Build project" 来构建。

.. image:: images/eclipse_c++_properties_builders.png
   :target: ../../_images/eclipse_c++_properties_builders.png
   :alt: eclipse_c++_properties_builders


.. image:: images/eclipse_c++_builder_main.png
   :target: ../../_images/eclipse_c++_builder_main.png
   :alt: eclipse_c++_builder_main


借助 PYTHONPATH，你也可以构建 Python 项目。

.. image:: images/eclipse_c++_builder_env.png
   :target: ../../_images/eclipse_c++_builder_env.png
   :alt: eclipse_c++_builder_env


.. image:: images/eclipse_c++_properties_builders_with_colcon.png
   :target: ../../_images/eclipse_c++_properties_builders_with_colcon.png
   :alt: eclipse_c++_properties_builders_with_colcon


右键单击该项目并选择 "Build Project"。

.. image:: images/eclipse_c++_build_project_with_colcon.png
   :target: ../../_images/eclipse_c++_build_project_with_colcon.png
   :alt: eclipse_c++_build_project_with_colcon
