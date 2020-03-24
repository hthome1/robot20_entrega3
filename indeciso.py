#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
import numpy as np

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan


def scaneou(dado):
    print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
    print("Leituras:")
    print(np.array(dado.ranges).round(decimals=2))
    dados = dado
    global dados
    


if __name__=="__main__":

    rospy.init_node("le_scan")

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
    recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)



    while not rospy.is_shutdown():
        print("Oeee")
        vel_forw = Twist(Vector3(0.1,0,0), Vector3(0,0,0))
        vel_back = Twist(Vector3(-0.1,0,0), Vector3(0,0,0))
        velocidade_saida.publish(vel_forw)
        rospy.sleep(2)

        if dados.ranges[0] < 1:
            velocidade_saida.publish(vel_back)
            rospy.sleep(2)
        if dados.ranges[0] > 1.02:
            velocidade_saida.publish(vel_forw)
            rospy.sleep(2)


