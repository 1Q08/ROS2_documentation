确保你有一个支持 ``UTF-8`` 的语言环境（locale）。
如果你处于最小化环境（例如 docker 容器），语言环境可能是 ``C`` 这样的最小设置。
我们使用以下设置进行测试。
不过，只要你使用其他支持 UTF-8 的语言环境，应该也没有问题。

.. code-block:: console

   $ locale  # check for UTF-8

   $ sudo dnf install langpacks-en glibc-langpack-en
   $ export LANG=en_US.UTF-8

   $ locale  # verify settings
