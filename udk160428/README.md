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
```
