import os
import time
from serial import Serial
from serial.tools import list_ports
import argparse

parser = argparse.ArgumentParser(description='Terminal for TracVision L2 satellite dish controller.')
parser.add_argument('--port', metavar='PORT', type=str, help='the serial port to use', default='COM5')

args = parser.parse_args()

ser = Serial(args.port, 9600)

if(ser.is_open):
    print('Connected @9600 @' + args.port + ', enter your command followed by enter.\r\nInsert "exit" to leave the application.')
else:
    print('Error connecting to the serial port, please check your port name and try again.')
    print('Available serial ports: ')
    for port in list_ports.comports():  # iterate over the list of available ports
        print(port)
    exit()

has_sent_halt = False
has_sent_ver = False
while has_sent_halt == False:
    ser.write('halt\r\n'.encode())
    out = ''
    time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()
    if out != '':
        print(">>" + out)
        print("Initialzed Terminal Mode.")
        has_sent_halt = True

while has_sent_ver == False:
    ser.write('version\r\n'.encode())
    out = ''
    time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()
    if out != '':
        print(">>" + out)
        print("Echoing version...")
        has_sent_ver = True

while True:
    user_input = input(">>")
    if user_input == 'exit':
        ser.close()
        exit()
    else:
        ser.write(user_input.encode() + '\r\n'.encode())
        out = ''
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1).decode()
        if out != '':
            print(">>" + out)