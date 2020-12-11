basic supercollider
--------------------

this assumes you have downloaded and installed supercollider from <https://supercollider.github.io/download>.


```supercollider
s.boot  //you always need to run this to make sound

"hello"

2+600

{SinOsc.ar(MouseX.kr([400, 600], 4000, 1))}.play

cmd+.  //to stop

{Saw.ar(MouseX.kr([400, 600], 4000, 1))}.play

{LFTri.ar(MouseX.kr([400, 600], 4000, 1))}.play

{Pulse.ar(MouseX.kr([400, 600], 4000, 1))}.play

100.do{{Pulse.ar(MouseX.kr([Rand(400), 600], Rand(4000), 1))/100}.play}

cmd+m  //to show level meters

{Pulse.ar( Pitch.kr(SoundIn.ar)[0] ).dup}.play
{Saw.ar( Pitch.kr(SoundIn.ar)[0] ).dup}.play
{LFTri.ar( Pitch.kr(SoundIn.ar)[0] ).dup}.play
{SinOsc.ar( Pitch.kr(SoundIn.ar)[0] ).dup}.play

{Pulse.ar( Pitch.kr( DelayN.ar(SoundIn.ar, 1, 1))[0].lag(0.02) ).dup}.play

{Pulse.ar( Amplitude.kr(SoundIn.ar).lag(0.1)* 4000 ).dup}.play

{Pulse.ar( Amplitude.kr( DelayN.ar(SoundIn.ar, 1, 1)).lag(0.1)* 4000 ).dup}.play

{Pulse.ar( 400 ).dup * Amplitude.kr(SoundIn.ar).lag(4) }.play

{Pulse.ar( 400 ).dup * Amplitude.kr(SoundIn.ar).lagud(0.001, 4) }.play

{DelayN.ar(SoundIn.ar, 2, 2)}.play  //delay mic input for 2 seconds
```

examples
--

```supercollider
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
Ndef(\atrack).clear;
```

```supercollider
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
Ndef(\ptrack).clear;
```

```supercollider
(
//timbre tracking
//track how 'clean' the input sound is.  try whistle vs blow (sine vs noise)
Ndef(\ttrack, {
    var buf= LocalBuf(2048).clear;
    var fft= FFT(buf, SoundIn.ar);
    SpecCentroid.kr(buf, fft).poll;  //will post values - the lower the cleaner signal
});
)

Ndef(\ttrack).stop;
Ndef(\ttrack).clear;

(
//timbre tracking with sound
Ndef(\ttrack2, {|thresh= 1500, lag= 0.1|
    var buf= LocalBuf(2048).clear;
    var fft= FFT(buf, SoundIn.ar);
    var t= SpecCentroid.kr(buf, fft);
    SinOsc.ar(999) * (t<thresh).poll.lag(lag);  //also try replacing < with >
}).play;
)

Ndef(\ttrack2).gui;

Ndef(\ttrack2).stop;
Ndef(\ttrack2).clear;
```

```supercollider
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

Ndef(\onOff).stop;
Ndef(\onOff).clear;
```

```supercollider
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
~buffer.play;  //turn up the volume and trigger manually once in a while
//you should be able to record the recorded sound over and over

~buffer.plot;  //see last recording
~buffer.write("~/Desktop/mybuffer.wav".standardizePath); //save last recording to desktop
```

```supercollider
~buffer2= Buffer.alloc(s, 44100*3);  //make a single three seconds long buffer

//detector with recorder and playback
(
Ndef(\automaticRecorder2, {|thresh= 0.5, time= 0.2, amp= 1, rate= 1|
    var src= SoundIn.ar*amp;
    //var src= BPF.ar(SoundIn.ar*amp, 150, 1); //variant with bandpass filter
    var off= DetectSilence.ar(src, thresh, time);
    var on= 1-off;      //invert
    on.poll;
    RecordBuf.ar(src, ~buffer2, loop:0, trigger: on);
    PlayBuf.ar(1, ~buffer2, rate, loop: 1).dup;
}).play;
)

Ndef(\automaticRecorder2).gui;

Ndef(\automaticRecorder2).stop;
Ndef(\automaticRecorder2).clear;
```

```supercollider
~buffer3= Buffer.alloc(s, 44100*3);  //make a single three seconds long buffer

//detector used to fill up a buffer
//only records when there is any should present
(
Ndef(\automaticRecorder3, {|thresh= 0.09, time= 0.2, amp= 1|
    var src= SoundIn.ar*amp;
    //var src= BPF.ar(SoundIn.ar*amp, 150, 1); //variant with bandpass filter
    var off= DetectSilence.ar(src, thresh, time);
    var on= 1-off;      //invert
    on.poll;
    RecordBuf.ar(src, ~buffer3, loop:1, run: on);  //here we only record when sound detected
});
)

~buffer3.play;  //trigger multiple times

Ndef(\automaticRecorder3).gui;

Ndef(\automaticRecorder3).stop;
Ndef(\automaticRecorder3).clear;
```

```supercollider
~buffer4= Buffer.alloc(s, 44100*3);  //make a single three seconds long buffer

//same as v3 but with playback
(
Ndef(\automaticRecorder4, {|thresh= 0.09, time= 0.2, amp= 1, rate= 1|
    var src= SoundIn.ar*amp;
    //var src= BPF.ar(SoundIn.ar*amp, 150, 1); //variant with bandpass filter
    var off= DetectSilence.ar(src, thresh, time);
    var on= 1-off;      //invert
    on.poll;
    RecordBuf.ar(src, ~buffer4, loop:1, run: on);  //here we only record when sound detected
    PlayBuf.ar(1, ~buffer4, rate, loop:1).dup;
}).play;
)

Ndef(\automaticRecorder4).gui;

Ndef(\automaticRecorder4).stop;
Ndef(\automaticRecorder4).clear;
```

links
--

Eli Fieldsteel's youtube supercollider tutorials...
<https://www.youtube.com/watch?v=yRzsOOiJ_p4&list=PLPYzvS8A_rTaNDweXe6PX4CXSGq4iEWYC>
