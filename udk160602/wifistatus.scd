//use this together with wifistatus_osx.py or wifistatus_linux.py
(
s.latency= 0.05;
s.waitForBoot{
	Ndef(\snd, {|noise= 0, signal= 50| BLowPass4.ar(ClipNoise.ar(noise)+Saw.ar(50, 0.2), signal, 0.1)!2}).play;
	OSCdef(\wifi, {|msg|
		msg.postln;  //debug
		Ndef(\snd).set(
			\signal, (msg[1]+120).midicps,
			\noise, msg[2].linexp(-99, 0, 0.01, 1)
		);
	}, \wifi, recvPort:12345);
};
)
