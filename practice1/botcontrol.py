#!/usr/bin/python3.6

import sys
import time
import math
import paho.mqtt.client as mqtt


class ArgumentsError(Exception):
    pass


class Robot():
    def __init__(self, 
                 broker_ip, 
                 broker_port, 
                 topic,
                 x=0, 
                 y=0, 
                 angle=0, 
                 speed=0, 
                 r_speed=0):
        self.client = mqtt.Client("robo_client")
        self.client.connect(broker_ip, broker_port)
        self.client.loop_start()
        self.client.subscribe(topic)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.r_speed = r_speed
        self.path = []


    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))


class RoboController():
    def __init__(self, 
                 broker_ip, 
                 broker_port, 
                 topic,
                 filename,
                 speed,
                 r_speed,
                 angle=0,
                 curr_x=0,
                 curr_y=0):
        self.x = curr_x
        self.y = curr_y
        self.speed = speed
        self.r_speed = r_speed
        self.angle = angle
        self.topic = topic
        self.client = mqtt.Client("controller_client")
        self.client.connect(broker_ip, broker_port)
  #      self.client.loop_start()
        self.path = []
        self.filename = filename
        self.send_message()

    def read_coordinates(self):
        with open(self.filename, 'r') as f:
            for xy_coord in f:
                x, y = xy_coord.split()
                self.path.append([float(x), float(y)])
    
    def calc_distance(self, x, y):
        return ((self.x - x)**2 + (self.y - y)**y)**0.5

    def calc_distance_time(self, distance):
        return distance / self.speed

    def calc_angle(self, x, y):
        if (x == 0 and y == 0) or (self.x == 0 and self.y == 0):
            return math.acos(0)
        cos_angle = (self.x * x + self.y * y) \
                  / (self.x * self.x + self.y * self.y)**0.5 \
                  * (x * x + y * y)**0.5
            
        return math.acos(cos_angle)

    def calc_rotate_time(self, angle):
        return angle / self.r_speed

    def create_message(self):
        msg = ''
        for point in self.path:
            x, y = point[0], point[1]
            distance = self.calc_distance(x, y)
            distance_time = self.calc_distance_time(distance)
            angle = self.calc_angle(x, y)
            rotate_time = self.calc_rotate_time(angle)
            

            if angle > 0:
                msg += str({'cmd': 'left', 'val': rotate_time})
            elif angle < 0:
                msg += str({'cmd': 'right', 'val': rotate_time})
            
            msg += str({'cmd': 'forward', 'val': distance_time})
            msg += str({'cmd': 'stop'})
    
        return msg

    def send_message(self):
        self.read_coordinates()
        msg = self.create_message()
        self.client.publish(self.topic, msg)
        print(self.topic, msg)

       
def main():
    try:
        print([i for i in sys.argv])
        if len(sys.argv) != 7:
            raise ArgumentsError('invalid number of parameters.\n'
                                 'Trere are should be:\n'
                                 'ip_address,\n'
                                 'port,\n'
                                 'topic_name,\n'
                                 'speed,\n'
                                 'rotation speed,\n'
                                 'file with coordinates')
    except ArgumentsError as e:
        print(str(e))
    else:
        broker_address = str(sys.argv[1])
        broker_port = int(sys.argv[2])
        topic_name = str(sys.argv[3])
        speed = float(sys.argv[4])
        r_speed = float(sys.argv[5])
        filename = str(sys.argv[6])
        
        r = RoboController(broker_address, broker_port, topic_name, filename, speed, r_speed)
        

if __name__ == "__main__":
    main()
