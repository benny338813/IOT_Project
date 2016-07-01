#!/usr/bin/python
# -*- coding: utf-8 -*-
import uuid
import sys
import threading
import time
import json
import os
sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'NIT_Module'))
import NIT_Node_Module
sys.path.append("..")
from terminalColor import bcolors
import random
import base64

NodeUUID = "Car2" +"@NODE-" + str(uuid.uuid1())

Functions = ["Image"]
NodeFunctions = ['GPS']  # ['Cam', 'GPS', 'CG'] 此NODE的功能
FuncSVList = []

print("::::::::::::::::::::::::::::::::::::::::::")
print("::::::::::::::::::::::::::::::::::::::::::")
print("'##::: ##::'#######::'########::'########:")
print(" ###:: ##:'##.... ##: ##.... ##: ##.....::")
print(" ####: ##: ##:::: ##: ##:::: ##: ##:::::::")
print(" ## ## ##: ##:::: ##: ##:::: ##: ######:::")
print(" ##. ####: ##:::: ##: ##:::: ##: ##...::::")
print(" ##:. ###: ##:::: ##: ##:::: ##: ##:::::::")
print(" ##::. ##:. #######:: ########:: ########:")
print("..::::..:::.......:::........:::........::")
print("::::::::::::::::::::::::::::::::::::::::::\n")

nit = NIT_Node_Module.NIT_Node(NodeUUID, Functions, NodeFunctions)

startPos = [22.993560, 120.223975];
endPos = [22.998518, 120.224383];	
# 緯度
def getLongitude(i): 
	return i*(endPos[0] - startPos[0])/10 + startPos[0]
	
# 經度	
def getLatitude(i):
	return i*(endPos[1] - startPos[1])/10 + startPos[1]

def getTemperature():
	return 75	
	
def path():
	if "counter" not in dir(path):
		path.counter = 0
		path.gap = 1
	else:
		path.counter+=path.gap

	if path.counter > 10:
		path.gap = -path.gap
	elif path.counter < 0:
		path.counter = 1
		path.gap = -path.gap
		
	print(path.counter)
		
	gpsData = str(getLongitude(path.counter)) + "," + str(getLatitude(path.counter))
	print(gpsData)
	return gpsData

class CustomError(Exception):
    """Base class for other exceptions"""
    def __init__(self, msg='err'):
        self.msg = msg


# Connect to MQTT Server for communication
def NodeToServerMQTTThread():
	# print("thread name：　" + threading.current_thread().getName())
	# callback
	nit.CallBackRxRouting = RxRouting
	print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
	print(bcolors.HEADER + '---------------Node(%s)--->>>Server in MQTT-\n' % NodeUUID + bcolors.ENDC)
	print(bcolors.HEADER + '>>>Start connect Server %s<<<' % (
		time.asctime(time.localtime(time.time()))) + bcolors.ENDC)
	print(bcolors.HEADER + '===============================================\n' + bcolors.ENDC)
	print(bcolors.HEADER + 'Register to IoT Server successful! \n' + bcolors.ENDC)

	try:
		nit.RegisterNoode()  # 向IoT_Server註冊 TopicName = "IOTSV/REG" , 'Control': 'NODE_REG'
	except (RuntimeError, TypeError, NameError) as e:
		print(bcolors.FAIL + "[INFO]Register error." + str(e) + bcolors.ENDC)
		raise
		sys.exit(1)


########### Keyboard interactive ##############
def RxRouting(self, _obj_json_msg):  # 收到訊息會執行這個，可在這邊新增功能
	fs = nit.M2M_RxRouting(_obj_json_msg)
	if fs is not None and fs not in FuncSVList:
		FuncSVList.append(fs)

def imageToBase64Str(obj=''):
    try:
        imgName = obj + '.jpg'
        with open(imgName, "rb") as f_img:
            image = base64.encodebytes(f_img.read())  # binary to base64
            imgStr = image.decode('utf-8')  # bytes to str
            print(bcolors.WARNING + "[IMAGE] Open image success" + bcolors.ENDC)
        return imgStr
    except:
        raise CustomError(bcolors.FAIL + '[Err] File does not exist.' + bcolors.ENDC)

def loop():
	try:
		if not FuncSVList:
			raise CustomError(bcolors.FAIL + '[Err] No FunctionServer.' + bcolors.ENDC)
		else:
			for FS in FuncSVList:
				initMSGObj = {'TopicName': FS, 'Control': 'UpdateValue', 'Source': str(NodeUUID)}
				initMSGObj['GPS'] = path()
				initMSGObj['Temperature'] = getTemperature()
				initMSGSTR = json.dumps(initMSGObj)  # 將對象轉json(JavaScript Object Notation)
				nit.DirectMSG(FS, initMSGSTR)  # Publish directly
	except CustomError as e:
		print(e)

if __name__ == "__main__":
	MQTT_Thread = threading.Thread(target=NodeToServerMQTTThread, name="main_thread")
	MQTT_Thread.start()
	time.sleep(4)
	while True:
		time.sleep(1)
		loop()
