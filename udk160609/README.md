more python
--------------------

network scanner
--

* make sure you download the code in this github directory (easiest if you go up one level and click 'clone or download' and then 'download zip')
* now open and start the processing sketch `networks_scanner.pde` (if problem make sure you have the OscP5 library installed)
* open terminal and cd to the folder udk160609. e.g. `cd ~/Downloads/udk15-Surveillance_and_Analysis/udk160609`
* then type `python networks_scanner_osx.py` (or `sudo python networks_scanner_linux.py` if you are running linux)
* if you have problems make sure you have the pyosc python package installed (see last week)
* if it works you should see white text in processing

faker
--

here we try out a python package called faker. see the docs: <http://faker.readthedocs.io/en/latest/>

open terminal type:

`sudo easy_install fake-factory`

(or if you have pip installed `pip install fake-factory`)

then start python...

`python`

`from faker import Faker`  #if installation above worked you should see no error
`f= Faker()`  #create a new faker object
`f.name()`  #return a name
`f.name()`  #another one
`f.name()`  #etc
`f.address()`  #a fake address
`f= Faker('de_DE')`  #create another object localized to germany
`f.name()`  #should return a german name
`print f.name()`  #pretty printing
`print f.address()`  #pretty printing

this last example will print out 100 fake name+addresses

```python
for i in range(100):
    print f.name()
    print f.address()
    print '---------'
```

text
--

playing with text in processing...

```cpp
//basic
void setup() {
    size(800, 600);
    background(0);
}
void draw() {
    //background(0);  //0-255
    textSize(50);
    //fill(0, 255, 127);  //text colour
    text("hallo", mouseX, mouseY);
}
```

```cpp
//grid
void setup() {
    size(800, 600);
    background(0);
    noSmooth();
}
void draw() {
    background(0);
    for (int i= 0; i<50; i++) {
        for (int j= 0; j<20; j++) {
            //rotate(0.001);
            //textSize(map(i, 0, 50, 2, 80));
            text(i+j, map(i, 0, 50, 0, width), map(j, 0, 20, 0, 200));
            //text((i+j+frameCount)%255, map(i, 0, 50, 0, width), map(j, 0, 20, 100, 700));
            //text(char((i+j+frameCount)%255), map(i, 0, 50, 0, width), map(j, 0, 20, 100, 700));
        }
    }
}
```

```cpp
//text with mousecontrol in 3d
void setup() {
    size(800, 600, P3D);
    background(0);
}
void draw() {
    //background(0);
    translate(width/2, height/2);  //reset 0,0 to center screen
    textSize(60);
    rotateZ(frameCount*0.1);
    rotateX(frameCount*0.08);
    rotateY(frameCount*0.04);
    fill(frameCount%255);
    text("hello", 0, 0, mouseX);
}
```

bonus
--

this basic example show how to send osc data (here mouse x and y) from processing to supercollider

```cpp
//processing code...

import oscP5.*;
import netP5.*;
OscP5 oscP5;
NetAddress supercollider= new NetAddress("127.0.0.1", 57120);  //ip supercollider

void setup() {
    size(800, 600);
    OscProperties properties= new OscProperties();
    oscP5= new OscP5(this, 9999);
}
void draw() {
    OscMessage msg= new OscMessage("/data");
    msg.add(mouseX);
    msg.add(mouseY);
    oscP5.send(msg, supercollider);
}
```

```
//supercollider code...

//example1 - plain synthdef
s.boot;

(
SynthDef(\mysaw, {|amp= 0, freq= 500|
    var snd= BLowPass4.ar(Saw.ar(freq, amp), 900, 0.5);
    Out.ar(0, snd!2);
}).add;
)

a= Synth(\mysaw)
a.set(\amp, 0.1)  //test
a.set(\amp, 0)

(
OSCdef(\mouse, {|msg|
    //msg.postln;  //debug
    a.set(\amp, msg[1].linlin(0, 800, 0, 1));
    a.set(\freq, msg[2].linexp(0, 600, 100, 1000));
}, \data);
)

a.free
OSCdef(\mouse).free

//example2 - samke but using ndef
s.boot;

(
Ndef(\mysnd, {|amp= 0, freq= 500|
    BLowPass4.ar(Saw.ar(freq, amp), 900, 0.5)!2;
}).play;
)

Ndef(\mysnd).set(\amp, 0.1)  //test
Ndef(\mysnd).set(\amp, 0)

(
OSCdef(\mouse, {|msg|
    //msg.postln;  //debug
    Ndef(\mysnd).set(\amp, msg[1].linlin(0, 800, 0, 1));
    Ndef(\mysnd).set(\freq, msg[2].linexp(0, 600, 100, 1000));
}, \data);
)

//now change it while it is playing
(
Ndef(\mysnd, {|amp= 0, freq= 500|
    SinOsc.ar(freq, 0, amp)!2;
}).play;
)

(
Ndef(\mysnd, {|amp= 0, freq= 500|
    RLPF.ar(WhiteNoise.ar(amp), freq, 0.05)!2;
}).play;
)

Ndef(\mysnd).clear
OSCdef(\mouse).free
```

advanced
--

using nmap to scan for computers and open ports on a network

`brew install nmap` or for ***linux*** `sudo apt-get install nmap`

list connected computers on your network:

`nmap -sn 192.168.1.0/24 -oG - | awk '/Up$/{print $2, $3}'` #edit ip to be match your network root ip (.0)

list connected computers on your network that have an open ssh port:

`nmap -p 22 --open -sV 192.168.1.0-255` #take care to not run this on unknown/open networks

list connected computers on your network that have supercollider running:

`sudo nmap -p 57120 --open -sU 192.168.1.0/24 -oG - | awk '/Up$/{print $2, $3}'`

now install python-nmap and try out the `discover.py` and `discover.scd` example

links
--

<https://saxenarajat99.wordpress.com/2015/01/27/nmap-tutorial/>

<https://github.com/vinta/awesome-python>
