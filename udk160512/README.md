basic processing
--------------------

this assumes you have downloaded and installed processing 3 from <http://processing.org>.
and also installed the following three processing libraries...

* Video
* OpenCV
* OscP5

(open sketch / import library / add library and search for them in the contribution manager)

you will also need some sort of camera connected to your computer (the built-in webcamera is fine)

camera
--

copy and paste the code below into processing. explore the example and get familiar with it.

```cpp
//--minimal camera example
import processing.video.*;

Capture video;

void setup() {
    size(320, 240);
    video = new Capture(this, width, height);  //create a video object
    video.start();
}
void captureEvent(Capture video) {  //automatically called each time there is a new image read by the camera
    video.read();  //update the video image with a new frame from the camera
}
void draw() {
    image(video, 0, 0);  //draw the current video image starting at the upper left corner
}
```

try replacing `image(video, 0, 0);` with `image(video, mouseX, mouseY);`

and replace `video.read();` with `if(mousePressed) {video.read();}`

also play with size by changing `size(320, 240);` to `size(1024, 240);`

and last `video = new Capture(this, width, height);` to `video = new Capture(this, width, 800);`

opencv
--

a template example for camera with opencv. this locates the brightest pixel and draws a circle around it.

```cpp
//--minimal opencv example
import processing.video.*;
import gab.opencv.*;

Capture video;
OpenCV opencv;

void setup() {
    size(320, 240);
    video = new Capture(this, width, height);
    video.start();
    opencv= new OpenCV(this, width, height);
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    opencv.loadImage(video);
    image(opencv.getOutput(), 0, 0);  //note: draws the output of the opencv image
    //image(video, 0, 0);  //to instead draw the video uncomment this
    PVector loc = opencv.max();
    stroke(255, 0, 0);
    strokeWeight(4);
    noFill();
    ellipse(loc.x, loc.y, 10, 10);
}
```

try replacing `PVector loc = opencv.max();` to `PVector loc = opencv.min();` to track the darkest pixel.

try to uncomment both image lines so that only the circle is drawn. add `background(0);` if you want to clear the screen each frame.

also try drawing something different. try changing `ellipse(loc.x, loc.y, 10, 10);` to `rect(loc.x, loc.y, 50, 50);` or to `line(loc.x, loc.y, width*0.5, height*0.5);`

filters
--

often you will want to adjust and prepare the image before doing the analysis. this example demonstrates how to apply filters to the image and change contrast, brightness etc. with this technique you can compensate for what the camera gives you - note: more professional cameras have settings for white balance, focus, brightness, contrast etc. in cheap webcameras this is often done automatically and thereby makes it a bit harder to use for camera tracking. so turn off auto white balance if you can.

```cpp
//--process the image to improve tracking
import processing.video.*;
import gab.opencv.*;

Capture video;
OpenCV opencv;

void setup() {
    size(320, 240);
    video = new Capture(this, width, height);
    video.start();
    opencv= new OpenCV(this, width, height);
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    opencv.loadImage(video);
    opencv.brightness(-80);  //-255 to 255
    opencv.contrast(2.5);  //1.0 means no change
    opencv.blur(8);  //number of pixels
    image(opencv.getOutput(), 0, 0);
    PVector loc = opencv.max();
    stroke(255, 0, 0);
    strokeWeight(4);
    noFill();
    ellipse(loc.x, loc.y, 10, 10);
}
```

play with the settings

also try tracking the darkest pixel (change `max` to `min` in the pvector line)

try changing `opencv.contrast(2.5);` to `opencv.contrast(mouseX*3.0/width);` to get mouse control

try adding `opencv.flip(OpenCV.HORIZONTAL)` and also try with `OpenCV.VERTICAL` and `OpenCV.BOTH` as arguments

set a threshold by adding `opencv.threshold(50);` or with mouse control: `opencv.threshold(mouseY);`

add one or more `opencv.dilate();`

and then take dilate away and add some `opencv.erode();` instead

note that the order in which you apply these filters matter. e.g. blurring and then eroding is different from eroding and then blurring.

now see <http://atduskgreg.github.io/opencv-processing/reference/> - click on OpenCV. read about the different methods and try out some of them.

preview
--

sometimes it is handy to see multiple video images at the same time - to compare effects and what the camera sends versus what openvs outputs etc.
this example show how to set up three images side by side. it can easily be adapted to more/fewer.

```cpp
//--preview
import processing.video.*;
import gab.opencv.*;

Capture video;
OpenCV opencv;

void setup() {
    size(960, 240);  //3x1
    video = new Capture(this, width/3, height);
    video.start();
    opencv= new OpenCV(this, width/3, height);
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    opencv.loadImage(video);
    image(opencv.getOutput(), 0, 0);  //draw pure opencv left
    opencv.blur(8);
    opencv.threshold(50);
    image(opencv.getOutput(), 320, 0);  //draw image after blur+thresh center
    image(video, 640, 0);  //and raw camera input right
    PVector loc = opencv.max();
    stroke(255, 0, 0);
    strokeWeight(4);
    noFill();
    ellipse(loc.x+320, loc.y, 10, 10);  //offset circle to center image
}
```

smoothing
--

another important technique is to smooth or lag the output xy data. here is one easy way to do that.

```cpp
//--basic smoothing of data
import processing.video.*;
import gab.opencv.*;

Capture video;
OpenCV opencv;
PVector now= new PVector(160, 120);
float smooth= 0.02;  //lower is more smooth, 1.0 is no change

void setup() {
    size(320, 240);
    video = new Capture(this, width, height);
    video.start();
    opencv= new OpenCV(this, width, height);
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    opencv.loadImage(video);
    image(opencv.getOutput(), 0, 0);  //note: draws the output of the opencv image
    PVector loc = opencv.max();
    now.x= now.x+((loc.x-now.x)*smooth);  //lag in x dimension
    now.y= now.y+((loc.y-now.y)*smooth);  //lag in y dimension
    stroke(255, 0, 0);
    strokeWeight(4);
    noFill();
    ellipse(now.x, now.y, 10, 10);
}
```

here `loc` can be seen as the target and `now` the current xy position.  `smooth` adds a bit of the difference between the two to `now` and thereby the circle approces the target in smaller and smaller steps.

try with different values for smooth.

bonus - advanced
--

send the smoothed x y data to supercollider via osc.

```
//--basic osc
import processing.video.*;
import gab.opencv.*;
import oscP5.*;
import netP5.*;

Capture video;
OpenCV opencv;
OscP5 oscP5;
NetAddress receiver;

PVector now= new PVector(160, 120);
float smooth= 0.02;  //lower is more smooth, 1.0 is no change

void setup() {
    size(320, 240);
    video = new Capture(this, width, height);
    video.start();
    opencv= new OpenCV(this, width, height);
    oscP5= new OscP5(this, 12000);
    receiver= new NetAddress("127.0.0.1", 57120);
}
void captureEvent(Capture video) {
    video.read();
}
void draw() {
    opencv.loadImage(video);
    opencv.blur(8);
    image(opencv.getOutput(), 0, 0);  //note: draws the output of the opencv image
    PVector loc = opencv.max();
    now.x= now.x+((loc.x-now.x)*smooth);  //lag in x dimension
    now.y= now.y+((loc.y-now.y)*smooth);  //lag in y dimension
    stroke(255, 0, 0);
    strokeWeight(4);
    noFill();
    ellipse(now.x, now.y, 10, 10);
    sendOscData(now.x, now.y, loc.x, loc.y);  //send dot location and analysed location
}
void sendOscData(float x, float y, float tx, float ty) {
    OscMessage msg= new OscMessage("/maxLoc");
    msg.add(x);
    msg.add(y);
    msg.add(tx);
    msg.add(ty);
    oscP5.send(msg, receiver);
}
```

and then in supercollider run this...

```
//sound
(
s.waitForBoot{
    Ndef(\snd, {|x= 0, y= 0, tx= 0, ty= 0|
        //here we use circle location x y to set frequencies of two oscillators
        //and the absolute difference between target and circle as amplitude
        SinOsc.ar([x, y]+500, 0, [tx-x, ty-y].abs/100);
    }).play;
    OSCdef(\max, {|msg|
        //the msg that comes in here is x, y location of circle
        //and then target location (the output of opencv max)
        msg.postln;
        //set the synth parameters with the incoming data
        Ndef(\snd).set(\x, msg[1], \y, msg[2], \tx, msg[3], \ty, msg[4]);
    }, \maxLoc);
};
)
```
