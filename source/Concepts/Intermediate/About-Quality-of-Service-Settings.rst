.. redirect-from::

    About-Quality-of-Service-Settings
    Concepts/About-Quality-of-Service-Settings

服务质量设置
============

.. contents:: 目录
   :local:

概述
----

ROS 2 提供了丰富多样的服务质量（QoS）策略，以便开发者调优节点之间的通信。
通过合适的服务质量策略，ROS 2 可以像 TCP 一样可靠，也可以像 UDP 一样尽力而为，之间存在大量可能的状态组合。
与主要只支持 TCP 的 ROS 1 不同，ROS 2 受益于底层 DDS 传输在有损无线网络环境中的灵活性，那里更适合使用“尽力而为”策略；在实时计算系统中，配合合适的服务质量配置文件以满足时限要求也很关键。

一组 QoS “策略”组合起来形成一个 QoS “配置文件”。
考虑到为特定场景选择正确 QoS 策略的复杂性，ROS 2 提供了一组预定义的 QoS 配置文件，用于常见场景（例如传感器数据）。
同时，开发者也能自由控制 QoS 配置文件中的特定策略。

QoS 配置文件可以为发布者、订阅者、服务端和客户端指定。
一个 QoS 配置文件可以分别应用到上述实体的每个实例，但如果使用不同的配置文件，就可能导致它们不兼容，从而阻止消息传递。

.. _about_qos_policies:

QoS 策略
--------

当前的基础 QoS 配置文件包含以下策略设置：

* History

  * *Keep last*：仅保留最多 N 个样本，可通过队列深度选项进行配置。
  * *Keep all*：保存所有样本，但受底层中间件配置资源限制约束。

* Depth

  * *Queue size*：仅当“history”策略被设置为“keep last”时才生效。

* Reliability

  * *Best effort*：尽量传递样本，但如果网络不可靠，可能会丢失。
  * *Reliable*：保证样本会被传送，可能会重试多次。

* Durability

  * *Transient local*：发布者负责为“后加入”订阅者保留样本。
  * *Volatile*：不尝试保存样本。

* Deadline

  * *Duration*：在话题上后续消息发布之间期待的最大时间间隔。

* Lifespan

  * *Duration*：从发布到消息被接收之间允许的最大时间间隔，超过后会视为陈旧或过期（过期消息会被静默丢弃，且实际上永远不会被接收）。

* Liveliness

  * *Automatic*：当任意一个发布者发布一条消息后，系统会把该节点的所有发布者视为再活跃一个“租期持续时间”。
  * *Manual by topic*：如果发布者通过发布者 API 手动声明它仍然存活，系统会视其活跃另一个“租期持续时间”。

* Lease Duration

  * *Duration*：发布者表明它还活着前允许的最长时间；超出后系统会认为发布者失去活性（活性丢失可能表示出现故障）。

对于非持续时间类型的策略，还存在“system default”选项，表示使用底层中间件默认值。
对于持续时间类型的策略，还存在“default”选项，表示持续时间未指定，底层中间件通常会把它解释为无限长时间。

与 ROS 1 的比较
^^^^^^^^^^^^^^^

ROS 2 中的“history”和“depth”策略组合起来的功能类似于 ROS 1 中的队列长度。

ROS 2 中的“reliability”策略类似于 ROS 1 中的“best effort”（仅在 ``roscpp`` 中使用 UDPROS）或 “reliable”（TCPROS，ROS 1 默认）。
不过需要注意，ROS 2 中的可靠策略底层仍使用 UDP，这使其在适当时也支持多播。

ROS 2 中的“durability”策略“transient local”结合任意深度，功能类似于 ROS 1 中的“latching”发布者。
ROS 2 中其余策略都不是 ROS 1 中可用的任何类似能力，这意味着 ROS 2 在这方面更强大。
未来，ROS 2 可能会拥有更多 QoS 策略。


QoS 配置文件
------------

配置文件允许开发者把精力集中在应用逻辑上，而无需担心所有可能的 QoS 设置。
一个 QoS 配置文件定义了一组预期能很好配合特定用例的策略。

当前定义的 QoS 配置文件有：

* 发布者与订阅者的默认 QoS 设置

  为了更容易从 ROS 1 迁移到 ROS 2，保持相似的网络行为是可取的。
  默认情况下，ROS 2 中的发布者和订阅者在历史记录上使用 “keep last”，队列大小为 10；可靠性使用 “reliable”；耐久性使用 “volatile”；活性使用 “system default”。
  截止时间、生命周期和租期持续时间也都设置为 “default”。

* 服务

  与发布者和订阅者类似，服务也应可靠。
  服务尤其要使用 volatile 耐久性，否则重启后的服务端可能收到过时请求。
  虽然客户端可以避免收到多个响应，但服务端无法避免接收过时请求带来的副作用。

* 传感器数据

  对于传感器数据，通常更重要的是尽快接收读数，而不是确保所有读数都到达。
  也就是说，开发者希望一旦捕获到最新样本就立即接收，而不必关心部分样本丢失。
  因此，传感器数据配置文件使用尽力而为的可靠性和较小的队列大小。

* 参数

  ROS 2 中的参数基于服务，因此它们具有相似的配置文件。
  区别在于参数使用更大的队列深度，以防请求在参数客户端无法访问参数服务端时丢失。

* 系统默认

  该配置文件使用 RMW 实现的默认策略值。
  不同 RMW 实现可能有不同默认值。

可在 `此处 <https://github.com/ros2/rmw/blob/{REPOS_FILE_BRANCH}/rmw/include/rmw/qos_profiles.h>`__ 查看上述配置文件使用的具体策略。
这些配置文件的设置可能会根据社区反馈进一步调整。

.. _about-qos_compatibilities:

QoS 兼容性
----------

**注意：** 本节讨论的是发布者与订阅者，但同样适用于服务服务器和客户端。

QoS 配置文件可以分别为发布者和订阅者单独配置。
只有当发布者和订阅者的 QoS 配置文件兼容时，才会建立连接。

QoS 配置文件兼容性基于“请求与提供”模型来决定。
订阅者 *请求* 一个 QoS 配置文件，作为其愿意接受的“最低质量”；发布者 *提供* 一个 QoS 配置文件，作为其能够提供的“最高质量”。
仅当请求的 QoS 配置文件中每项策略都不比提供的 QoS 配置文件更严格时，连接才会建立。
多个订阅者可以同时连接到一个发布者，即使它们请求的 QoS 配置文件不同。
发布者与订阅者之间的兼容性不受其他发布者和订阅者存在与否的影响。

下表展示了不同策略设置的兼容性及结果：

*可靠性 QoS 策略兼容性：*

.. list-table::
   :header-rows: 1

   * - Publisher
     - Subscription
     - Compatible
   * - Best effort
     - Best effort
     - Yes
   * - Best effort
     - Reliable
     - No
   * - Reliable
     - Best effort
     - Yes
   * - Reliable
     - Reliable
     - Yes

*耐久性 QoS 策略兼容性：*

.. list-table::
   :header-rows: 1

   * - Publisher
     - Subscription
     - Compatible
     - Result
   * - Volatile
     - Volatile
     - Yes
     - New messages only
   * - Volatile
     - Transient local
     - No
     - No communication
   * - Transient local
     - Volatile
     - Yes
     - New messages only
   * - Transient local
     - Transient local
     - Yes
     - New and old messages

若要实现对后加入订阅者可见的“latched”主题，
发布者和订阅者必须都同意使用 'Transient Local'。

*截止时间 QoS 策略兼容性：*

  假设 *x* 与 *y* 是任意有效持续时间值。

.. list-table::
   :header-rows: 1

   * - Publisher
     - Subscription
     - Compatible
   * - Default
     - Default
     - Yes
   * - Default
     - *x*
     - No
   * - *x*
     - Default
     - Yes
   * - *x*
     - *x*
     - Yes
   * - *x*
     - *y* (where *y* > *x*)
     - Yes
   * - *x*
     - *y* (where *y* < *x*)
     - No

*活性 QoS 策略兼容性：*

.. list-table::
   :header-rows: 1

   * - Publisher
     - Subscription
     - Compatible
   * - Automatic
     - Automatic
     - Yes
   * - Automatic
     - Manual by topic
     - No
   * - Manual by topic
     - Automatic
     - Yes
   * - Manual by topic
     - Manual by topic
     - Yes

*租期持续时间 QoS 策略兼容性：*

  假设 *x* 与 *y* 是任意有效持续时间值。

.. list-table::
   :header-rows: 1

   * - Publisher
     - Subscription
     - Compatible
   * - Default
     - Default
     - Yes
   * - Default
     - *x*
     - No
   * - *x*
     - Default
     - Yes
   * - *x*
     - *x*
     - Yes
   * - *x*
     - *y* (where *y* > *x*)
     - Yes
   * - *x*
     - *y* (where *y* < *x*)
     - No

要使连接得以建立，所有影响兼容性的策略都必须兼容。
例如，即使请求与提供的 QoS 配置文件在可靠性 QoS 策略上兼容，但它们在耐久性 QoS 策略上不兼容，连接仍然不会建立。

当连接没有建立时，发布者与订阅者之间不会传递任何消息。
有机制可以检测到这种情况，这将在后面的章节中介绍。

与 ROS 1 的比较
^^^^^^^^^^^^^^^

从历史上看，在 ROS 1 中，只要发布者和订阅者使用相同话题上的相同消息类型，它们就会被连接。
请求与提供的 QoS 配置文件可能不兼容，这是使用 ROS 2 时需要了解的新情况。

.. _about-qos_qos-events:

QoS 事件
--------

某些 QoS 策略可能有与之相关的事件。
开发者可以为每个发布者和订阅者提供回调函数，这些回调函数由这些 QoS 事件触发，并以开发者认为合适的方式进行处理，类似于处理话题上接收到的消息的方式。

开发者可以订阅以下与发布者关联的 QoS 事件：

* 未满足所提供的截止时间

  发布者没有在截止时间 QoS 策略规定的预期时长内发布消息。

* 活性丢失

  发布者未能在租期持续时间内表明其活性。

* 所提供的 QoS 不兼容

  发布者在同一话题上遇到了一个订阅者，该订阅者请求的 QoS 配置文件无法由所提供的 QoS 配置文件满足，导致发布者与该订阅者之间没有建立连接。

开发者可以订阅以下与订阅者关联的 QoS 事件：

* 未满足所请求的截止时间

  订阅者没有在截止时间 QoS 策略规定的预期时长内接收到消息。

* 活性改变

  订阅者发现所订阅话题上的一个或多个发布者未能在租期持续时间内表明其活性。

* 请求的 QoS 不兼容

  订阅者在同一话题上遇到了一个发布者，该发布者提供的 QoS 配置文件无法满足所请求的 QoS 配置文件，导致订阅者与该发布者之间没有建立连接。
