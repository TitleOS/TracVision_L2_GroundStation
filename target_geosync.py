import ephem
import argparse
import time
import math
from serial import Serial
from serial.tools import list_ports

from satellite_tle import fetch_tle_from_celestrak


obs = ephem.Observer()

parser = argparse.ArgumentParser(description='Target GeoSync satellites using the TracVision L2.')
parser.add_argument('--norad_id', metavar='NORAD', type=str, help='The geosync satellite NORAD ID you would like to target.', default='41866')
parser.add_argument('--port', metavar='PORT', type=str, help='the serial port to use', default='COM5')
parser.add_argument('--latitude', metavar='LAT', type=float, help='Your present latitude', default='36.0')
parser.add_argument('--longitude', metavar='LONG', type=float, help='Your present longitude', default='-55.0')
parser.add_argument('--verbose', metavar='VERBOSE', type=bool, help='Enable verbose output', default=False)

args = parser.parse_args()

# Function to initialize the ephem observer's location using provided latitude and longitude
def initialize_observer(lat, long):
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.long = str(long)

    return observer

# Function to download TLE data for a given satellite
def download_tle(norad_id):
    try:
        tle_data = fetch_tle_from_celestrak(norad_id)
        return tle_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def initialize_serial():
    # Initialize the serial port.
    ser = Serial(args.port, 9600)

    if(ser.is_open):
        print('Connected @9600 @' + args.port + ', the dish will orientate towards your target shortly.')
        return ser
    else:
        print('Error connecting to the serial port, please check your port name and try again.')
        print('Available serial ports: ')
        for port in list_ports.comports():  # Iterate over the list of available ports and print.
            print(port + "\n")
        exit()

def init_term_mode():
    send_command('halt', 3) # Wait 3 seconds to break into terminal mode.
    print("Initialized Terminal Mode.")

def send_command(command, wait_time=1):
    ser.write(command.encode() + '\r\n'.encode()) # Send the command plus a carriage return to the dish over serial.
    time.sleep(wait_time)

def initialize_dish():
    init_term_mode()
    send_command('AZ,0000', 5) # Park the dish at azimuth 0 for calibration.
    print("Set azimuth to 0.")
    send_command('EL,100', 5)
    print("Set elevation to 100.") # Park the dish at elevation 100 (Lowest) for calibration.
    print("Dish orientation setup completed.")

def move_zero(number):
    # Convert the number to a string
    num_str = str(number)
    
    # Check if the last character is a zero
    if num_str[-1] == '0':
        # Move the zero to the beginning
        num_str = '0' + num_str[:-1]
    
    # Convert the string back to an integer
    return int(num_str)

# Function to calculate the satellite's position using the TLE data and observer's location
def get_satellite_position(tle_data, observer):
    # Define a satellite using its Two-Line Element (TLE) data
    # This is a placeholder TLE for GOES 16; you will need to use the current TLE for accurate calculations
    satellite_tle = tle_data

    # Create a satellite object
    satellite = ephem.readtle(*satellite_tle)

    # Compute the satellite's position from the observer's location
    satellite.compute(observer)

    # Extract and print the azimuth and elevation
    azimuth = satellite.az
    elevation = satellite.alt

    return azimuth, elevation

def calculate_dish_orientation():
    # Initialize the observer's location
    obs = initialize_observer(args.latitude, args.longitude)

    # Download the TLE data for the satellite
    tle_data = download_tle(args.norad_id)

    # Calculate the satellite's position
    azimuth, elevation = get_satellite_position(tle_data, obs)
    timestamp = ephem.now()

    azimuth_degrees = float(ephem.degrees(azimuth)) * (180.0 / math.pi)

    # Convert and scale elevation from radians to a value from 100 to 700
    elevation_degrees = float(ephem.degrees(azimuth)) * (180.0 / math.pi)
    elevation_scaled = ((elevation_degrees / 90.0) * 600) + 100

    print(f"Satellite {args.norad_id} is @ Azimuth: {azimuth_degrees:.1f}°, Elevation: {elevation_scaled:.2f} @ {time.strftime('%Y%m%d-%H%M%S')} UTC")

    return float(f'{azimuth_degrees:.1f}'), elevation_scaled

def get_current_signal_strength():

    send_command('SIGLEVEL', 1)
    out = ''
    time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(1).decode()
    if out != '':
        if(verbose):
            print("Return: " + out)
        return out.split('=')[1].split(' ')[1] #Return: Signal Strength = XXXX

def main():
    global ser
    global verbose
    ser = initialize_serial()
    verbose = args.verbose
    initialize_dish()
    az, el = calculate_dish_orientation()
    command_az = f"{int(float(f'{az * 100:.1f}')):04d}"
    corrected_az = move_zero(command_az)
    if(len(str(corrected_az)) < 4):
        temp_num = str(corrected_az)
        temp_num = '0' + temp_num[:-1]
        corrected_az = int(temp_num)

    print(f"Moving dish to Azimuth: {corrected_az}°, Elevation: {el:.2f}")
    if(verbose):
        print("Sending commands to dish...")
        print("Sending AZ command: " + f'AZ,{corrected_az}')
        print("Sending EL command: " + f'EL,{el:.0f}')
    send_command(f'AZ,{corrected_az}', 3)
    send_command(f'EL,{el:.0f}', 3)
    print("Dish is now pointing at specified coordinates.")
    signal_strength = get_current_signal_strength()
    if(int(signal_strength) < 25):
        print("No satellite signal detected :(, please check your dish's orientation and try again.")
        print("Signal strength: " + signal_strength)
        exit()
    else:
        print("Signal strength: " + signal_strength)
        print("Satellite lock achieved! Enjoy your packets!")

if __name__ == "__main__":
    main()