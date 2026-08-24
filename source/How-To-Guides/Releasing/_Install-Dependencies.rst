根据你的平台安装你在后续步骤中会用到的工具：

.. tabs::

   .. group-tab:: deb (e.g. Ubuntu)

      .. code-block:: console

         $ sudo apt install python3-bloom python3-catkin-pkg

   .. group-tab:: RPM (e.g. RHEL)

      .. code-block:: console

          $ sudo dnf install python3-bloom python3-catkin_pkg

   .. group-tab:: Other

      .. code-block:: console

         $ pip3 install -U bloom catkin_pkg

确保你已初始化 rosdep：

.. code-block:: console

    $ sudo rosdep init
    $ rosdep update

请注意，如果 ``rosdep init`` 命令过去已经初始化过，它可能会失败；这可以安全地忽略。
