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
```

```
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

```
(
//timbre tracking
//track how 'clean' the input sound is.  try whistle vs blow (sine vs noise)
Ndef(\ttrack, {
    var buf= LocalBuf(2048).clear;
    var fft= FFT(buf, SoundIn.ar);
    SpecCentroid.kr(buf, fft).poll;  //will post values - the lower the cleaner signal
});
)

Ndef(\ttrack.stop;
```

```
//--detect sound

(
Ndef(\onOff, {|thresh= 0.09, time= 0.2, amp= 1|
    var src= SoundIn.ar*amp;
    //var src= BPF.ar(SoundIn.ar*amp, 150, 1); //variant with bandpass filter
    var off= DetectSilence.ar(src, thresh, time);
    var on= 1-off;		//invert
    on.poll;
});
)



//--recording sounds
~buffers= Array.fill(10, {Buffer.alloc(s, 44100*3)});  //make ten, three seconds long buffers

(
//a single buffer recorder. records into ~buffers[x]. change x to select recording buffer
Ndef(\recorder, {
    var src= SoundIn.ar;
    RecordBuf.ar(src, ~buffers[5], loop:0);
});
)
~buffers[5].plot
~buffers[5].play



//--detector with recorder - miniature i'm sitting in a room
~buffer= Buffer.alloc(s, 44100*3);  //make a single three seconds long buffer

(
Ndef(\automaticRecorder, {|thresh= 0.09, time= 0.2, amp= 1|
    var src= SoundIn.ar*amp;
    //var src= BPF.ar(SoundIn.ar*amp, 150, 1); //variant with bandpass filter
    var off= DetectSilence.ar(src, thresh, time);
    var on= 1-off;		//invert
    on.poll;
    RecordBuf.ar(src, ~buffer, loop:0, trigger: on);
});
)
~buffer.play  //turn up the volume and trigger manually once in a while
//you should be able to record the recorded sound over and over

```
