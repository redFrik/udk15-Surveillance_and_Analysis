introduction and overview
--------------------

* links to previous semesters... <http://redfrik.github.io/udk00-Audiovisual_Programming/>
* and dates + times for this course... <https://github.com/redFrik/udk15-Surveillance_and_Analysis> <-save this page

course software
--

* [SuperCollider](http://supercollider.github.io/download.html)
* [Processing](http://processing.org)
* [Python](https://www.python.org)
* and perhaps some other programs like [Arduino](http://www.arduino.cc) and [Audacity](http://audacityteam.org)

processing
--

first download and install processing 3 from <http://processing.org>.
then open sketch / import library / add library and install the following three libraries...

* Video
* OpenCV
* OscP5

mouse
--

now try this basic example in processing...

```cpp
void setup() {
    fullScreen();  //'esc' key to exit
}
void draw() {
    rect(mouseX, mouseY, mouseX-pmouseX, mouseY-pmouseY);
}
```

examples
--

now try the following examples that you can find in the menu file / examples / libraries / video / capture...

* BackgroundSubtraction
* BrightnessThresholding
* BrightnessTracking
* FrameDifferencing

and then the following examples from file / examples / contributed libraries / opencv for processing...

* BackgroundSubtraction (different from above)
* LiveCamTest
* WhichFace

optical flow
--

this example takes the optical flow example that comes with opencv, adds camera input and osc output to supercollider.

first install OpenCV and OscP5 libraries for Processing.

* open processing and the sketch menu
* select `Import Library...` and then `Add Library...`
* search for 'opencv' and install
* search for 'oscp5' and install

processing code:

```cpp
//from opencv examples
//adapted for camera and processing3
//also sends osc
import gab.opencv.*;
import processing.video.*;
import oscP5.*;
import netP5.*;

OpenCV opencv;
Capture video;
OscP5 oscP5;
NetAddress receiver;

void setup() {
    size(640, 240);
    video = new Capture(this, 320, 240);
    opencv = new OpenCV(this, 320, 240);
    video.start();
    oscP5= new OscP5(this, 12000);
    receiver= new NetAddress("127.0.0.1", 57120);  //ip address and port to send to, 57120= sc
}

void draw() {
    background(0);
    opencv.loadImage(video);
    opencv.calculateOpticalFlow();

    image(video, 0, 0);
    translate(video.width, 0);
    stroke(255, 0, 0);
    opencv.drawOpticalFlow();

    PVector aveFlow = opencv.getAverageFlow();
    int flowScale = 50;

    stroke(255);
    strokeWeight(2);
    line(video.width/2, video.height/2, video.width/2 + aveFlow.x*flowScale, video.height/2 + aveFlow.y*flowScale);

    sendOscData(aveFlow.x, aveFlow.y);
}

void captureEvent(Capture c) {
    c.read();
}

void sendOscData(float x, float y) {
    OscMessage msg= new OscMessage("/flow");
    msg.add(x);
    msg.add(y);
    oscP5.send(msg, receiver);
}
```

supercollider code:

```
//test
(
OSCdef(\flow, {|msg| msg.postln}, \flow);
)

//sound
(
s.waitForBoot{
    Ndef(\snd, {|x= 0, y= 0| SinOsc.ar([x, y].lag(0.05)*999, 0, [x, y].lag(0.1)/3)}).play;
    OSCdef(\flow, {|msg| Ndef(\snd).set(\x, msg[1], \y, msg[2])}, \flow);
};
)

//trigger
(
s.waitForBoot{
    var syn= SynthDef(\ping, {|t_trig= 0, x= 0, y= 0|
        var env= EnvGen.ar(Env.perc(0.001, 0.1), t_trig);
        var snd= SinOsc.ar(x*100+400);
        Out.ar(0, Pan2.ar(snd*env, y.poll));
    }).play;
    OSCdef(\flow, {|msg|
        var x= msg[1];
        var y= msg[2];
        if(x.abs>1 or:{y.abs>1}, {
            syn.set(\t_trig, 1, \x, x, \y, y);
        });
    }, \flow);
};
)
```

traceroute
--

(might only work on osx and linux)

open terminal and type `traceroute www.google.de` and then compare that with `traceroute www.google.jp`

try your own webpage.

bluetooth
--

<https://github.com/adafruit/adafruit-bluefruit-le-desktop>

faceosc
--

written in openframeworks. osx binary... <https://github.com/kylemcdonald/ofxFaceTracker/releases>
but you should also be able to grab the project and run it under windows+linux if you have oF installed.

the default output port is 8338. so to listen to it in supercollider do something like this...

```
OSCdef(\gesture_eye_right, {|msg| msg.postln}, '/gesture/eye/right', recvPort:8338)
OSCdef(\gesture_eyebrow_left, {|msg| msg.postln}, '/gesture/eyebrow/left', recvPort:8338)
OSCdef(\gesture_eyebrow_right, {|msg| msg.postln}, '/gesture/eyebrow/right', recvPort:8338)
OSCdef(\gesture_jaw, {|msg| msg.postln}, '/gesture/jaw', recvPort:8338)
OSCdef(\gesture_nostrils, {|msg| msg.postln}, '/gesture/nostrils', recvPort:8338);
```

netcat
--

to listen to udp (osc) on some port run this in terminal...

`nc -ul 8338`

note: one can only have one udp port open at a time so sometimes programs will complain that the port is already in use.

