GeoIPbulk
=========

Description
-----------
A simple script to retrieve some useful information such as location and occurence number for a provided IP list

Features
--------
* Using the Maxmind GeoIP python API (http://dev.maxmind.com/geoip/legacy/downloadable) to retrieve some IP location information
* Counting the number of occurence for an IP in the list
* Generating the output as csv

Usage
-----
Pass the IP list (1 dotted quad IP per line) via stdin or from a specified file (-i).  
The processed dump can be collected at stdout or to a specified file (-o).

### Options
```
$ python geoipbulk.py -h
Usage: geoipbulk.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUT, --input=INPUT
                        IP list file (stdin if not specified)
  -o OUTPUT, --output=OUTPUT
                        csv output filename (stdout if not specified)
  -c, --count           count IP occurence
  -r, --reverse         reverse sort order
  -s, --skip-header     do not print the csv header
```

### Examples
```
$ python geoipbulk.py -i ip_list.txt
IP;COUNTRY_NAME
130.136.254.21;Italy
203.110.240.22;India
202.95.202.24;Papua New Guinea
152.3.138.4;United States
123.234.32.27;China
94.81.48.5;Italy
150.176.182.31;United States
80.88.242.32;Bahrain
...

$ cat ip_list.txt| python geoipbulk.py  -c -r
COUNT;IP;COUNTRY_NAME
4;122.152.183.103;Japan
3;152.3.138.4;United States
3;128.238.88.64;United States
3;128.223.8.111;United States
3;128.223.8.112;United States
3;80.153.156.21;Germany
```

Requirements
------------
* python >= 2.6
* 'python-geoip' apt package

Copyright and license
---------------------
GeoIPBulk is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

GeoIPBulk is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with GeoIPBulk. 
If not, see http://www.gnu.org/licenses/.

Contact
-------
* Thomas Debize < tdebize at mail d0t com >
