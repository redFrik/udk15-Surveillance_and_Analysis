#make sure to install pyosc and psutil
import psutil
from OSC import OSCClient, OSCMessage, OSCClientError
from time import sleep

cli= OSCClient()
cli.connect(('127.0.0.1', 23456))  #send address

while True:
  loads= psutil.cpu_percent(percpu= True)
  #print loads  #debug
  msg= OSCMessage()
  msg.setAddress('/cpu')
  msg.append(loads)
  sleep(0.05)  #update rate
  try:
    cli.send(msg)
  except OSCClientError:
    print 'could not send to '+str(cli.client_address)
    sleep(1)

