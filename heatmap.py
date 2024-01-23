import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Heatmap generator for TracVision L2 satellite dish scans.')
parser.add_argument('--scan_settings', metavar='scan_s', type=str, help='The path to the scan settings from your desired scan.')
parser.add_argument('--raw_data', metavar='scan_d', type=str, help='The path to the scan raw data from your desired scan.')

args = parser.parse_args()

print('Loading scan data.')
sky_data = np.loadtxt(args.raw_data)

print('Loading parameters of scan.')
scan_params = np.loadtxt(args.scan_settings)
az_start=int(scan_params[0])
az_end=int(scan_params[1])
el_start=int(scan_params[2])
el_end=int(scan_params[3])

cleaned_data = np.delete(sky_data, obj=0, axis=0)
cleaned_data = np.delete(cleaned_data, obj=0, axis=1)
#cleaned_data = sky_data
	
#set up custom axis labels
x=np.array([0,(az_end-az_start-1)/2,az_end-az_start-2])
az_range=np.array([az_end,(az_start+az_end)/2,az_start])
plt.xticks(x,az_range)
y=np.array([0,(el_end-el_start-1)/2,el_end-el_start-1])
el_range=np.array([el_end,(el_start+el_end)/2,el_start])
plt.yticks(y,el_range)

	

print('Processing heatmap...')


plt.imshow(cleaned_data, cmap='CMRmap')
plt.colorbar(location='bottom',label='RF Signal Strength')
plt.xlabel("Azimuth")
plt.ylabel("Elevation")
plt.title("Ku Band Scan via TracVision L2")



plt.show()