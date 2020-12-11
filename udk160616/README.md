more supercollider
--------------------

a tuned 'ringing' filter can be used to as a simple spectrum analyzer.

```supercollider
s.boot

{BPF.ar(WhiteNoise.ar, 1500, 1)}.play

//BPF= bandpass filter

{Mix(BPF.ar(WhiteNoise.ar, [800, 900, 1200], 0.01))!2}.play

{Impulse.ar(2)!2}.play

{Mix(BPF.ar(Impulse.ar(2), [1800, 900, 1200], 0.01))*15!2}.play

{Mix(BPF.ar(Impulse.ar([2, 2.1, 2.2, 3, 4]), [1800, 900, 1200, 5000, 500], 0.01))*15!2}.play

{Mix(BPF.ar(SoundIn.ar, [1800, 900, 1200], 0.01))*15!2}.play

{Mix(BPF.ar(DelayN.ar(SoundIn.ar, 5, 5), [1800, 900, 1200], 0.001))*20!2}.play

{Mix(BPF.ar(DelayN.ar(SoundIn.ar, 2, 2), [1800, 900, 1200, 500, 600, 700]*MouseX.kr(0.01, 3, 1), 0.001))*20!2}.play

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

//many ringing filters
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

```supercollider
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

```supercollider
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

this example will analyze sound in supercollider and send over three parameters to processing. the three parameters are freqiency (pitch), amplitude (volume) and centroid (timbre or how 'noisy' the signal is)

supercollider code:

```supercollider
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

extra - 3d
--

install PeasyCam library for Processing and use this example with the spectrum graphics sc code above

```cpp
//click and drag the mouse
import peasy.*;
import oscP5.*;
import netP5.*;
OscP5 oscP5;
PeasyCam cam;
float data[]= new float[0];
void setup() {
    size(800, 600, P3D);
    colorMode(HSB, 100);
    cam= new PeasyCam(this, 500);
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
        pushMatrix();
        fill(a*100, 100, 100);
        translate(0, a*height);
        box(data[i]*width, height/data.length, 50);
        popMatrix();
    }
}
```

markov chains
--

markov chains -> guided randomness

```cpp
//very simple markov chain example

float[][] arr= {  //weights
    {0.1, 0.7, 0.1, 0.1},  //each line should add up to 1.0
    {0.1, 0.1, 0.7, 0.1},  //each line is a state and descibes the
    {0.2, 0.1, 0.1, 0.6},  //likelyhood of going to another state
    {0.7, 0.2, 0.1, 0.0}   //so state 3 (this line) has 60% chance of going back to state 0, 20% going to state 1, 10% to state 2 and 0% chance of staying put at state 3
};

int state= 0;  //starting state

void setup() {
    size(640, 480);
    frameRate(2);
}

void draw() {
    background(0);

    //--draw all states as outlines
    noFill();
    stroke(255);
    for(int i= 0; i<arr.length; i++) {
        rect(i*100+100, 50, 20, 20);
    }

    //--fill current state
    fill(255);
    rect(state*100+100, 50, 20, 20);

    //--pick new state
    float[] weights= arr[state];  //find the weights for current state
    float rand= random(1.0);  //pick a random number 0.0-1.0
    float sum= 0.0;  //this will step-by-step add up to rand
    for(int i= 0; i<weights.length; i++) {
        sum= sum+weights[i];
        if(sum>rand) {
            state= i;  //sum added up to greater than rand and we found the new state 
            break;
        }
    }
}
```

works really well for generating natural texts. also you can analyze a text/sound/gesture/picture etc and get the table of weights from that. then regenerate a similar text/sound/gesture/picture that's very similar but not always the same. variations on a theme.

read more...

<https://en.wikipedia.org/wiki/Markov_chain>

<https://projects.haykranen.nl/markov/demo/>

and a similar example in supercollider...

```supercollider
(
//simple markov chain in supercollider
//here each state is represented as a note
var arr= [  //weights
    [0.1, 0.7, 0.1, 0.1],
    [0.1, 0.1, 0.7, 0.1],
    [0.2, 0.1, 0.1, 0.6],
    [0.6, 0.2, 0.1, 0.1]
];
var synth= {|freq= 400, t_trig= 0| SinOsc.ar(freq, 0, 0.5)*EnvGen.ar(Env.perc, t_trig)!2}.play;
var state= 0;  //starting state
Routine.run({
    inf.do{
        var weights= arr[state];  //find the weights for current state
        var rand= 1.0.rand;  //pick a random number 0.0-1.0
        var sum= 0.0;  //this will step-by-step add up to rand
        state= weights.detectIndex{|w|
            sum= sum+w;
            sum>rand;
        };
        synth.set(\t_trig, 1, \freq, state*100+300);  //map state to freq and trigger sound
        0.5.wait;
    };
});
)
```

try changing the weights in arr

```supercollider
(
//five states example
//with a tendency to get 'stuck' at the top note (state= 4)
var arr= [  //weights
    [0.05, 0.7, 0.1, 0.1, 0.05],  //state 0
    [0.1, 0.1, 0.7, 0.05, 0.05],
    [0.2, 0.1, 0.1, 0.5, 0.1],
    [0.6, 0.2, 0.1, 0.05, 0.05],
    [0.03, 0.03, 0.02, 0.02, 0.9]  //state 4
];
var synth= {|freq= 400, t_trig= 0| SinOsc.ar(freq, 0, 0.5)*EnvGen.ar(Env.perc, t_trig)!2}.play;
var state= 0;  //starting state
Routine.run({
    inf.do{
        var weights= arr[state];  //find the weights for current state
        var rand= 1.0.rand;  //pick a random number 0.0-1.0
        var sum= 0.0;  //this will step-by-step add up to rand
        state= weights.detectIndex{|w|
            sum= sum+w;
            sum>rand;
        };
        synth.set(\t_trig, 1, \freq, state*100+300);  //map state to freq and trigger sound
        0.1.wait;
    };
});
)
```

and a last example showing how to rewrite the weights and number of states while it is running...

```supercollider
(
//12 states random weights to start with
var synth= {|freq= 400, t_trig= 0| SinOsc.ar(freq, 0, 0.5)*EnvGen.ar(Env.perc, t_trig)!2}.play;
~state= 0;
~arr= Array.fill(12, {Array.fill(12, {[0.9, 0.1].choose}).normalizeSum}).postln;
Routine.run({
    inf.do{
        var weights= ~arr[~state];  //find the weights for current state
        var rand= 1.0.rand;  //pick a random number 0.0-1.0
        var sum= 0.0;  //this will step-by-step add up to rand
        ~state= weights.detectIndex{|w|
            sum= sum+w;
            sum>rand;
        };
        synth.set(\t_trig, 1, \freq, ~state*100+300);  //map state to freq and trigger sound
        0.1.wait;
    };
});
)

//run this while it is playing
(
~state= 0;
~arr= Array.fill(4, {Array.fill(4, {[0.9, 0.1].choose}).normalizeSum}).postln;
)

(
~state= 0;
~arr= Array.fill(8, {Array.fill(8, {[10, 0.1, 0].choose}).normalizeSum}).postln;
)
```

the method `normalizeSum` just makes sure all the weights add up to 1.0
