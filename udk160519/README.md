basic supercollider
--------------------

this assumes you have downloaded and installed supercollider from <http://supercollider.github.io/download>.


```
s.boot;
```

```
(
//amplitude tracking
//this example tracks amplitude around 'freq' hz and play a sine for 'dur' seconds
Ndef(\atrack, {|thresh= 0.1, dur= 4, freq= 200, rq= 1, atk= 0.1, rel= 1|
    var snd= SinOsc.ar([400, 404]);
    var trk= Amplitude.kr(BPF.ar(SoundIn.ar, freq, rq))>thresh;
    var gate= Trig.kr(trk, dur);
    gate.poll;
    snd*gate.lagud(atk, rel);
}).play;
);

Ndef(\atrack).gui;  //opens a gui where you can tune the tracker

Ndef(\atrack).stop;


(
//pitch tracking
//this example tracks if pitch matches 'freq' hz and if so plays a sine
Ndef(\ptrack, {|range= 20, dur= 4, freq= 200, atk= 0.1, rel= 1|
    var snd= SinOsc.ar([400, 404]);
    var pt= Pitch.kr(SoundIn.ar);
    var pitch= pt[0];
    var found= pt[1];
    var gate= InRange.kr(pitch*found, freq-range, freq+range);
    (pitch*found).poll;
    snd*gate.lagud(atk, rel);
}).play;
);

Ndef(\ptrack).gui;  //opens a gui where you can tune the tracker

Ndef(\ptrack).stop;
```
