#osx only
#make sure to install pyosc
import subprocess
from OSC import OSCClient, OSCMessage, OSCClientError
from time import sleep

cli= OSCClient()
cli.connect(('127.0.0.1', 12345))  #send address

while True:
  a= subprocess.Popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I', shell=True, stdout=subprocess.PIPE).stdout.read()
  a= a.split()
  rssi= int(float(a[1]))
  noise= int(float(a[5]))
  msg= OSCMessage()
  msg.setAddress('/wifi')
  msg.append(rssi)
  msg.append(noise)
  sleep(0.1)  #update rate
  try:
    cli.send(msg)
  except OSCClientError:
    print 'could not send to '+str(cli.client_address)
    sleep(1)
