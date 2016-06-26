supercollider and processing
--------------------

detuned oscillators...

```
s.boot

Ndef(\saw, { Saw.ar([400, 400]) }).play;  //no detuning - same frequency in left and right speaker

//detune
Ndef(\saw, { Saw.ar([400, 404]) }).play;  //4 Hz difference
Ndef(\saw, { Saw.ar([400, 402]) }).play;
Ndef(\saw, { Saw.ar([400, 400.2]) }).play;
Ndef(\saw, { Saw.ar([400, 800.1]) }).play;  //detune also works over octaves
Ndef(\saw, { Saw.ar([400, 600.1]) }).play;  //and other intervals
```
drone
--

```
//supercollider code
s.boot;

Ndef(\drone).fadeTime= 5;  //five seconds cross fade time
Ndef(\drone, {var f= [300, 301, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f))))}).play;
Ndef(\drone, {var f= [300, 301, 150, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f))))}).play;  //adding frequencies
Ndef(\drone, {var f= [600, 300, 301, 150, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f))))}).play;
Ndef(\drone, {var f= [600, 300, 301, 150, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f, 0, LFTri.ar(1/f*11)), LFTri.ar(2/f*10).exprange(500, 5000)))}).play;
Ndef(\drone, {var f= [600.1, 300, 301, 150, 99]; Splay.ar(BLowPass4.ar(LFSaw.ar(f+LFTri.kr(4/f), 0, LFTri.ar(1/f*11)), LFTri.ar(2/f*10).exprange(500, 5000)))}).play;
```

matching processing graphics?

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

or...

```cpp
void setup() {
    size(800, 600);
}
void draw() {
    background(0);
    stroke(255);
    translate(width/2, height/2);
    for (int i= 0; i<100; i++) {
        line(cos(frameCount*0.01+i)*200, sin(frameCount*0.011+i)*200, 2, 2);
        rotate(frameCount*0.0001);
    }
}
```

more drones
--

```
//op-art
//drone

Ndef(\mydrone, { BLowPass4.ar( Saw.ar([400, 404]) ) }).play

Ndef(\mydrone, { Splay.ar( BLowPass4.ar( Saw.ar([400, 50, 600, 700, 800]) )) }).play

Ndef(\mydrone, { Splay.ar( BLowPass4.ar( Saw.ar([400+2, 50+1, 599.9, 700, 800.4]) )) }).play

Ndef(\mydrone, { Splay.ar( BLowPass4.ar( Saw.ar([400+MouseX.kr(-2, 2), 50, 600, 700, 800]) )) }).play

Ndef(\mydrone).fadeTime= 2

Ndef(\mydrone, { Splay.ar( BLowPass4.ar( Saw.ar([400+2, 50+1, 599.9, 700, 800.4], LFTri.ar(1)) )) }).play

Ndef(\mydrone, { Splay.ar( BLowPass4.ar( Saw.ar([400+2, 50+1, 599.9, 700, 800.4], LFTri.ar([1,2,3,4,5])) )) }).play

Ndef(\mydrone).stop
Ndef(\mydrone).play

(
Ndef(\mydrone, { Splay.ar( BLowPass4.ar(
    Saw.ar([400+2, 50+1, 599.9, 700, 800.4],
    LFTri.ar([1.001,2.001,3*0.999,4,5]/40)) )) }).play;
Ndef(\mydrone2, { Splay.ar( BLowPass4.ar(
    Saw.ar([400+2, 50+1, 599.9, 700, 800.4]+1,
    LFTri.ar([1.001,2.001,3*0.999,4,5]/40)) )) }).play;
Ndef(\mydrone3, { Splay.ar( BLowPass4.ar(
    Saw.ar([400+2, 50+1, 599.9, 700, 800.4]*MouseX.kr(0.5, 2).round(0.25),
    LFTri.ar([1.001,2.001,3*0.999,4,5]/40)) )) }).play;
)

NdefMixer(s)

//automation...
(
Routine({
    1.wait;
    Ndef(\mydrone3).play;
    2.wait;
    Ndef(\mydrone3).stop;
    //etc...
}).play;
)
```

moiré patterns
--

compare this...

```cpp
void setup() {
    size(800, 600);
}
void draw() {
    background(0);
    stroke(255);
    for(int i= 0; i<200; i++) {
        line(0, i*2, width, i*2);
    }
}
```

with this...

```cpp
void setup() {
    size(800, 600);
}
void draw() {
    background(0);
    stroke(255);
    for(int i= 0; i<200; i++) {
        line(0, i*2, width, i*2.1);
    }
}
```

also try adding `noSmooth();` in setup to turn off anti-aliasing. it will give a more 'pixely' effect that often works well with these types of interferensens.

rotate...

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

rotate with mouse control...

```cpp
void setup() {
    size(800, 600);
    //noSmooth();  //turn off anti-aliasing
}
void draw() {
    background(0);
    stroke(255);
    translate(width/2, height/2);
    for(int i= 0; i<200; i++) {
        line(0, 0, 100+i, 100+i);
        rotate(mouseX/10000.0);
    }
}
```

more mouse control...

```cpp
void setup() {
    //fullScreen();
    size(800, 600);
    //noSmooth();  //turns off anti-aliasing
}
void draw() {
    background(0, 255, 0);
    stroke(255, 0, 255);
    for (int i= 0; i<200; i++) {
        line(0, i*map(mouseX, 0, width, 2, 4), width, i*3);
    }
    for (int i= 0; i<200; i++) {
        line(i*map(mouseY, 0, height, 2, 4), 0, i*3, height);
    }
}
```

```cpp
void setup() {
    size(800, 600, FX2D);
    //noSmooth();  //turn off anti-aliasing
}
void draw() {
    background(0);
    stroke(255);
    translate(width/2, height/2);
    for(int i= 0; i<200; i++) {
        line(0, 0, 100+i, 100+i);
        rotate(frameCount* -0.0001);
    }
    for(int i= 0; i<200; i++) {
        line(0, 0, 100+i, 100+i);
        rotate(frameCount* 0.0001);
    }
}
```

rectangles...

```cpp
void setup() {
    size(800, 600, FX2D);
    //noSmooth();  //turn off anti-aliasing
}
void draw() {
    background(0);
    stroke(255);
    noFill();
    translate(width/2, height/2);
    for(int i= 0; i<200; i++) {
        rect(0, 0, 100+i, 100+i);
        rotate(frameCount* -0.0001);
    }
    for(int i= 0; i<200; i++) {
        rect(0, 0, 100+i, 100+i);
        rotate(frameCount* 0.0001);
    }
}
```

ellipses...

```cpp
void setup() {
    size(800, 600, FX2D);
    //noSmooth();  //turn off anti-aliasing
}
void draw() {
    background(0);
    stroke(255);
    noFill();
    translate(width/2, height/2);
    for(int i= 0; i<200; i++) {
        ellipse(10, 100, 100+i, 100+i);
        rotate(frameCount* -0.0001);
    }
    for(int i= 0; i<200; i++) {
        ellipse(10, 100, 100+i, 100+i);
        rotate(frameCount* 0.0001);
    }
}
```

links
--

processing (and p5) tutorials... <https://www.youtube.com/user/shiffman>
