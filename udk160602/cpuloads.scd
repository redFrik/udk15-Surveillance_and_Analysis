//use this together with cpuloads.py
//this will 'sonify' cpu core loads
//try opening programs in the background
(
s.latency= 0.05;
s.waitForBoot{
	var loads;
	Ndef(\snd).clear;
	Ndef(\loads).clear;
	OSCdef(\cpu, {|msg|
		//msg.postln;  //debug
		loads= msg.copyToEnd(1);  //array of cpu (typically 4 or 8 floats)
		if(Ndef(\snd).isPlaying.not, {
			Ndef(\loads, loads);
			Ndef(\snd, {var l= Ndef(\loads).kr; LPF.ar(Splay.ar(Saw.ar(l.linexp(0, 100, 50, 5000), l/100)))}).play;
		}, {
			Ndef(\loads).source= loads;
		});
	}, \cpu, recvPort:23456);
};
)
