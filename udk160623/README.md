supercollider and processing
--------------------

drone
--

```
//supercollider code
s.boot;

Ndef(\drone).fadeTime= 10;
Ndef(\drone, {f= [300, 301, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f))))}).play;
Ndef(\drone, {f= [300, 301, 100, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f))))}).play;
Ndef(\drone, {f= [600, 300, 301, 100, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f))))}).play;
Ndef(\drone, {f= [600, 300, 301, 100, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f*11)), LFTri.ar(2/f*10).exprange(500, 5000)))}).play;
Ndef(\drone, {f= [600, 300, 301, 100, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f+LFTri.kr(4/f), 0, LFTri.ar(1/f*11)), LFTri.ar(2/f*10).exprange(500, 5000)))}).play;
```

matching graphics?

```cpp
void setup() {
    size(800, 600);
}
void draw() {
    background(0);
    stroke(255);
    translate(width/2, height/2);
    for (int i= 0; i<400; i++) {
        line(200+i, 200+i, 2, 2);
        rotate(frameCount*0.0001);
    }
}
```
