more supercollider
--------------------

a tuned 'ringing' filter can be used to as a simple spectrum analyzer.

```
s.boot;

(
{
    var freq= 300;  //try changing/adding frequency
    var in= SoundIn.ar;
    var ring= BPF.ar(in, freq, 0.01);
    var mix= Limiter.ar(Mix(ring)*25);
    ring.dup(2);
}.play;
)


//same but with mouse control
(
{
    var freq= MouseX.kr(100, 3000, 1);
    var in= SoundIn.ar;  //also try with Impulse.ar(1, 0, 100)
    var ring= BPF.ar(in, freq, 0.01);
    var mix= Limiter.ar(Mix(ring)*25);
    ring.dup(2);
}.play;
)
```


many ringing filters

```
(
{
    var freqs= [400, 500, 600, 700]*MouseX.kr(0.5, 3, 1);  //try changing/adding frequencies
    var in= SoundIn.ar;
    var rings= freqs.collect{|f| BPF.ar(in, f, 0.01)};
    var mix= Limiter.ar(Mix(rings)*25);
    rings.dup(2);
}.play;
)
```

spectrum graphics
--

supercollider code:

```
(
var n= NetAddr("127.0.0.1", 9000);
{
    var freqs= [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100];  //try changing/adding frequencies
    var in= SoundIn.ar;
    var rings= freqs.collect{|f| BPF.ar(in, f, 0.01)};
    var trackers= rings.collect{|r| Amplitude.kr(r, 0.01, 1).lincurve(0, 1, 0.001, 1, -4)};
    var mix= Limiter.ar(Mix(rings)*25);
    SendReply.kr(Impulse.kr(60), '/bands', trackers);
    rings.dup(2);
}.play;
OSCdef(\bands, {|msg|
    //msg.postln;
    n.sendMsg(\toProcessing, *msg[3..]);
}, \bands);
)
```

processing code:

```cpp
import oscP5.*;
import netP5.*;
OscP5 oscP5;
float data[]= new float[0];
void setup() {
    size(800, 600);
    colorMode(HSB, 100);
    OscProperties properties= new OscProperties();
    properties.setListeningPort(9000);  //osc receive port (from sc)
    oscP5= new OscP5(this, properties);
}
void oscEvent(OscMessage msg) {
    if (msg.checkAddrPattern("/toProcessing")) {
        data= new float[msg.arguments().length];
        for (int i= 0; i<msg.arguments().length; i++) {
            data[i]= msg.get(i).floatValue();
        }
    }
}
void draw() {
    background(0);
    stroke(0);
    for(int i= 0; i<data.length; i++) {
        float a= i/float(data.length);
        fill(a*100, 100, 100);
        rect(0, a*height, data[i]*width, height/data.length);
    }
}
```

pitch tracking
--

supercollider code:

```
(
var n= NetAddr("127.0.0.1", 9000);
{
    var in= SoundIn.ar;
    var tracker= Pitch.kr(in);
    var freq= tracker[0];
    var flag= tracker[1];
    SendReply.kr(Impulse.kr(60)*flag, '/freq', freq);
}.play;
OSCdef(\freq, {|msg|
    //msg.postln;
    n.sendMsg(\toProcessingFreq, msg[3]);
}, \freq);
)
```

processing code:

```cpp
import oscP5.*;
import netP5.*;
OscP5 oscP5;
float freq= 0.0;
void setup() {
    size(800, 600);
    OscProperties properties= new OscProperties();
    properties.setListeningPort(9000);  //osc receive port (from sc)
    oscP5= new OscP5(this, properties);
    background(0);
}
void oscEvent(OscMessage msg) {
    if (msg.checkAddrPattern("/toProcessingFreq")) {
        freq= msg.get(0).floatValue();
    }
}
void draw() {
    stroke(255);
    point(frameCount%width, map(freq, 60, 4000, height, 0));
    if(frameCount%width==0) {
        background(0);
    }
}
```

more
--

supercollider code:

```
(
var n= NetAddr("127.0.0.1", 9000);
{
    var in= SoundIn.ar;
    var tracker= Pitch.kr(in);
    var freq= tracker[0];
    var flag= tracker[1];
    var amp= Amplitude.kr(in, 0.01, 0.1);
    var chain= FFT(LocalBuf(2048), in);
    var cent= SpecCentroid.kr(chain);
    SendReply.kr(Impulse.kr(60), '/more', [freq*flag, amp, cent]);
}.play;
OSCdef(\more, {|msg|
    //msg.postln;
    n.sendMsg(\toProcessingMore, *msg[3..]);
}, \more);
)
```

processing code:

```cpp
//this will draw three parameters
import oscP5.*;
import netP5.*;
OscP5 oscP5;
float freq= 0.0;
float amp= 0.0;
float cent= 0.0;
void setup() {
    size(800, 600);
    OscProperties properties= new OscProperties();
    properties.setListeningPort(9000);  //osc receive port (from sc)
    oscP5= new OscP5(this, properties);
    background(0);
}
void oscEvent(OscMessage msg) {
    if (msg.checkAddrPattern("/toProcessingMore")) {
        freq= msg.get(0).floatValue();
        amp= msg.get(1).floatValue();
        cent= msg.get(2).floatValue();
    }
}
void draw() {
    stroke(255, 0, 0);  //red is freq
    point(frameCount%width, map(freq, 60, 4000, height, 0));
    stroke(255, 255, 255);  //white is amp
    point(frameCount%width, map(amp, 0, 1, height, 0));
    stroke(0, 255, 0);  //green is centroid
    point(frameCount%width, map(cent, 100, 10000, 0, height));
    if (frameCount%width==0) {
        background(0);
    }
}
```
