#! /usr/bin/env python
#coding: utf-8

import rospy
from geometry_msgs.msg import Twist, Vector3
from math import pi

v = 0.5  # Velocidade linear
w = pi/3  # Velocidade angular
stop = 0
if __name__ == "__main__":
    rospy.init_node("roda_exemplo")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=3)

    try:
        while not rospy.is_shutdown():

            frente = Twist(Vector3(v,0,0), Vector3(0,0,0))
            curva = Twist(Vector3(0,0,0), Vector3(0,0,w))
            parar = Twist(Vector3(0,0,0), Vector3(0,0,0))

            pub.publish(parar)
            rospy.sleep(2)

            #1 reta
            pub.publish(frente)
            rospy.sleep(3)
            #1 curva 
            pub.publish(curva)
            rospy.sleep(1.5)

            #2 reta 
            pub.publish(frente)
            rospy.sleep(3)
            #2 curva 
            pub.publish(curva)
            rospy.sleep(1.5)

            #3 reta
            pub.publish(frente)
            rospy.sleep(3)
            #3 curva 
            pub.publish(curva)
            rospy.sleep(1.5)

            #4 reta
            pub.publish(frente)
            rospy.sleep(3)
            #4 curva 
            pub.publish(curva)
            rospy.sleep(1.5)


    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")