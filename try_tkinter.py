# -*- coding: utf_8 -*-

import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import struct
from tkinter import *


#下面是读写数据的
def ReadFloat(*args,reverse=False):
    for n,m in args:
        n,m = '%04x'%n,'%04x'%m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!f',y_bytes)[0]
    y = round(y,6)
    return y

def WriteFloat(value,reverse=False):
    y_bytes = struct.pack('!f',value)
    # y_hex = bytes.hex(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    n,m = y_hex[:-4],y_hex[-4:]
    n,m = int(n,16),int(m,16)
    if reverse:
        v = [n,m]
    else:
        v = [m,n]
    return v

def ReadDint(*args,reverse=False):
    for n,m in args:
        n,m = '%04x'%n,'%04x'%m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!i',y_bytes)[0]
    return y

def WriteDint(value,reverse=False):
    y_bytes = struct.pack('!i',value)
    # y_hex = bytes.hex(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    n,m = y_hex[:-4],y_hex[-4:]
    n,m = int(n,16),int(m,16)
    if reverse:
        v = [n,m]
    else:
        v = [m,n]
    return v

def judge_type():
     if(v_data_type.get()=="浮点数"):
          v = WriteFloat(float(v_data.get()),True)
     elif(v_data_type.get()=="整数"):
          v = WriteDint(int(v_data.get()),True)
     return v

def judge_type2(red):
     if(v_data_type.get()=="浮点数"):
          print(red)
          v = ReadFloat(red, reverse=True)
     elif(v_data_type.get()=="整数"):
          print(red)
          v = ReadDint(red ,reverse=True)
     return v

def receive(PORT="com4"):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT,
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        # 读寄存器
        red = master.execute(int(v_arm_address.get()), cst.READ_HOLDING_REGISTERS, int(v_register_address.get()),quantity_of_x=2)  # 这里可以修改需要读取的功能码
        v_r_data.set(judge_type2(red))

    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))

def mod(PORT="com4"):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT,
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(5.0)
        master.set_verbose(True)

        # 写寄存器
        write_data = judge_type()
        wri = master.execute(int(v_arm_address.get()), cst.WRITE_MULTIPLE_REGISTERS, int(v_register_address.get()), output_value=write_data)  # 这里可以修改需要读取的功能码

    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))

root = Tk()

Label(root, text='设备地址：').grid(row=0)
Label(root, text='寄存器地址：').grid(row=1)
Label(root, text='读取寄存器位数\写入的数据：').grid(row=2)
Label(root, text='写入的数据类型：').grid(row=3)
Label(root, text='接收到的数据：').grid(row=5)

v_arm_address = IntVar()
v_register_address = IntVar()
v_data_type = StringVar()
v_data_type.set("整数")
v_data = StringVar()
v_r_data = StringVar()

e_arm_address = Entry(root, textvariable=v_arm_address)\
                .grid(row=0, column=1, padx=10, pady=5)
e_register_address = Entry(root, textvariable=v_register_address)\
                     .grid(row=1, column=1, padx=10, pady=5)
e_data = Entry(root, textvariable=v_data)\
                     .grid(row=2, column=1, padx=10, pady=5)
w =OptionMenu(root, v_data_type ,"浮点数","整数")\
                   .grid(row=3, column=1, padx=10, pady=5)
text_r_data = Entry(root, textvariable=v_r_data)\
                     .grid(row=5, column=1, padx=10, pady=5)

def deal():
     mod()
     print("传送成功"+v_data_type.get())
def deal2():
     receive()
     
Button(root, text="发送数据", width=10, command=deal)\
             .grid(row =4, column =0, sticky =W, padx=10,pady=5)
Button(root, text="接收数据", width=10, command=deal2)\
             .grid(row =4, column =1, sticky =E, padx=10,pady=5)


mainloop()
