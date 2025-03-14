#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool

class SingleOdomPublisher:
    def __init__(self):
        rospy.init_node('single_odom_publisher', anonymous=True)

        self.input_sub = rospy.Subscriber('/human_input', Bool, self.input_callback)
        self.odom_pub = rospy.Publisher('/filtered_odom', Odometry, queue_size=10)
        self.reset_input_pub = rospy.Publisher('/human_input', Bool, queue_size=10)

    def input_callback(self, msg):
        if msg.data:
            odom_msg = rospy.wait_for_message('/odometry/imu', Odometry)
            self.odom_pub.publish(odom_msg)
            rospy.loginfo("Published one odometry message.")

            self.reset_input_pub.publish(Bool(False))
            rospy.loginfo("Human input reset to False.")

if __name__ == '__main__':
    try:
        SingleOdomPublisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
