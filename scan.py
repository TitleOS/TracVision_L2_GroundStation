import time
from serial import Serial
from serial.tools import list_ports
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Sky Microwave Imager for TracVision L2 satellite dish.')
parser.add_argument('--port', metavar='PORT', type=str, help='the serial port to use', default='COM5')
parser.add_argument('--start_az', metavar='START_AZ', type=int, help='the starting azimuth', default='0')
parser.add_argument('--end_az', metavar='END_AZ', type=int, help='the ending azimuth', default='3599')
parser.add_argument('--start_el', metavar='START_EL', type=int, help='the starting elevation', default='100')
parser.add_argument('--end_el', metavar='END_EL', type=int, help='the ending elevation', default='700')

args = parser.parse_args()

current_timestamp = time.strftime("%Y%m%d-%H%M%S")

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

def initialize_serial():
    # Initialize the serial port.
    ser = Serial(args.port, 9600)

    if(ser.is_open):
        print('Connected @9600 @' + args.port + ', your scan will commence shortly.')
        return ser
    else:
        print('Error connecting to the serial port, please check your port name and try again.')
        print('Available serial ports: ')
        for port in list_ports.comports():  # Iterate over the list of available ports and print.
            print(port + "\n")
        exit()

def send_command(command, wait_time=1):
    ser.write(command.encode() + '\r\n'.encode()) # Send the command plus a carriage return to the dish over serial.
    time.sleep(wait_time)

def initialize_dish():
    init_term_mode()
    get_current_version()
    send_command('AZ,0000', 5) # Park the dish at azimuth 0 for calibration.
    print("Set azimuth to 0.")
    send_command('EL,100', 5)
    print("Set elevation to 100.") # Park the dish at elevation 100 (Lowest) for calibration.
    print("Dish orientation setup completed.")

def get_current_signal_strength():
    send_command('SIGLEVEL', 1)
    out = ''
    time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()
    if out != '':
        return out.split('=')[1].split(' ')[1] #Return: Signal Strength = XXXX
    
def get_current_version():
    send_command('VERSION', 1)
    out = ''
    time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()
    if out != '':
        return out

def init_term_mode():
    send_command('halt', 3) # Wait 3 seconds to break into terminal mode.
    ser.reset_output_buffer() # Clear the output buffer of the boot log.
    print("Initialized Terminal Mode.")

def write_scan_settings():
    # Write the scan settings to a file.
    f = open(f"scan_settings_{str(current_timestamp)}.txt", "w")
    f.write(str(args.start_az) + "\n")
    f.write(str(args.end_az) + "\n")
    f.write(str(args.start_el) + "\n")
    f.write(str(args.end_el) + "\n")
    f.close()

def main():
    az_range = args.end_az - args.start_az
    el_range = args.end_el - args.start_el

    #Build the Numpy data array to store the scan data.
    sky_data = np.zeros((el_range+1,az_range+1))

    global ser

    ser = initialize_serial()
    initialize_dish()

    print("Beginning scan...")
    start_time = time.time() #Start the timer.
    for el in range(args.start_el, args.end_el, 10): #Break the elevation range into 10 degree increments.
        send_command('EL,' + str(el), 1)
        print("Set elevation to " + str(el) + ".")
        for az in range(args.start_az, args.end_az, 10): #Break the azimuth range into 25 degree increments.
            send_command('AZ,' + str(az), 1)
            print("Set azimuth to " + str(az) + ".")
            signal_strength = get_current_signal_strength() #We have manuevered the dish to the current azimuth and elevation, now get the signal strength.
            print("Current signal strength: " + signal_strength)
            sky_data[abs(el - args.end_el),abs(az - args.end_az)]=signal_strength #record raw data to array
            np.savetxt(f"raw-data-" + current_timestamp +".txt", sky_data) #record raw data to array
    print("Scan complete, took " + str(time.time() - start_time) + " seconds.") #Print the time it took to complete the scan.


if __name__ == "__main__":
    main()