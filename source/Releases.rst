.. _Releases:

发行版
======

什么是发行版？
--------------

ROS 发行版是一组带有版本号的 ROS 软件包。
这类似于 Linux 发行版（例如 Ubuntu）。
ROS 发行版的目的在于，让开发者能够基于一个相对稳定的代码库进行开发，直到他们准备好将所有内容向前推进。
因此，一旦某个发行版发布，我们会尽量将对核心软件包（ros-desktop-full 下的所有内容）的更改限制在 bug 修复和非破坏性改进的范围内。
这通常适用于整个社区，但对于"更高层级"的软件包，规则不那么严格，因此避免破坏性更改的责任落在相应软件包的维护者身上。

.. _list_of_distributions:

发行版列表
----------

以下是当前和历史 ROS 2 发行版的列表。
表格中标记为蓝色的行是当前受支持的发行版。

.. toctree::
   :hidden:

   Releases/Release-Lyrical-Luth
   Releases/Release-Kilted-Kaiju
   Releases/Release-Jazzy-Jalisco
   Releases/Release-Humble-Hawksbill
   Releases/Release-Rolling-Ridley
   Releases/Development
   Releases/End-of-Life
   Releases/Release-Process

.. raw:: html

   <!--
     This CSS overrides the styles of certain rows to mark them blue, indicating they are supported releases.
     For the odd number rows, a line like the following must be used:

       .rst-content table.distros:not(.field-list) tr:nth-child(1) td {...}

     For the even number rows, a line like the following must be used:

       .rst-content tr:nth-child(2) {...}

     No other combination I've found has worked.  Yes, this is extremely fragile.  No, I don't understand
     why it is like this.
   -->
   <style>
     /* Targeting the cells and rows for the background and plain text */
    .rst-content table.distros:not(.field-list) tr:nth-child(1) td,
    .rst-content table.distros tr:nth-child(2),
    .rst-content table.distros:not(.field-list) tr:nth-child(3) td,
    .rst-content table.distros:not(.field-list) tr:nth-child(5) td {
      background-color: #22314E;
      color: white;
    }

    /* Targeting the links inside those specific rows to force them to be not-blue */
    .rst-content table.distros:not(.field-list) tr:nth-child(1) td a,
    .rst-content table.distros tr:nth-child(2) a,
    .rst-content table.distros:not(.field-list) tr:nth-child(3) td a,
    .rst-content table.distros:not(.field-list) tr:nth-child(3) td a {
      color: #B0B0B0 !important;
    }
   </style>

.. |rolling| image:: Releases/rolling-small.png
   :alt: Rolling logo

.. |lyrical| image:: Releases/lyrical-small.png
   :alt: Lyrical logo

.. |kilted| image:: Releases/kilted-small.png
   :alt: Kilted logo

.. |jazzy| image:: Releases/jazzy-small.png
   :alt: Jazzy logo

.. |iron| image:: Releases/iron-small.png
   :alt: Iron logo

.. |humble| image:: Releases/humble-small.png
   :alt: Humble logo

.. |galactic| image:: Releases/galactic-small.png
   :alt: Galactic logo

.. |foxy| image:: Releases/foxy-small.png
   :alt: Foxy logo

.. |eloquent| image:: Releases/eloquent-small.png
   :alt: Eloquent logo

.. |dashing| image:: Releases/dashing-small.png
   :alt: Dashing logo

.. |crystal| image:: Releases/crystal-small.png
   :alt: Crystal logo

.. |bouncy| image:: Releases/bouncy-small.png
   :alt: Bouncy logo

.. |ardent| image:: Releases/ardent-small.png
   :alt: Ardent logo

.. list-table::
   :class: distros
   :header-rows: 1
   :widths: 35 25 30 20 10

   * - 发行版
     - 发布日期
     - 徽标
     - EOL 日期
     - ROS 负责人
   * - :doc:`Lyrical Luth <Releases/Release-Lyrical-Luth>`
     - May 22, 2026
     - |lyrical|
     - May 2031
     - `Shane Loretz <https://github.com/sloretz>`_
   * - :doc:`Kilted Kaiju <Releases/Release-Kilted-Kaiju>`
     - May 23, 2025
     - |kilted|
     - December 2026
     - `Scott K Logan <https://github.com/cottsay>`_
   * - :doc:`Jazzy Jalisco <Releases/Release-Jazzy-Jalisco>`
     - May 23, 2024
     - |jazzy|
     - May 2029
     - `Marco A. Gutiérrez <https://github.com/marcoag>`_
   * - :doc:`Iron Irwini <Releases/Release-Iron-Irwini>`
     - May 23, 2023
     - |iron|
     - December 4, 2024
     - `Yadunund Vijay <https://github.com/Yadunund>`_
   * - :doc:`Humble Hawksbill <Releases/Release-Humble-Hawksbill>`
     - May 23, 2022
     - |humble|
     - May 2027
     - `Christophe Bédard <https://github.com/christophebedard>`_ / `Audrow Nash <https://github.com/audrow>`_
   * - :doc:`Galactic Geochelone <Releases/Release-Galactic-Geochelone>`
     - May 23, 2021
     - |galactic|
     - December 9, 2022
     - `Scott Logan <https://github.com/cottsay/>`_
   * - :doc:`Foxy Fitzroy <Releases/Release-Foxy-Fitzroy>`
     - June 5, 2020
     - |foxy|
     - June 20, 2023
     - `Jacob Perron <https://github.com/jacobperron>`_ / `Dharini Dutia <https://github.com/quarkytale>`_
   * - :doc:`Eloquent Elusor <Releases/Release-Eloquent-Elusor>`
     - November 22, 2019
     - |eloquent|
     - November 2020
     - `Michael Carroll <https://github.com/mjcarroll>`_
   * - :doc:`Dashing Diademata <Releases/Release-Dashing-Diademata>`
     - May 31, 2019
     - |dashing|
     - May 2021
     - `Steven! Ragnarök <https://github.com/nuclearsandwich>`_
   * - :doc:`Crystal Clemmys <Releases/Release-Crystal-Clemmys>`
     - December 14, 2018
     - |crystal|
     - December 2019
     - `Steven! Ragnarök <https://github.com/nuclearsandwich>`_
   * - :doc:`Bouncy Bolson <Releases/Release-Bouncy-Bolson>`
     - July 2, 2018
     - |bouncy|
     - July 2019
     - `Mikael Arguedas <https://github.com/mikaelarguedas>`_ / `Steven! Ragnarök <https://github.com/nuclearsandwich>`_
   * - :doc:`Ardent Apalone <Releases/Release-Ardent-Apalone>`
     - December 8, 2017
     - |ardent|
     - December 2018
     - `Steven! Ragnarök <https://github.com/nuclearsandwich>`_
   * - :doc:`beta3 <Releases/Beta3-Overview>`
     - September 13, 2017
     -
     - December 2017
     -
   * - :doc:`beta2 <Releases/Beta2-Overview>`
     - July 5, 2017
     -
     - September 2017
     -
   * - :doc:`beta1 <Releases/Beta1-Overview>`
     - December 19, 2016
     -
     - Jul 2017
     -
   * - :doc:`alpha1 - alpha8 <Releases/Alpha-Overview>`
     - August 31, 2015
     -
     - December 2016
     -

未来发行版
----------

有关即将推出的功能的详细信息，请参见 :doc:`路线图 <The-ROS2-Project/Roadmap>`。

每年 5 月 23 日（`世界海龟日 <https://www.worldturtleday.org/>`_）都会发布一个新的 ROS 2 发行版。

.. list-table::
   :class: future-distros
   :header-rows: 1
   :widths: 35 30 20 15

   * - 发行版
     - 发布日期
     - 徽标
     - EOL 日期
   * - :doc:`Makoa Mata-mata <Releases/Release-Makoa-Mata-mata>`
     - May 2027
     - TBD
     - Dec 2028


.. _rolling_distribution:

Rolling 发行版
--------------

:doc:`ROS 2 Rolling Ridley <Releases/Release-Rolling-Ridley>` 是 ROS 2 的滚动开发发行版。
它在 `REP 2002 <https://reps.openrobotics.org/rep-2002/>`_ 中有描述，并于 2020 年 6 月首次推出。

ROS 2 的 Rolling 发行版有两个用途：

1. 它是 ROS 2 未来稳定发行版的暂存区；
2. 它是最新开发版本的集合。

顾名思义，Rolling 会持续更新，并且**可能进行包含破坏性更改的就地更新**。
我们建议大多数人改用最新的稳定发行版（参见 :ref:`list_of_distributions`）。

发布到 Rolling 发行版中的软件包将自动发布到 ROS 2 未来的稳定发行版中。
将 :doc:`ROS 2 软件包 <../How-To-Guides/Releasing/Releasing-a-Package>` 发布到 Rolling 发行版，遵循与所有其他 ROS 2 发行版相同的流程。

跨发行版通信
------------

无法保证节点能够跨发行版进行通信。
例如，针对 Humble 构建并运行的节点，无法保证能与针对 Iron 构建并运行的节点正确通信。
这可能会也可能不会成功，但它不受支持，不应依赖。
请注意，:ref:`跨厂商（单一发行版）的通信同样无法保证 <different-middleware-vendors-cross-vendor-communication>`。
