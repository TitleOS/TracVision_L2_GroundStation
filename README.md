# TracVision L2 RV Satellite - Microwave Imaging
A collection of Python utility scripts and a PoC script for microwave imaging the sky using a TracVision L2 Portable RV Satellite over Serial.

### Scripts
* serial_terminal.py: A rudimentary serial terminal for interfacing with the L2 controller over serial, compatible with Linux and Windows.
* scan.py: A rudimentary PoC that builds on my research to hopefully develop a script capable of automatically microwave imaging the sky (or section of the sky) via returned RF signal strength.
* heatmap.py: Using scan-settings and raw-data recorded during a scan by scan.py, heatmap.py can generate a matlib heatmap plot of the sky section scanned.
* target_geosync.py: By specifying a satellite's NORAD ID, your latitude and longitude, this script can automatically calculate the azimuth and elevation of the satellite from your current location, using this data to automatically point the dish at it's location.
* More To Come


### Notes
Be slow using target_geosync.py, currently the script redownloads the NORAD TLE every run, and multiple rapid runs will result in your IP being temporarily banned from celestrak.org
```
403 - Forbidden: Access is denied.
We have detected excessive downloads for files in the /NORAD/elements directory and access has been temporarily blocked. Access will be automatically restored once the excessive downloads have ceased for 2 hours.

Please note that orbital data files are only checked for updates every 2 hours and most orbital data only updates 2-3 times a day (or less). Please check your scripts to ensure they are operating properly.
```

