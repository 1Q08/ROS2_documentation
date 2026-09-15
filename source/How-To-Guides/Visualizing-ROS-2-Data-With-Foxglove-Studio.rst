使用 Foxglove Studio 可视化 ROS 2 数据
======================================

`Foxglove Studio <https://foxglove.dev/studio>`__ 是一款开源的可视化与调试工具，用于处理你的机器人数据。

它提供了多种使用方式，尽可能方便开发——既可以作为独立的桌面应用运行，也可以通过浏览器访问，甚至可以在你自己的域名上自行托管。

在 `GitHub <https://www.github.com/foxglove/studio>`__ 上查看源代码。

安装
----

要使用 Web 应用，只需打开 Google Chrome 并访问 `studio.foxglove.dev <https://studio.foxglove.dev>`__。

要在 Linux、macOS 或 Windows 上使用桌面应用，请直接从 `Foxglove Studio 网站 <https://foxglove.dev/download>`__ 下载。

连接到数据源
------------

打开 Foxglove Studio 后，你会看到一个对话框，其中列出了 `所有可能的数据源 <https://foxglove.dev/docs/studio/connection/data-sources>`__。

要连接到你的 ROS 2 系统，请点击 “Open connection”，选择 “Rosbridge (ROS 1 & 2)” 选项卡，并配置你的 “WebSocket URL”。

你也可以把任何本地 ROS 2 ``.db3`` 文件直接拖放到应用程序中，以便加载并回放它们。

.. note::

  为了 `在 ROS 2 文件中加载自定义消息定义 <https://github.com/ros2/rosbag2/issues/782>`__，可以尝试将它们转换为 `MCAP 文件格式 <https://mcap.dev>`__。

更多详细说明请查看 `Foxglove Studio 文档 <https://foxglove.dev/docs/studio/connection/native>`__。

使用面板构建布局
----------------

`面板 <https://foxglove.dev/docs/studio/panels/introduction>`__ 是模块化的可视化界面，可以配置并排列成 Studio 的 `布局 <https://foxglove.dev/docs/studio/layouts>`__。
你还可以保存布局以便将来使用，供自己参考，或与更大的机器人团队共享。

在侧边栏的 “Add panel” 选项卡中可以找到所有可用面板的完整列表。

下面我们重点介绍几个特别有用的面板：

1 3D：在 3D 场景中显示可视化标记
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

向 3D 面板的场景发布标记消息，可以添加基本形状（箭头、球体等）以及更复杂的可视化内容（占据栅格、点云等）。

通过左侧的话题选择器选择要显示的话题，并在 “Edit topic settings” 菜单中配置每个话题的可视化设置。

.. image:: foxglove-studio/3d.png
  :width: 500 px
  :alt: Foxglove Studio's 3D panel

有关 `支持的消息类型 <https://foxglove.dev/docs/studio/panels/3d#supported-messages>`__ 的完整列表以及一些有用的 `用户交互 <https://foxglove.dev/docs/studio/panels/3d#user-interactions>`__，请参阅 `文档 <https://foxglove.dev/docs/studio/panels/3d>`__。

2 诊断：筛选并排序诊断消息
^^^^^^^^^^^^^^^^^^^^^^^^^^

在实时数据流中显示具有 ``diagnostic_msgs/msg/DiagnosticArray`` 数据类型的话题中所看到的节点状态（即 stale、error、warn 或 OK），并显示给定 ``diagnostic_name/hardware_id`` 的诊断数据。

.. image:: foxglove-studio/diagnostics.png
  :width: 500 px
  :alt: Foxglove Studio's Diagnostics panel

更多细节请参阅 `文档 <https://foxglove.dev/docs/studio/panels/diagnostics>`__。

3 图像：查看摄像头图像
^^^^^^^^^^^^^^^^^^^^^^

选择一个 ``sensor_msgs/msg/Image`` 或 ``sensor_msgs/msg/CompressedImage`` 话题进行显示。

.. image:: foxglove-studio/image.png
  :width: 500 px
  :alt: Foxglove Studio's Image panel

更多细节请参阅 `文档 <https://foxglove.dev/docs/studio/panels/image>`__。

4 日志：查看日志消息
^^^^^^^^^^^^^^^^^^^^

要实时查看 ``rcl_interfaces/msg/Log`` 消息，请使用桌面应用 `连接 <https://foxglove.dev/docs/studio/connection/native>`__ 到你正在运行的 ROS 系统。
要查看预先录制的数据文件中的 ``rcl_interfaces/msg/Log`` 消息，你可以把文件拖放到 `Web <https://studio.foxglove.dev>`__ 或桌面应用中。

接下来，向你的布局中添加一个 `Log <https://foxglove.dev/docs/studio/panels/log>`__ 面板。
如果你已正确连接到 ROS 系统，现在应该能看到日志消息列表，并可以按节点名称或严重级别进行筛选。

更多细节请参阅 `文档 <https://foxglove.dev/docs/studio/panels/log>`__。

5 绘图：绘制任意值随时间的变化
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

按回放时间绘制来自话题消息路径的任意值。

指定你想要在 y 轴上绘制的那些话题值。
对于 x 轴，可以选择绘制 y 轴值的时间戳、元素索引，或另一个自定义话题消息路径。

.. image:: foxglove-studio/plot.png
  :width: 500 px
  :alt: Foxglove Studio's Plot panel

更多细节请参阅 `文档 <https://foxglove.dev/docs/studio/panels/plot>`__。

6 原始消息：查看传入的话题消息
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以易读的可折叠 JSON 树格式显示传入的话题数据。

.. image:: foxglove-studio/raw-messages.png
  :width: 500 px
  :alt: Foxglove Studio's Raw Messages panel

更多细节请参阅 `文档 <https://foxglove.dev/docs/studio/panels/raw-messages>`__。

7 遥控：遥控你的机器人
^^^^^^^^^^^^^^^^^^^^^^

通过在给定话题上发布 ``geometry_msgs/msg/Twist`` 消息并发送回你正在运行的 ROS 系统，来遥控你的实体机器人。

.. image:: foxglove-studio/teleop.png
  :width: 300 px
  :alt: Foxglove Studio's URDF Viewer panel

更多细节请参阅 `文档 <https://foxglove.dev/docs/studio/panels/teleop>`__。

8 URDF 查看器：查看并操作你的 URDF 模型
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

要在 Foxglove Studio 中可视化并控制你的机器人模型，请打开 Web 或桌面应用，并向你的布局中添加一个 `URDF Viewer <https://foxglove.dev/docs/studio/panels/urdf-viewer>`__ 面板。
然后，把你的 URDF 文件拖放到该面板中即可可视化你的机器人模型。

.. image:: foxglove-studio/urdf.png
  :width: 300 px
  :alt: Foxglove Studio's URDF Viewer panel

选择任何发布 ``JointState`` 消息的话题，即可根据发布的关节状态更新可视化（默认为 ``/joint_states``）。

切换到 “Manual joint control”，使用提供的控件设置关节位置。

.. image:: foxglove-studio/urdf-joints.png
  :width: 500 px
  :alt: Foxglove Studio's URDF Viewer panel with editable joint positions

更多细节请参阅 `文档 <https://foxglove.dev/docs/studio/panels/urdf-viewer>`__。

其他基本操作
------------

1 查看你的 ROS 计算图
^^^^^^^^^^^^^^^^^^^^^

`使用桌面应用 <https://foxglove.dev/download>`__，`连接 <https://foxglove.dev/docs/studio/connection/native>`__ 到你正在运行的 ROS 系统。
接下来，向你的布局中添加一个 `Topic Graph <https://foxglove.dev/docs/studio/panels/topic-graph>`__ 面板。
如果你已正确连接到 ROS 系统，现在应该能在该面板中看到由 ROS 节点、话题和服务构成的计算图。
使用面板右侧的控件可以选择要显示哪些话题，或切换服务的显示。

2 查看并编辑你的 ROS 参数
^^^^^^^^^^^^^^^^^^^^^^^^^

`使用桌面应用 <https://foxglove.dev/download>`__，`连接 <https://foxglove.dev/docs/studio/connection/native>`__ 到你正在运行的 ROS 系统。
接下来，向你的布局中添加一个 `Parameters <https://foxglove.dev/docs/studio/panels/parameters>`__ 面板。
如果你已正确连接到 ROS 系统，现在应该能看到当前 ``rosparams`` 的实时视图。
你可以编辑这些参数值，把 ``rosparam`` 更新发布回你的 ROS 系统。

3 把消息发布回你正在运行的 ROS 系统
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`使用桌面应用 <https://foxglove.dev/download>`__，`连接 <https://foxglove.dev/docs/studio/connection/native>`__ 到你正在运行的 ROS 系统。
接下来，向你的布局中添加一个 `Publish <https://foxglove.dev/docs/studio/panels/publish>`__ 面板。

指定你想要发布的话题，以推断其数据类型，并在文本字段中填入 JSON 消息模板。

在常见 ROS 数据类型的下拉列表中选择一个数据类型，同样会在文本字段中填入 JSON 消息模板。

在点击 “Publish” 之前，编辑该模板以自定义你的消息。

.. image:: foxglove-studio/publish.png
  :width: 300 px
  :alt: Foxglove Studio's Publish panel
