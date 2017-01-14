more processing
--------------------

very good article about computer vision: <http://www.flong.com/texts/essays/essay_cvad/>

background removal
--

first see the processing example Background Subtraction that you find under Examples / Libraries / Video / Capture.

(press space to capture background)

opencv has this built in and also dynamically update the background reference.

```cpp
import processing.video.*;
import gab.opencv.*;

Capture video;
OpenCV opencv;

void setup() {
    size(640, 480);
    video = new Capture(this, width, height);
    video.start();
    opencv= new OpenCV(this, video.width, video.height);
    opencv.startBackgroundSubtraction(5, 3, 0.5);  //play with these settings
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    background(0);
    opencv.loadImage(video);
    opencv.updateBackground();
    image(opencv.getOutput(), 0, 0);
}
```

contours
--

removing background like above but also analyzing and drawing the countour.

```cpp
import processing.video.*;
import gab.opencv.*;

Capture video;
OpenCV opencv;

void setup() {
    size(640, 480);
    video = new Capture(this, width, height);
    video.start();
    opencv= new OpenCV(this, video.width, video.height);
    opencv.startBackgroundSubtraction(5, 3, 0.5);  //play with these settings
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    background(0);
    opencv.loadImage(video);
    opencv.updateBackground();
    //try adding more dilates and erodes here below
    opencv.dilate();  //first thicken the shape
    opencv.dilate();
    opencv.erode();  //then thin the shape again to close holes
    opencv.erode();
    fill(0, 255, 0);  //try commenting out
    stroke(255);
    for (Contour contour : opencv.findContours()) {
        contour.draw();
    }
}
```

movement detection
--

we can figure out the average movement in the total picture by first removing the background and then calculate how many white pixels showing.

in this example we also downsample to save on cpu and the resulting total is both displayed and sent to supercollider via osc.

```cpp
//total movement
import processing.video.*;
import gab.opencv.*;
import oscP5.*;
import netP5.*;

Capture video;
OpenCV opencv;
OscP5 oscP5;
NetAddress receiver;

int downscale= 4;  //try with 1, 2, 4, 8, 16 etc for different resolutions
void setup() {
    size(640, 480);
    video = new Capture(this, width/downscale, height/downscale);
    video.start();
    opencv= new OpenCV(this, video.width, video.height);
    opencv.startBackgroundSubtraction(5, 3, 0.8);  //play with these settings
    oscP5= new OscP5(this, 12000);
    receiver= new NetAddress("127.0.0.1", 57120);
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    stroke(255);
    opencv.loadImage(video);
    opencv.updateBackground();
    scale(downscale, downscale);
    PImage img= opencv.getOutput();
    long total= 0;
    for(int i= 0; i<img.pixels.length; i++) {
        total= total+int(brightness(img.pixels[i]));
    }
    total= total/255;
    image(img, 0, 0);
    text("total: "+total, 10, 20);
    sendOsc(total);
}
void sendOsc(long t) {
    OscMessage msg= new OscMessage("/total");
    msg.add(t);
    oscP5.send(msg, receiver);
}
```

```supercollider
//supercollider code for total movement
s.boot;
s.latency= 0.05;
(
Ndef(\snd, {|freq= 500, amp= 0|
    BLowPass4.ar(WhiteNoise.ar(amp), freq.lag, 0.5).dup;
}).play;
OSCdef(\total, {|msg|
    var t= msg[1];
    //msg.postln;  //debug
    Ndef(\snd).set(\amp, (t/1000).clip(0, 1), \freq, t.linexp(0, 5000, 200, 2000));
}, \total);
)
```

optical flow
--

this example will analyse the 'flow' or direction of all things moving in the camera image.
then the average of that will be sent out to supercollider via osc (as movement in x and y directions).

```cpp
//average optical flow
import processing.video.*;
import gab.opencv.*;
import oscP5.*;
import netP5.*;

Capture video;
OpenCV opencv;
OscP5 oscP5;
NetAddress receiver;

int downscale= 2;  //try with 1, 2, 4 and 8 for different resolutions
void setup() {
    size(1280, 480);
    video = new Capture(this, width/2/downscale, height/downscale);
    video.start();
    opencv= new OpenCV(this, video.width, video.height);
    oscP5= new OscP5(this, 12000);
    receiver= new NetAddress("127.0.0.1", 57120);
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    background(0);
    stroke(255);
    opencv.loadImage(video);
    opencv.calculateOpticalFlow();

    pushMatrix();
    scale(downscale, downscale);
    image(opencv.getOutput(), 0, 0);
    translate(width/downscale*0.5, 0);
    opencv.drawOpticalFlow();
    popMatrix();

    PVector averageFlow= opencv.getAverageFlow();
    stroke(0, 255, 0);
    translate(width*0.25, height*0.5);
    line(0, 0, averageFlow.x*100, averageFlow.y*100);
    sendOsc(averageFlow.x, averageFlow.y);
}
void sendOsc(float x, float y) {
    OscMessage msg= new OscMessage("/avgflow");
    msg.add(x);
    msg.add(y);
    oscP5.send(msg, receiver);
}
```

```supercollider
//supercollider code for average optical flow
s.boot;
s.latency= 0.05;
(
Ndef(\snd, {|freq= 500, pan= 0, amp= 0|
    Pan2.ar(BLowPass4.ar(WhiteNoise.ar(amp), freq.lag, 0.5), pan);
}).play;
OSCdef(\avgflow, {|msg|
    var x= msg[1];
    var y= msg[2];
    //msg.postln;  //debug
    Ndef(\snd).set(\amp, (x.abs+y.abs).clip(0, 1), \pan, (y*3).clip(-1, 1), \freq, (0-y).linexp(-1, 1, 200, 2000));
}, \avgflow);
)
```

optical flow examples
--

<http://www.memo.tv/bodypaint/>

```cpp
//bodypaint remake
import processing.video.*;
import gab.opencv.*;

Capture video;
OpenCV opencv;

int downscale= 4;  //try with 2, 4 and 8 for different resolutions
float colorSpeed= 0.4;
int trail= 4;  //0-255
float thresh= 1;

float hue= 0.0;
void setup() {
    size(640, 480);
    video = new Capture(this, width/downscale, height/downscale);
    video.start();
    opencv= new OpenCV(this, video.width, video.height);
    colorMode(HSB, 255);
    background(0);
    noStroke();
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    fill(0, trail);
    rect(0, 0, width, height);
    hue= hue+colorSpeed;
    fill(int(hue)%256, 255, 255);
    opencv.loadImage(video);
    opencv.calculateOpticalFlow();
    for (int x= 0; x<opencv.width; x++) {
        for (int y= 0; y<opencv.height; y++) {
            PVector flow= opencv.getFlowAt(x, y);
            float m= flow.mag();
            if(m>thresh) {
                rect(x*downscale, y*downscale, m-thresh, m-thresh);
            }
        }
    }
}
```

kinect
==

for the below to work you will need a kinect sensor.

Daniel Shiffman - Processing and Kinect Tutorial <https://www.youtube.com/playlist?list=PLRqwX-V7Uu6ZMlWHdcy8hAGDy6IaoxUKf>

install the 'Open Kinect for Processing' library in processing.

```cpp
//basic example demonstrating different modes
import org.openkinect.processing.*;
Kinect kinect;
int mode= 0;  //press space to cycle mode
void setup() {
    size(640, 480);
    kinect= new Kinect(this);
    kinect.initDepth();
    kinect.initVideo();
    println(kinect.width, kinect.height);  //report dimension of kinect camera
    //also try these...
    //kinect.enableMirror(true);  //or false
    //kinect.setTilt(10);  //0 - 30 degrees
}
void draw() {
    if(mode==0) {
        kinect.enableIR(false);
        image(kinect.getVideoImage(), 0, 0);
        text("plain video", 10, 20);
    } else if(mode==1) {
        kinect.enableIR(true);
        image(kinect.getVideoImage(), 0, 0);
        text("video with infra red", 10, 20);
    } else if(mode==2) {
        kinect.enableColorDepth(false);
        image(kinect.getDepthImage(), 0, 0);
        text("depth image", 10, 20);
    } else if(mode==3) {
        kinect.enableColorDepth(true);
        image(kinect.getDepthImage(), 0, 0);
        text("depth image with colour", 10, 20);
    }
}
void keyPressed() {
    if(key==' ') {
        mode++;
        if(mode>3) {
            mode= 0;
        }
    }
}
```

easy kinect skeleton
--

install Synapse from <http://synapsekinect.tumblr.com>

follow Eli Fieldsteel's SuperCollider Tutorial: 13. Xbox Kinect <https://www.youtube.com/watch?v=dbSTq_UsFK4>

```supercollider
s.boot;
s.latency= 0.05;

//very basic supercollider with synaps
//make sure synapse is running, start this code and then go and stand in special 'skeleton' position
(
Ndef(\snd1, {|freq= 100, amp= 0, cf= 0.1|
    BLowPass4.ar(Saw.ar(freq, amp), cf, 0.1).dup;
}).play;
Ndef(\snd2, {|freq= 100, amp= 0, cf= 0.1|
    BLowPass4.ar(Saw.ar(freq, amp), cf, 0.1).dup;
}).play;
n= NetAddr("127.0.0.1", 12346);  //receive from synapse application
OSCdef(\righthand, {|msg|
    //msg.postln;  //debug
    Ndef(\snd1).set(
        \cf, msg[1].linexp(-1500, 1500, 50, 5000),  //x pos is about -1500 to 1500
        \freq, msg[2].linexp(-800, 800, 50, 5000),  //y pos is about -800 to 800
        \amp, msg[3].linexp(0, 4500, 1, 0.01)  //z pos is about 0 to 4500 - here mapped to amplitude
    );
}, '/righthand_pos_world', nil, 12345);
OSCdef(\lefthand, {|msg|
    //msg.postln;  //debug
    Ndef(\snd2).set(
        \cf, msg[1].linexp(-1500, 1500, 5000, 50),  //x pos is about -1500 to 1500
        \freq, msg[2].linexp(-800, 800, 50, 5000),  //y pos is about -800 to 800
        \amp, msg[3].linexp(0, 4500, 1, 0.01)  //z pos is about 0 to 4500 - here mapped to amplitude
    );
}, '/lefthand_pos_world', nil, 12345);
r= Routine.run({
    inf.do{
        n.sendMsg("/righthand_trackjointpos", 2);
        n.sendMsg("/lefthand_trackjointpos", 2);
        2.wait;  //keep synapse tracking alive by sending msg every other second
    };
});
)

//cmd+. to stop
```

advanced kinect skeleton
--

skeleton tracking on osx...

(from <https://github.com/Sensebloom> and <https://github.com/totakke/homebrew-openni>)

* `brew install openni`
* `brew tap totakke/openni`
* `brew install sensor-kinect`
* `brew install nite`
* `git clone https://github.com/Sensebloom/OSCeleton`
* `cd OSCeleton`
* `sudo ln -s /usr/local/Cellar/openni/1.5.7.10/include/ni /usr/include/ni`  #create a temp symlink
* `make`
* `sudo rm /usr/include/ni`  #remove temp symlink

to start...

* `./osceleton -p 57120`  #start sending osc to supercollider

```supercollider
//supercollider code
//this simple example demonstrates how to use a kinect
//to count people in a (small) room and fade in/out sound accordingly
OSCFunc.trace

s.boot;
s.latency= 0.05;

(
Ndef(\snd, {|user= 0|
    SinOsc.ar([400, 404]+(user*100), 0, user.lagud(1, 5));
}).play;
OSCdef(\newuser, {|msg|
    msg.postln;
    Ndef(\snd).set(\user, 1);
}, \new_user);
OSCdef(\lostuser, {|msg|
    msg.postln;
    Ndef(\snd).set(\user, 0);
}, \lost_user);
)
```

links
--

more about kinect... <http://neurogami.com/presentations/KinectForArtists/>

using infra red camera and lights to find silhouette... <http://www.tmema.org/messa/diagrams/old/concert_2_screen/messa_optical_configurations.pdf> <https://www.youtube.com/watch?v=STRMcmj-gHc>

for tracking hands... <http://leapmotion.com>

bonus
--

color modes in processing.

HSB= hue, saturation, brightness

```cpp
int cnt= 0;
void setup() {
    size(640, 480);
    colorMode(HSB, 255);  //compare with this commented out (the default is RGB)
}
void draw() {
    //because we set HSB mode instead of the default RGB
    //the first value (our cnt) now controls hue instead
    //or red
    background(cnt, 255, 255);  //cycle through hue
    cnt= cnt+1;
    if(cnt==256) {
        cnt= 0;
    }
}
```
