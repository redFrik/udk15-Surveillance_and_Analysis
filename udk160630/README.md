webcams
--------------------

install the IPcapture library for the following to work

```cpp
import ipcapture.*;
IPCapture cam;

void setup() {
    size(640, 480);  //must be the same as the stream dimensions
    //cam = new IPCapture(this, "http://37.35.189.15:8080/mjpg/video.mjpg", "", "");  //last two are username and passwd
    //cam = new IPCapture(this, "http://93.165.142.237:80/mjpg/video.mjpg", "", "");
    cam = new IPCapture(this, "http://109.190.32.217:82/axis-cgi/mjpg/video.cgi?camera=&amp;resolution=640x480", "", "");
    cam.start();
}
void draw() {
    if (cam.isAvailable()) {
        cam.read();
        image(cam, 0, 0);
    }
}
```

find more open cameras here... <http://www.insecam.org>

to access the raw url you can control click the camera, select 'inspect' and then figure out the ip by looking at the img html tag. or select view source in your webbrowser and search for the url.

for example: `<img id="image0" src="http://93.165.142.237:80/mjpg/video.mjpg?COUNTER" class="thumbnailimgfullsize" alt="" title="Click here to enter the camera located in Denmark, region Hovedstaden, Copenhagen">`

shows you what the raw ip of the camera is and what you should copy: http://93.165.142.237:80/mjpg/video.mjpg

note that not all cameras will work within processing.

multiple cameras...

```cpp
import ipcapture.*;
IPCapture cam, cam2, cam3, cam4;
void setup() {
    size(640, 480);
    cam = new IPCapture(this, "http://109.190.32.217:82/axis-cgi/mjpg/video.cgi?camera=&amp;resolution=640x480", "", "");
    cam2 = new IPCapture(this, "http://93.165.142.237:80/mjpg/video.mjpg", "", "");
    cam3 = new IPCapture(this, "http://81.12.190.218:80/cgi-bin/camera?resolution=640&amp;amp;quality=1&amp;amp;Language=0&amp;amp;1467291044", "", "");
    cam4 = new IPCapture(this, "http://209.54.68.94:82/cgi-bin/camera?resolution=640&amp;amp;quality=1&amp;amp;Language=0&amp;amp;1467291257", "", "");
    cam.start();
    cam2.start();
    cam3. start();
    cam4. start();
}
void draw() {
    if (cam.isAvailable()) {
        cam.read();
    }
    if (cam2.isAvailable()) {
        cam2.read();
    }
    if (cam3.isAvailable()) {
        cam3.read();
    }
    if (cam4.isAvailable()) {
        cam4.read();
    }
    cam.filter(THRESHOLD, 0.3);
    cam2.filter(THRESHOLD, 0.3);
    cam3.filter(THRESHOLD, 0.3);
    cam4.filter(THRESHOLD, 0.3);
    image(cam, 0, 0, 320, 240);
    image(cam2, 320, 0, 320, 240);
    image(cam3, 0, 240, 320, 240);
    image(cam4, 320, 240, 320, 240);
}
```

recording to disk...

```cpp
import ipcapture.*;
IPCapture cam;

void setup() {
    size(640, 480);
    cam = new IPCapture(this, "http://109.190.32.217:82/axis-cgi/mjpg/video.cgi?camera=&amp;resolution=640x480", "", "");
    cam.start();
}
void draw() {
    if (cam.isAvailable()) {
        cam.read();
        image(cam, 0, 0);
        if (mousePressed) {  //click and hold mouse to record 
            saveFrame();
        }
    }
}
```

then select 'Show Sketch Folder' (cmd+k) to get to the all recorded images. and under Tools menu use 'Movie Maker' to turn them into a movie.

playing with filter...

```cpp
import ipcapture.*;
IPCapture cam;

void setup() {
    size(640, 480);
    cam = new IPCapture(this, "http://109.190.32.217:82/axis-cgi/mjpg/video.cgi?camera=&amp;resolution=640x480", "", "");
    cam.start();
}
void draw() {
    if (cam.isAvailable()) {
        cam.read();
        cam.filter(THRESHOLD, map(mouseX, 0, width, 0, 1));  //mouse set threshold
        tint(0, 255, 0);
        image(cam, 0, 0);
    }
}
```

using opencv together with ip cameras...

```cpp
//opencv with ipcapture
import gab.opencv.*;
import ipcapture.*;

IPCapture video;
OpenCV opencv;

void setup() {
    size(640, 480);
    video = new IPCapture(this, "http://109.190.32.217:82/axis-cgi/mjpg/video.cgi?camera=&amp;resolution=640x480", "", "");
    video.start();
    opencv= new OpenCV(this, video.width, video.height);
    opencv.gray();
    noFill();
}
void draw() {
    if (video.isAvailable()) {
        video.read();
        opencv.threshold(int(map(mouseX, 0, width, 0, 100)));  //threshold mousex
        opencv.loadImage(video);
        image(video, 0, 0);
        stroke(0, 255, 0);
        for (Contour contour : opencv.findContours(true, true)) {
            beginShape();
            for (PVector point : contour.getPolygonApproximation().getPoints()) {
                vertex(point.x, point.y);
            }
            endShape();
        }
    }
}
```

using your own webcamera...

```cpp
import processing.video.*;

Capture cam;

void setup() {
    size(640, 480);
    println(Capture.list());
    cam= new Capture(this, width, height);
    cam.start();
}
void draw() {
    if (cam.available()) {
        cam.read();
        cam.filter(ERODE);
        cam.filter(ERODE);
        cam.filter(ERODE);
        image(cam, 0, 0);
    }
}
```

setting up your own cam
--

requirements:

* raspberry pi with jessie
* usb webcamera
* ethernet cable

follow the instructions here... <https://pimylifeup.com/raspberry-pi-webcam-server/>

```
sudo apt-get update
sudo apt-get upgrade
lsusb #check to see that the usb webcamera is there
sudo apt-get install motion
sudo nano /etc/motion/motion.conf
    daemon on
    width 640
    height 480
    framerate 100
    stream_localhost off
    stream_maxrate 15
    output_pictures off
    ffmpeg_output_movies off
sudo nano /etc/default/motion
    start_motion_daemon=yes
sudo service motion start
```

now test it by browsing to port 8081 on your rpi (e.g. http://192.168.1.2:8081)

links
--

Eyes of Laura, Janet Cardiff, 2004 <http://www.docam.ca/en/case-studies/eyes-of-laura-j-cardiff.html>
