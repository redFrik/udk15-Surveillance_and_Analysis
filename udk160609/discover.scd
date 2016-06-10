//use together with discover.py

(
d= ();
OSCdef(\discover, {|msg|
	msg.postln;
	if(msg[0]=='/discover', {
		msg.drop(1).clump(4).do{|arr|
			d.put(arr[3].asSymbol, arr[1]);
		};
	});
}, \discover, recvPort:51000);
)
NetAddr("127.0.0.1", 50000).sendMsg(\discover);
//wait a little bit
d.postcs


//can maybe be simplified as:
//  "nmap -sn 192.168.1.0/24 -oG - | awk '/Up$/{print $2, $3}'".unixCmdGetStdOut.split(Char.nl).select{|x| x.size>0};
