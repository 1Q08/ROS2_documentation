确保你拥有支持 ``UTF-8`` 的 locale。
如果你处于最小化环境（例如 docker 容器）中，locale 可能是像 ``C`` 这样的最小设置。
我们使用以下设置进行测试。
不过，即使你使用其他支持 UTF-8 的 locale，也应该没有问题。

.. code-block:: console

   $ locale  # check for UTF-8

   $ sudo dnf install langpacks-en glibc-langpack-en
   $ export LANG=en_US.UTF-8

   $ locale  # verify settings
