#!/usr/bin/python3
# -*- coding: utf-8 -*-

# read_sma_modbus.py, based on https://github.com/JanusHL/pvcontrol/tree/master/SMA
# created by Alexander Kabza, 2020-02-26
# 2022-03-18    changed from Python2 to Python3

import os
import datetime
import time
import sys
from pyModbusTCP.client import ModbusClient

import ctypes

class x2u16Struct(ctypes.Structure):
    _fields_ = [("h", ctypes.c_uint16),
                ("l", ctypes.c_uint16)]


class convert(ctypes.Union):
    _fields_ = [("float", ctypes.c_float),
                ("u16", x2u16Struct),
                ("sint32", ctypes.c_int32),
                ("uint32", ctypes.c_uint32)]

def getvalue(reg, len):
    # data = mbus.read_data(reg, len)
    data = mb_device.read_holding_registers(int(reg), len)
    Translate = convert()
    Translate.u16.h = data[1]
    Translate.u16.l = data[0]
    value = Translate.uint32
    return value


if __name__ == "__main__":

    TCP_IP = '192.168.144.54'
    UNIT_ID = 3
    PORT = 502

    now = datetime.datetime.now()
    nowstr = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        mb_device = ModbusClient(host=TCP_IP, port=PORT, timeout=10, debug=True, unit_id=UNIT_ID)
        mb_device.open()
    except:
        print(mb_device)
        # return mb_device.last_error()
        raise

    SerNo = getvalue(30005, 2)
    PowerGrid = getvalue(30865, 2)
    DeviceClass = getvalue(30051, 2)
    Condition = getvalue(30201, 2)
    OpHrs = getvalue(30541, 2) / 3600.0
    FeedInHrs = getvalue(30543, 2) / 3600.0
    TotalYield = getvalue(30529, 4) / 1000.0
    TotalGrid = getvalue(30581, 2) / 1000.0
    TotalFeedIn = getvalue(30583, 2) / 1000.0
    PowerGrid = getvalue(30865, 2)
    PowerFeed = getvalue(30867, 2)
    PowerPV = getvalue(30775, 2)
    if (PowerPV == int("80000000", 16)):
        PowerPV = 0.0
    UL1 = getvalue(30783, 2) / 100.0
    UL2 = getvalue(30785, 2) / 100.0
    UL3 = getvalue(30787, 2) / 100.0
    UPPCL1 = getvalue(31253, 2) / 100.0
    UPPCL2 = getvalue(31255, 2) / 100.0
    UPPCL3 = getvalue(31257, 2) / 100.0
    UL1L2 = getvalue(30789, 2) / 100.0
    UL2L3 = getvalue(30791, 2) / 100.0
    UL3L1 = getvalue(30793, 2) / 100.0

    print("SerNo = ", SerNo)
    print("PowerGrid = {:d} W".format(PowerGrid))
    print("Condition = ", Condition)
    print("OpHrs = {0:0.2f} hrs".format(OpHrs))
    print("FeedInHrs = {0:0.2f} hrs".format(FeedInHrs))
    print("TotalYield = {0:0.2f} kWh".format(TotalYield))
    print("TotalGrid = {0:0.2f} kWh".format(TotalGrid))
    print("TotalFeedIn = {0:0.2f} kWh".format(TotalFeedIn))
    print("PowerGrid = {0:0.0f} W".format(PowerGrid))
    print("PowerFeed = {0:0.0f} W".format(PowerFeed))
    print("PowerPV = {0:0.0f} W".format(PowerPV))
    print("UL1 = {0:0.2f} V".format(UL1))
    print("UL2 = {0:0.2f} V".format(UL2))
    print("UL3 = {0:0.2f} V".format(UL3))
    print("UPPCL1 = {0:0.2f} V".format(UPPCL1))
    print("UPPCL2 = {0:0.2f} V".format(UPPCL2))
    print("UPPCL3 = {0:0.2f} V".format(UPPCL3))
    print("UL1L2 = {0:0.2f} V".format(UL1L2))
    print("UL2L3 = {0:0.2f} V".format(UL2L3))
    print("UL3L1 = {0:0.2f} V\n".format(UL3L1))

    mb_device.close()
