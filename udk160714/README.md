own projects 1
--

various questions and examples that came up in class...

supercollider
--

```supercollider
//mouse area

//how to detect if mouse is inside a rectangle on the screen
(
{
    var mx= MouseX.kr(20, 500);  //arbitrary - could be screen dimension
    var my= MouseY.kr(20, 500);
    var a= (mx>120)*(mx<180);  //check to see if 120<x<180
    var b= (my>80)*(my<200);  //check to see if 80<y<200
    var trg= a*b;  //if a=1 and b=1 then 1 else 0
    Splay.ar(SinOsc.ar(400)*trg.lag(0.05));
}.play
)
```

```supercollider
//mouse delta

//use rate of change (mouse speed) to control frequency
//here we calculate the difference (-) between current
//and a delayed mouse position
(
{
    var mx= MouseX.kr(0, 1);
    var my= MouseY.kr(0, 1);
    var dx= mx-(DelayN.kr(mx, 0.1, 0.1));
    var dy= my-(DelayN.kr(my, 0.1, 0.1));
    [dx, dy].poll;
    LeakDC.ar(SinOsc.ar([dx, dy]*9999));
}.play
)

//version 2 - same but with lag and controlling
//phase and amplitude
(
{
    var mx= MouseX.kr(0, 1);
    var my= MouseY.kr(0, 1);
    var dx= mx-(DelayN.kr(mx, 0.1, 0.1)).lag(0.5);
    var dy= my-(DelayN.kr(my, 0.1, 0.1)).lag(0.5);
    LeakDC.ar(SinOsc.ar([200, 202], [dx, dy]*9999, [dx, dy]*2));
}.play
)

//version 3 - using the Slope of the mouse position
(
{
    var lag= 0.01;  //try different up to and above 1.0
    var mx= MouseX.kr(0, 1);
    var my= MouseY.kr(0, 1);
    var dx= Slope.kr(mx).lag(lag);
    var dy= Slope.kr(my).lag(lag);
    LeakDC.ar(SinOsc.ar([dx, dy]*999));
}.play
)
```

```supercollider
//six channel output

s.options.numChannels= 6;
s.reboot;
s.meter;

//how to pan (-1.0 to 1.0) a mono sound (Saw) in 6 channels
{PanAz.ar(6, Saw.ar(300), MouseX.kr(-1, 1), width: 2)}.play;
//look at the level meter window

//width above is the spread of the sound.  try different values.

//nice idea with a 'shadow' sound that follows.
//here a quieter noise is delayed 1sec and follows the saw tooth
//additional lag to make the shadow move less jerky
(
{
    PanAz.ar(6, Saw.ar(300), MouseX.kr(-1, 1), width: 2)
    +
    PanAz.ar(6, WhiteNoise.ar(0.05), DelayN.kr(MouseX.kr(-1, 1).lag(2), 1, 1))
}.play;
)
```

python
--

how to read a string from a textfile:

```python
nano test.txt  #write something in there and press ctrl+x to save and quit
python  #to start python
with open("test.txt", "r") as f:
    a= f.read()
a.rsplit()  #this should print the string from the file. rsplit removes trailing newlines (\n)
```

audio sniffer
--

easy to build device for listening to circuits... <http://www.openmusiclabs.com/projects/audio-sniffer/>

schematics are on the wiki

(thanks for the tip Till)

links
--

music and storytelling: <http://www.laurieanderson.com/gallery/#video>

recommended processing and supercollider tutorials: <http://funprogramming.org>
