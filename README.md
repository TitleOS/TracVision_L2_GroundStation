# TracVision L2 RV Satellite Dish - Ground Station
A collection of Python scripts for interfacing with the TracVision L2 RV Motorized Satellite Dish over serial. Functionality currently includes targeting geosynchronous satellites and (Very Roughly) tracking moving satellites.

### Scripts
* serial_terminal.py: A rudimentary serial terminal for interfacing with the L2 controller over serial, compatible with Linux and Windows.
* target_geosync.py: By specifying a satellite's NORAD ID, your latitude and longitude, this script can automatically calculate the azimuth and elevation of the satellite from your current location, using this data to automatically point the dish at it's location via the serial interface.
* More To Come

### How to:
* target_geosync.py: `python target_geosync.py --sat_name GOES18 --latitude 34.68462 --longitude -101.77635` OR `python target_geosync.py --norad_id 41866 --latitude 34.68462 --longitude -101.77635 --verbose True --finetune True` - Will calculate the GeoSync satellite's rough azimuth and elevation based on the provided latitude and longitude, before using the serial interface to point the L2 satellite dish.

* target_geosync.py: `python target_geosync.py --norad_id 59051 --latitude 34.68462 --longitude -101.77635 --track True` - Will calculate the target (moving) satellite's rough azimuth and elevation based on the provided latitude and longitude, before using the serial interface to point the L2 satellite dish at the satellite. The script will then continuously monitor the signal level and adjust it's azimuth and elevation as needed to maintain a lock on the satellite until it moves below the horizon.

* target_geosync.py: `python target_geosync.py --sat_name GOES18 --latitude 34.68462 --longitude -101.77635 --debug True` - Will calculate GOES18's azimuth and elevation based on the provided latitude and longitude, before *printing* the values to the terminal, instead of sending it over a serial interface. This is useful to testing changes to the script without having to have the satellite dish attached and powered.  




### Notes
target_geosync.py caches TLE data to a local file called `tle_cache.json` for 2 hours. This is more than sufficient for tracking GeoSync satellites, however if you would like to force a redownload of TLE data early, simply delete tle_cache.json and rerun target_geosync.py. You should be aware that Celestrak is pretty aggressive when it comes to rate-limiting. They themselves recommend only updating TLE data not more than every 2 hours.
* `54-0195A_TVL2_5.03.pdf` is the original TracVision L2 Owner Manual, which was essential to the creation of these scripts and reverse engineering the serial interface. Specific pages 64-69 cover serial interfacing.


### Additional Resources
* https://rvsatellite.com/support/kvh/antenna-commands/