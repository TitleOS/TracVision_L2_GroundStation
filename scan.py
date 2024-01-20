import os
import time
from serial import Serial
from serial.tools import list_ports
import argparse

parser = argparse.ArgumentParser(description='Sky Microwave Imager for TracVision L2 satellite dish.')
parser.add_argument('--port', metavar='PORT', type=str, help='the serial port to use', default='COM5')
parser.add_argument('--start_az', metavar='START_AZ', type=int, help='the starting azimuth', default='0')
parser.add_argument('--end_az', metavar='END_AZ', type=int, help='the ending azimuth', default='3599')
parser.add_argument('--start_el', metavar='START_EL', type=int, help='the starting elevation', default='100')
parser.add_argument('--end_el', metavar='END_EL', type=int, help='the ending elevation', default='700')

args = parser.parse_args()

if(args.start_az < 0 or args.start_az > 3599):
    print('Error: start_az must be between 0 and 3599')
    exit()
if(args.end_az < 0 or args.end_az > 3599):
    print('Error: end_az must be between 0 and 3599')
    exit()
if(args.start_el < 100 or args.start_el > 700):
    print('Error: start_el must be between 100 and 700')
    exit()
if(args.end_el < 100 or args.end_el > 700):
    print('Error: end_el must be between 100 and 700')
    exit()

ser = Serial(args.port, 9600)

if(ser.is_open):
    print('Connected @9600 @' + args.port + ', your scan will commence shortly.')
else:
    print('Error connecting to the serial port, please check your port name and try again.')
    print('Available serial ports: ')
    for port in list_ports.comports():  # Iterate over the list of available ports and print.
        print(port + "\n")
    exit()

def send_command(command, wait_time=1):
    ser.write(command.encode() + '\r\n'.encode()) # Send the command plus a carriage return to the dish over serial.
    out = ''
    time.sleep(wait_time)
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()
    if out != '':
        print(">>" + out)

def initialize_dish():
    send_command('halt', 3) # Wait 3 seconds to break into terminal mode.
    print("Initialized Terminal Mode.")
    send_command('version', 1)
    print("Echoed version.")
    send_command('AZ,0000', 5) # Park the dish at azimuth 0 for calibration.
    print("Set azimuth to 0.")
    send_command('EL,100', 5)
    print("Set elevation to 100.") # Park the dish at elevation 100 (Lowest) for calibration.
    print("Dish orientation initialized.")

def get_current_signal_strength():
    send_command('SIGLEVEL', 1)
    out = ''
    time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()
    if out != '':
        return out.split('=')[1].split(' ')[1] #Return: Signal Strength = XXXX


    