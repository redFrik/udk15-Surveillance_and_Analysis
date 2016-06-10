#script to scan network of nodes (ip and hostname)
#use together with discover.scd

#!/usr/bin/env python

import nmap
from OSC import OSCServer, OSCClient, OSCMessage, OSCClientError
from time import sleep
from threading import Thread

nm= nmap.PortScanner()

cli= OSCClient()
cli.connect(('127.0.0.1', 51000)) #send address

def oscInput(addr, tags, stuff, source):
  devices= []
  scan= nm.scan(hosts='192.168.1.0/24', arguments='-sP')['scan']
  print scan
  for ip in scan.keys():
    if len(scan[ip]['hostnames'])>0:
      name= scan[ip]['hostnames'][0]['name'] #should iterate here and not only take the first
      devices.append({'ip': ip, 'name': name})
  print devices
  msg= OSCMessage()
  msg.setAddress("/discover")
  msg.append(devices)
  try:
    cli.send(msg)
  except OSCClientError:
    print "could not send to sc"

server= OSCServer(('0.0.0.0', 50000)) #receive from everywhere
server.addDefaultHandlers() #for dealing with unmatched messages
server.addMsgHandler("/discover", oscInput)
server_thread= Thread(target= server.serve_forever)
server_thread.start()

try:
	while True:
		sleep(1)
except KeyboardInterrupt:
	print 'closing'
	server.close()
	server_thread.join()
	print 'done'
