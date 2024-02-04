# TracVision L2 RV Satellite - Microwave Imaging
A collection of Python utility scripts and a PoC script for microwave imaging the sky using a TracVision L2 Portable RV Satellite over Serial.

### Scripts
* serial_terminal.py: A rudimentary serial terminal for interfacing with the L2 controller over serial, compatible with Linux and Windows.
* scan.py: A rudimentary PoC that builds on my research to hopefully develop a script capable of automatically microwave imaging the sky (or section of the sky) via returned RF signal strength.
* heatmap.py: Using scan-settings and raw-data recorded during a scan by scan.py, heatmap.py can generate a matlib heatmap plot of the sky section scanned.
* target_geosync.py: By specifying a satellite's NORAD ID, your latitude and longitude, this script can automatically calculate the azimuth and elevation of the satellite from your current location, using this data to automatically point the dish at it's location.
* More To Come

### How to:
* target_geosync.py: `python target_geosync.py --sat_name GOES18 --latitude 34.68462 --longitude -101.77635` OR `python target_geosync.py --norad_id 41866 --latitude 34.68462 --longitude -101.77635 --verbose True --debug True`


### Notes
target_geosync.py caches TLE data to a local file called `tle_cache.json` for 2 hours. This is more than sufficient for tracking GeoSync satellites, however if you would like to force a redownload of TLE data early, simply delete tle_cache.json and rerun target_geosync.py. You should be aware that Celestrak is pretty aggressive when it comes to rate-limiting. They themselves recommend only updating TLE data not more than every 2 hours.
* `54-0195A_TVL2_5.03.pdf` is the original TracVision L2 Owner Manual, which was essential to the creation of these scripts and reverse engineering the serial interface. Specific pages 64-69 cover serial interfacing.


### Additional Resources
* https://rvsatellite.com/support/kvh/antenna-commands/