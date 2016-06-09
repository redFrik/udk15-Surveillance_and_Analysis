#osx only
#make sure to install pyosc
import subprocess
from OSC import OSCClient, OSCMessage, OSCClientError
from time import sleep

cli= OSCClient()
cli.connect(('127.0.0.1', 34567))  #send address

while True:
  a= subprocess.Popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s', shell=True, stdout=subprocess.PIPE).stdout.read()
  a= a.splitlines()
  a.pop(0)  #remove first line with headers
  msg= OSCMessage()
  msg.setAddress('/num_networks')
  msg.append(len(a))  #send how many networks found
  try:
    cli.send(msg)
  except OSCClientError:
    print 'could not send to '+str(cli.client_address)
  i= 0
  for line in a:
    l= line.strip()  #optional - removes trailing whitespaces
    msg= OSCMessage()
    msg.setAddress('/networks')
    msg.append(i)  #send network index
    msg.append(l)  #send data string
    try:
      cli.send(msg)
    except OSCClientError:
      pass
    i= i+1
  sleep(1)  #update rate
