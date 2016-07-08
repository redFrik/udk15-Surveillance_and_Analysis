sdr
--

software defined radio:

<http://www.rtl-sdr.com/about-rtl-sdr/>

<https://dolske.wordpress.com/2014/03/25/hacks-all-the-way-down/> (read the long list of possibilities)

radio spectrum:

see the table of frequencies here... <https://en.wikipedia.org/wiki/Radio_spectrum>

web applications:

<http://websdr.org> here you can find some free online radios to use. for example <http://dj3le.spdns.de:8901>

<http://sdr.hu>

(use soundflower to get the sound into supercollider - see under [cubic](#cubic) below)

gui applications:

Gqrx SDR <http://gqrx.dk>

Cubic SDR <http://cubicsdr.com>

or sdr for maxmsp: <https://github.com/tkzic/maxradio>

then there's also the more advanced gnuradio <http://gnuradio.org>.

cubic
--

note: these instructions are for osx and for it to work you will also need a DVB-T TV tuner usb dongle or other sdr capable device. i used a [logilink VG0002A](http://logilink.de/Produkte_LogiLink/DVB-T/USB_20_DVB-T_Empfaenger/DVB-T_USB_20_Receiver_fuer_digital_TV_und_Radio.htm)

* download cubic sdr
* install [soundflower](https://github.com/mattingalls/Soundflower/releases/)
* start cubic sdr and tune in to some signal
* set audio output from cubic sdr to soundflower (2ch)
* open system preferences and set audio input to soundflower (2ch). audio output should be build-in.
* start supercollider and boot the server
* now with `{SoundIn.ar([0, 1])}.play` you should hear the radio.
* experiment with filters, delays, distortion etc.

flightradar
--

<https://www.flightradar24.com/>

ads-b
--

you can set up and run your own flight radar. to access ADS-B (flight data) use the [dump1090](https://github.com/antirez/dump1090) program.

install dump1090 on a raspberry pi by following the instructions at <http://www.satsignal.eu/raspberry-pi/dump1090.html> or <https://ferrancasanovas.wordpress.com/2013/09/26/dump1090-installation/>

to start it i used...

`./dump1090 --interactive --net --net-beast --net-ro-port 31001 --net-http-port 8088`

then open a browser and go to rpi's ip on port 8088.  e.g. `http://192.168.1.3:8088`

you can also install in on osx following the instructions here: <http://www.mactopics.de/2016/03/07/ads-b-dump1090-auf-os-x-el-capitan-installieren/>

on osx start it from terminal with `./dump1090 --interactive --net`

links
--

some topics we discussed...

<http://danieltemkin.com/Tutorials> glitch tutorials

<http://interface.khm.de/index.php/lab/interfaces-advanced/radio-signal-strength-sensor/>

<http://blog.riyas.org/2014/06/a-simple-24ghz-spectrum-analyser-arduino-lcd-shield.html>
