请根据你的平台安装后续步骤中会用到的工具：

.. tabs::

   .. group-tab:: deb（例如 Ubuntu）

      .. code-block:: console

         $ sudo apt install python3-bloom python3-catkin-pkg

   .. group-tab:: RPM（例如 RHEL）

      .. code-block:: console

          $ sudo dnf install python3-bloom python3-catkin_pkg

   .. group-tab:: 其他

      .. code-block:: console

         $ pip3 install -U bloom catkin_pkg

请确认你已经初始化了 rosdep：

.. code-block:: console

    $ sudo rosdep init
    $ rosdep update

注意，如果过去已经初始化过，``rosdep init`` 命令可能会失败；这时可以安全地忽略该错误。
