安装前置依赖
------------

安装 Chocolatey
^^^^^^^^^^^^^^^

Chocolatey 是 Windows 的一个包管理器，请按照它的安装说明进行安装：

https://chocolatey.org/install

你将使用 Chocolatey 来安装其他一些开发者工具。

安装 Python
^^^^^^^^^^^

打开命令提示符（Command Prompt），输入以下命令通过 Chocolatey 安装 Python：

.. code-block:: bash

   choco install -y python --version 3.8.3

.. note::

   Chocolatey 会将 Python 安装到 ``C:\Python38``，后续安装步骤默认它位于该位置。
   如果你把 Python 安装到了其他位置，必须将它复制或链接到该位置。

安装 Visual C++ 可再发行组件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

打开命令提示符，输入以下命令通过 Chocolatey 安装它们：

.. code-block:: bash

   choco install -y vcredist2013 vcredist140

安装 OpenSSL
^^^^^^^^^^^^

打开命令提示符，输入以下命令通过 Chocolatey 安装 OpenSSL：

.. code-block:: bash

  choco install -y openssl --version 1.1.1.2100

此命令设置一个跨会话持久保留的环境变量：

.. code-block:: bash

   setx /m OPENSSL_CONF "C:\Program Files\OpenSSL-Win64\bin\openssl.cfg"

你需要将 OpenSSL-Win64 的 bin 文件夹追加到 PATH 中。
你可以单击 Windows 图标，输入“Environment Variables”，然后单击“Edit the system environment variables”来完成。
在弹出的对话框中，单击“Environment Variables”，然后在底部窗格中单击“Path”，最后单击“Edit”并加入下面的路径。

* ``C:\Program Files\OpenSSL-Win64\bin\``

安装 Visual Studio
^^^^^^^^^^^^^^^^^^

安装 Visual Studio 2019。

如果你已经拥有 Visual Studio 2019 的付费版本（Professional、Enterprise），请跳过此步骤。

Microsoft 提供了一个名为 Community 的免费 Visual Studio 2019 版本，可用于构建使用 ROS 2 的应用程序。
`你可以通过此链接直接下载安装程序。 <https://aka.ms/vs/16/release/vs_community.exe>`_

确保安装了 Visual C++ 相关功能。

确保它们已安装的简便方法是，在安装时选择 ``Desktop development with C++`` 工作负载。

   .. image:: /Installation/images/windows-vs-studio-install.png

请在待安装组件列表中取消勾选 C++ CMake 工具，确保没有安装它们。

安装 OpenCV
^^^^^^^^^^^

部分示例需要安装 OpenCV。

你可以从 `这里 <https://github.com/ros2/ros2/releases/download/opencv-archives/opencv-3.4.6-vc16.VS2019.zip>`__ 下载预编译版本的 OpenCV ``3.4.6``。

假设你将它解压到了 ``C:\opencv``，请在命令提示符中输入以下命令（需要管理员权限）：

.. code-block:: bash

   setx /m OpenCV_DIR C:\opencv

由于你使用的是预编译的 ROS 版本，我们必须告诉它在哪里找到 OpenCV 库。
你需要将 ``PATH`` 变量扩展到 ``C:\opencv\x64\vc16\bin``。

安装依赖项
^^^^^^^^^^

有一些依赖项在 Chocolatey 软件包数据库中不可用。
为了简化手动安装过程，我们提供了所需的 Chocolatey 软件包。

由于一些 chocolatey 软件包依赖它，我们先安装 CMake

.. code-block:: bash

   choco install -y cmake

你需要将 CMake 的 bin 文件夹 ``C:\Program Files\CMake\bin`` 追加到 PATH 中。

请从 `这个 <https://github.com/ros2/choco-packages/releases/latest>`__ GitHub 仓库下载这些软件包。

* ``asio.1.12.1.nupkg``
* ``bullet.3.17.nupkg``
* ``cunit.2.1.3.nupkg``
* ``eigen.3.3.4.nupkg``
* ``tinyxml-usestl.2.6.2.nupkg``
* ``tinyxml2.6.0.0.nupkg``

下载完这些软件包后，打开一个管理员权限的 shell 并执行以下命令：

.. code-block:: bash

   choco install -y -s <PATH\TO\DOWNLOADS\> asio cunit eigen tinyxml-usestl tinyxml2 bullet

请将 ``<PATH\TO\DOWNLOADS>`` 替换为你下载软件包的文件夹。

首先升级 pip 和 setuptools：

.. code-block:: bash

   python -m pip install -U pip setuptools==59.6.0

现在安装一些额外的 python 依赖项：

.. code-block:: bash

   python -m pip install -U catkin_pkg cryptography empy==3.3.4 importlib-metadata lark==1.1.1 lxml matplotlib netifaces numpy opencv-python PyQt5 pillow psutil pycairo pydot pyparsing==2.4.7 pyyaml rosdistro

安装 Qt5
^^^^^^^^

从 Qt 官网下载 `5.12.X 离线安装程序 <https://www.qt.io/offline-installers>`_。
运行安装程序。
确保在 ``Qt`` -> ``Qt 5.12.12`` 树下选择 ``MSVC 2017 64-bit`` 组件。

最后，在一个管理员权限的 ``cmd.exe`` 窗口中设置这些环境变量。
下面的命令假设你将它安装到了默认位置 ``C:\Qt``。

.. code-block:: bash

   setx /m Qt5_DIR C:\Qt\Qt5.12.12\5.12.12\msvc2017_64
   setx /m QT_QPA_PLATFORM_PLUGIN_PATH C:\Qt\Qt5.12.12\5.12.12\msvc2017_64\plugins\platforms


.. note::

   此路径可能会因所安装的 MSVC 版本、Qt 的安装目录以及所安装的 Qt 版本而变化。

RQt 依赖项
^^^^^^^^^^

要运行 rqt_graph，你需要 `下载 <https://graphviz.gitlab.io/_pages/Download/Download_windows.html>`__ 并安装 `Graphviz <https://graphviz.gitlab.io/>`__。
安装程序会询问是否将 graphviz 添加到 PATH，请选择将其添加到当前用户或所有用户。
