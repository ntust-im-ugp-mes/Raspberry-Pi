import RPi.GPIO as GPIO
import time
import threading
from socket import *

#network
serverName = '192.168.50.64'
serverPort = 11000
BUFSIZ = 1024
ADDR = (serverName,serverPort)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)
'''
while True:
    data = input('Input Data')
    if not data:
        break
    clientSocket.send(data.encode('utf-8'))
    returnData = clientSocket.recv(BUFSIZ)
    if not returnData:
        break
    print(returnData.decode('utf-8'))
clientSocket.close()
'''



GPIO.setmode(GPIO.BOARD)

redLED = [16,5,7]
blueLED = [18,13,15]
LaserSensor = [12,21,23]                     #定义激光接收模块信号引脚为2
Laser = [22,31,33]                           #定义激光发射模块信号引脚为12

 
def setup():
  # put your setup code here, to run once:
    #GPIO.setup(redLED, GPIO.OUT)    #定义LED为输出模式
    #GPIO.setup(blueLED, GPIO.OUT)    #定义LED为输出模式LED, GPIO.OUT)    #定义LED为输出模式
    #GPIO.setup(Laser, GPIO.OUT)  #定义Laser为输出模式
    #GPIO.setup(LaserSensor, GPIO.IN)  #定于LaserSensor为输入模式
    
    for i in range(len(redLED)):
        GPIO.setup(redLED[i], GPIO.OUT)
        
    for i in range(len(blueLED)):
        GPIO.setup(blueLED[i], GPIO.OUT)
        
    for i in range(len(LaserSensor)):
        GPIO.setup(LaserSensor[i], GPIO.IN)
        
    for i in range(len(Laser)):
        GPIO.setup(Laser[i], GPIO.OUT)


def loop():
    while True:
        for i in range(len(Laser)):
            GPIO.output(Laser[i], True)  #给Laser高电平，激光发射模式发射激光
            time.sleep(0.2) #延时200毫秒

        SensorReading = [GPIO.input(LaserSensor[0]),GPIO.input(LaserSensor[1]),GPIO.input(LaserSensor[2])]
        
        #SensorReading = GPIO.input(LaserSensor)  #读取LaserSensor(激光接收模块信号引脚)的当前状态
        for i in range(len(SensorReading)):
            if(SensorReading[i] == False):                   #如果等于电平
                GPIO.output(blueLED[i], False)
                GPIO.output(redLED[i], True)  #则red T(发射与接收之间有东西挡住)
                print( str(i) + ' th Sensor  : ' + str(SensorReading[i]))
                
                if i==0:
                    data = 's1,in'
                elif i==1:
                    data = 's2,in'
                elif i==2:
                    data = 's3,in'
                clientSocket.send(data.encode('utf-8'))
                returnData = clientSocket.recv(BUFSIZ)
                if not returnData:
                    break
                print(returnData.decode('utf-8'))
                
                
            elif(SensorReading[i] == True):
                GPIO.output(blueLED[i], True)  #则blue T(发射与接收之间没有障碍物)
                GPIO.output(redLED[i], False)  #则red F(发射与接收之间没有障碍物)
                print( str(i) + ' th Sensor  : ' + str(SensorReading[i]))
                
                if i==0:
                    data = 's1,out'
                elif i==1:
                    data = 's2,out'
                elif i==2:
                    data = 's3,out'
                clientSocket.send(data.encode('utf-8'))
                returnData = clientSocket.recv(BUFSIZ)
                if not returnData:
                    break
                print(returnData.decode('utf-8'))
                
setup()
loop()
