#!/usr/bin/python
# -*- coding: utf-8 -*-

# created by Alexander Kabza, 2022-02-21
# 2022-02-21    first version
# 2022-02-22    minor mods

import os
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

TCP_IP = '192.168.144.54'
UNIT_ID = 3
PORT = 502

def getvalue(reg, len):
    #data = mbus.read_data(reg, len)
    data = mb_device.read_holding_registers(int(reg), len)
    Translate = convert()
    Translate.u16.h = data[1]
    Translate.u16.l = data[0]
    value = Translate.uint32
    return value

if __name__ == "__main__":
    now = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))

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
    CondMode = getvalue(30201, 2)
    OpHrs = getvalue(30541, 2) / 3600.0
    FeedInHrs = getvalue(30543, 2)
    if (FeedInHrs >= int("FFFFFFFF", 16)):  # >= 4,294,967.29, 0x100000000 = 4,294,967,295
        FeedInHrs = PrevFeedInHrs
    else:
        FeedInHrs = FeedInHrs / 3600.0
    TotalYield = getvalue(30529, 4)
    if (TotalYield >= int("FFFFFFFF", 16)):  # >= 4,294,967.29, 0x100000000 = 4,294,967,295
        TotalYield = PrevTotalYield
    else:
        TotalYield = TotalYield / 1000.0
    TotalGrid = getvalue(30581, 2) / 1000.0
    TotalFeedIn = getvalue(30583, 2) / 1000.0
    PowerGrid = getvalue(30865, 2)
    PowerFeed = getvalue(30867, 2)
    PowerPV = getvalue(30775, 2)
    if (PowerPV == int("80000000", 16)):
        PowerPV = 0.0
    U1 = getvalue(31253, 2) / 100.0
    U2 = getvalue(31255, 2) / 100.0
    U3 = getvalue(31257, 2) / 100.0

    print("SerNo = ", SerNo)
    print("PowerGrid = {:d} W".format(PowerGrid))
    print("CondMode = ", CondMode)
    print("OpHrs = {0:0.2f} hrs".format(OpHrs))
    print("FeedInHrs = {0:0.2f} hrs".format(FeedInHrs))
    print("TotalYield = {0:0.2f} kWh".format(TotalYield))
    print("TotalGrid = {0:0.2f} kWh".format(TotalGrid))
    print("TotalFeedIn = {0:0.2f} kWh".format(TotalFeedIn))
    print("PowerGrid = {0:0.0f} W".format(PowerGrid))
    print("PowerFeed = {0:0.0f} W".format(PowerFeed))
    print("PowerPV = {0:0.0f} W".format(PowerPV))
    print("U1 = {0:0.2f} V".format(U1))
    print("U2 = {0:0.2f} V".format(U2))
    print("U3 = {0:0.2f} V\n".format(U3))

    mb_device.close()
	