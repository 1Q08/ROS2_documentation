.. redirect-from::

    Tutorials/Tf2/Quaternion-Fundamentals

.. _QuaternionFundamentals:

四元数基础
==========

**目标：** 学习 ROS 2 中四元数使用的基础知识。

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

四元数是方向的 4 元组表示，它比旋转矩阵更简洁。
四元数在分析涉及三维旋转的情况时非常高效。
四元数被广泛用于机器人学、量子力学、计算机视觉和 3D 动画。

你可以在 `Wikipedia <https://en.wikipedia.org/wiki/Quaternion>`_ 上了解更多关于其底层数学概念的内容。
你也可以看看由 `3blue1brown <https://www.youtube.com/3blue1brown>`_ 制作的可探索视频系列 `Visualizing quaternions <https://eater.net/quaternions>`_。

在本教程中，你将学习四元数及其转换方法在 ROS 2 中是如何工作的。

先决条件
--------

你可以看看像 `transforms3d <https://github.com/matthew-brett/transforms3d>`_、`scipy.spatial.transform <https://github.com/scipy/scipy/tree/master/scipy/spatial/transform>`_、`pytransform3d <https://github.com/rock-learning/pytransform3d>`_、`numpy-quaternion <https://github.com/moble/quaternion>`_ 或 `blender.mathutils <https://docs.blender.org/api/master/mathutils.html>`_ 这样的库。

不过，这不是硬性要求，你可以使用任何最适合你的其他几何变换库。

四元数的组成
------------

ROS 2 使用四元数来追踪和应用旋转。
四元数有 4 个分量 ``(x, y, z, w)``。
在 ROS 2 中，``w`` 在最后，但在 Eigen 等一些库中，``w`` 可以放在第一个位置。
常用的不产生绕 x/y/z 轴旋转的单位四元数是 ``(0, 0, 0, 1)``，可以通过以下方式创建：

.. code-block:: C++

   #include <tf2/LinearMath/Quaternion.h>
   ...

   tf2::Quaternion q;
   // Create a quaternion from roll/pitch/yaw in radians (0, 0, 0)
   q.setRPY(0, 0, 0);
   // Print the quaternion components (0, 0, 0, 1)
   RCLCPP_INFO(this->get_logger(), "%f %f %f %f",
               q.x(), q.y(), q.z(), q.w());

四元数的模长应该始终为 1。
如果数值误差导致四元数的模长不为 1，ROS 2 会打印警告。
为避免这些警告，请对四元数进行归一化：

.. code-block:: C++

   q.normalize();

ROS 2 中的四元数类型
--------------------

ROS 2 使用两种四元数数据类型：``tf2::Quaternion`` 及其等价的 ``geometry_msgs::msg::Quaternion``。
要在 C++ 中在它们之间转换，请使用 ``tf2_geometry_msgs`` 的方法。

.. code-block:: C++

   #include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
   ...

   tf2::Quaternion tf2_quat, tf2_quat_from_msg;
   tf2_quat.setRPY(roll, pitch, yaw);
   // Convert tf2::Quaternion to geometry_msgs::msg::Quaternion
   geometry_msgs::msg::Quaternion msg_quat = tf2::toMsg(tf2_quat);

   // Convert geometry_msgs::msg::Quaternion to tf2::Quaternion
   tf2::convert(msg_quat, tf2_quat_from_msg);
   // or
   tf2::fromMsg(msg_quat, tf2_quat_from_msg);

Python 中没有 ``tf2::Quaternion`` 的等价物。
而是使用内建的 ``list``。

.. code-block:: python

   from geometry_msgs.msg import Quaternion
   ...

   # Create a list of floats, which is compatible with tf2
   # Quaternion methods
   quat_tf = [0.0, 1.0, 0.0, 0.0]

   # Convert a list to geometry_msgs.msg.Quaternion
   msg_quat = Quaternion(x=quat_tf[0], y=quat_tf[1], z=quat_tf[2], w=quat_tf[3])

四元数运算
----------

1 先用 RPY 思考，再转换为四元数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

我们很容易思考绕轴的旋转，但很难用四元数来思考。
一个建议是，用三个独立的旋转 *roll* （绕 X 轴）、*pitch* （绕 Y 轴）和 *yaw* （绕 Z 轴）来计算目标旋转，然后转换为四元数。

.. code-block:: python

   # quaternion_from_euler method is available in turtle_tf2_py/turtle_tf2_py/turtle_tf2_broadcaster.py
   q = quaternion_from_euler(1.5707, 0, -1.5707)
   print(f'The quaternion representation is x: {q[0]} y: {q[1]} z: {q[2]} w: {q[3]}.')

这个方法与 `欧拉角 <https://en.wikipedia.org/wiki/Euler_angles>`_ 相关。
有几种应用欧拉角的方式。
上面描述的、ROS 2 所采用的方式被称为*固定（或静态）坐标系* RPY。
这意味着三个独立的旋转被应用到原始的、不移动的坐标轴上。
这与*相对坐标系*相反，相对坐标系中的旋转被应用到被先前旋转变换过的坐标轴上。


2 应用四元数旋转
^^^^^^^^^^^^^^^^

要将一个四元数的旋转应用到位姿上，只需将位姿之前的四元数乘以表示所需旋转的四元数。
这个乘法的顺序很重要。

C++

.. code-block:: C++

   #include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
   ...

   tf2::Quaternion q_orig, q_rot, q_new;

   q_orig.setRPY(0.0, 0.0, 0.0);
   // Rotate the previous pose by 180* about X
   q_rot.setRPY(3.14159, 0.0, 0.0);
   q_new = q_rot * q_orig;
   q_new.normalize();

Python

.. code-block:: python

   q_orig = quaternion_from_euler(0, 0, 0)
   # Rotate the previous pose by 180* about X
   q_rot = quaternion_from_euler(3.14159, 0, 0)
   q_new = quaternion_multiply(q_rot, q_orig)


3 四元数求逆
^^^^^^^^^^^^

求四元数逆的一个简单方法是对 x、y 和 z 分量取负：

.. code-block:: python

   q[0] = -q[0]
   q[1] = -q[1]
   q[2] = -q[2]

.. note::

   这不应与对四元数的*所有*元素取负相混淆。

4 相对旋转
^^^^^^^^^^

假设你有同一坐标系下的两个四元数 ``q_1`` 和 ``q_2``。
你想找到相对旋转 ``q_r``，它以如下方式将 ``q_1`` 转换为 ``q_2``：

.. code-block:: C++

   q_2 = q_r * q_1

你可以像求解矩阵方程一样求解 ``q_r``。
对 ``q_1`` 求逆并右乘两边。
同样，乘法的顺序很重要：

.. code-block:: C++

   q_r = q_2 * q_1_inverse

下面是一个用 python 获取从上一个机器人位姿到当前机器人位姿的相对旋转的示例：

.. code-block:: python

  def quaternion_multiply(q0, q1):
      """
      Multiplies two quaternions.

      Input
      :param q0: A 4 element array containing the first quaternion (q01, q11, q21, q31)
      :param q1: A 4 element array containing the second quaternion (q02, q12, q22, q32)

      Output
      :return: A 4 element array containing the final quaternion (q03,q13,q23,q33) in (w, x, y, z) order

      """
      # Extract the values from q0
      x0 = q0[0]
      y0 = q0[1]
      z0 = q0[2]
      w0 = q0[3]

      # Extract the values from q1
      x1 = q1[0]
      y1 = q1[1]
      z1 = q1[2]
      w1 = q1[3]

      # Compute the product of the two quaternions, term by term
      q0q1_w = w0 * w1 - x0 * x1 - y0 * y1 - z0 * z1
      q0q1_x = w0 * x1 + x0 * w1 + y0 * z1 - z0 * y1
      q0q1_y = w0 * y1 - x0 * z1 + y0 * w1 + z0 * x1
      q0q1_z = w0 * z1 + x0 * y1 - y0 * x1 + z0 * w1

      # Create a 4 element array containing the final quaternion
      final_quaternion = np.array([q0q1_w, q0q1_x, q0q1_y, q0q1_z])

      # Return a 4 element array containing the final quaternion (q02,q12,q22,q32)
      return final_quaternion

  q1_inv[0] = -prev_pose.pose.orientation.x   # Negate for inverse
  q1_inv[1] = -prev_pose.pose.orientation.y   # Negate for inverse
  q1_inv[2] = -prev_pose.pose.orientation.z   # Negate for inverse
  q1_inv[3] = prev_pose.pose.orientation.w

  q2[0] = current_pose.pose.orientation.x
  q2[1] = current_pose.pose.orientation.y
  q2[2] = current_pose.pose.orientation.z
  q2[3] = current_pose.pose.orientation.w

  qr = quaternion_multiply(q2, q1_inv)

总结
----

在本教程中，你学习了四元数的基本概念及其相关的数学运算，如求逆和旋转。
你还学习了它在 ROS 2 中的使用示例，以及两个独立 Quaternion 类之间的转换方法。
