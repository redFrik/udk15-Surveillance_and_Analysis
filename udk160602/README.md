python
--------------------

open terminal and type `python`.

play around.

see previous python experiments... <https://github.com/redFrik/udk12-Back_to_basics/tree/master/udk141127>

to exit type `quit()`.

for the examples below we will need to install two python packages. type (in the terminal)...

`easy_install pyosc psutil`

if you get permission problems try `sudo easy_install pyosc psutil`

on **osx** you might here be asked to install xcode command line tools.

and on **linux** you might first also need to `sudo apt-get update` and `sudo apt-get install python-dev python-setuptools`

or (a better way on both osx and linux assuming you have python-pip installed), you can also get them with pip like this...

`pip install pyosc psutil`

cpu measurements
--

type `python` and then `import psutil`

if you don't see any errors you can continue, else the psutil package didn't install properly. (try rebooting your mac if you had to install xcode.)

now we can get data about what our computer is doing.

`psutil.cpu_percent()`  #to see cpu usage in percent (run multiple times)

`psutil.cpu_percent(percpu= True)`  #same but for each individual cpu core

`psutil.cpu_count()`  #how many cpu cores do you have

`psutil.virtual_memory()`  #how much ram memory

`psutil.virtual_memory().free`  #how much is free

`psutil.disk_usage('/')`  #disk space

`psutil.net_io_counters()`  #how much data has your network sent

`psutil.net_connections()`  #open network connections (note needs `sudo python` on osx)

`psutil.boot_time()`  #time since you booted your computer

etc etc. see <https://pypi.python.org/pypi/psutil>

we can use the above commands in python and send the resulting cpu load data to processing or supercollider via osc.

* make sure you download the code in this github directory (easiest if you go up one level and click 'clone or download' and then 'download zip')
* now open and start the processing sketch `cpuloads.pde` (if problem make sure you have the OscP5 library installed)
* open terminal and cd to the folder udk160526. e.g. `cd ~/Downloads/udk15-Surveillance_and_Analysis/udk160602`
* then type `python cpuloads.py`
* you should see numbers and rectangles change according to your cpu load.
* last close the processing sketch and open `cpuloads.scd` in supercollider

(note: after you have run the supercollider example, you should recompile to close the network port. else the processing example will not run again)

wifi signal strength
--

<http://www.nearfield.org/2011/02/wifi-light-painting>

on **osx** you can get data about your current wifi network using the following command in terminal...

`/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I`

and to perform a scan of nearby networks...

`/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s`

(another way is to use the CoreWLAN framework. see the python code provided here `python rssi_objc_osx.py`)

under **linux** use...

`iwconfig wlan0`

or...

`cat /proc/net/wireless`

and to scan nerby networks...

`sudo iwlist wlan0 scanning`

we can use the above commands in python and send the resulting wifi strength data to processing or supercollider via osc.

* make sure you download the code in this github directory (easiest if you go up one level and click 'clone or download' and then 'download zip')
* now open and start the processing sketch `wifistatus.pde` (if problem make sure you have the OscP5 library installed)
* open terminal and cd to the folder udk160526. e.g. `cd ~/Downloads/udk15-Surveillance_and_Analysis/udk160602`
* then on **osx** type `python wifistatus_osx.py`
* and on **linux** type `python wifistatus_linux.py`
* you should see numbers in the upper left corner change and the green bargraph change according to your rssi.
* last close the processing sketch and open `wifistatus.scd` in supercollider

(note: after you have run the supercollider example, you should recompile to close the network port. else the processing example will not run again)

links
--

use opencv with python for advanced image analysis... <https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html>

more on linux wifi... <http://www.cyberciti.biz/tips/linux-find-out-wireless-network-speed-signal-strength.html>
