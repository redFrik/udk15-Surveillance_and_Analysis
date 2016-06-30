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
