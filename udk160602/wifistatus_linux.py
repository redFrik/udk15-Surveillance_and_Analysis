#linux only
#make sure to install pyosc
import subprocess
from OSC import OSCClient, OSCMessage, OSCClientError
from time import sleep

cli= OSCClient()
cli.connect(('127.0.0.1', 12345))  #send address

interface= 'wlan0'  #edit to match your network interface

while True:
  a= subprocess.Popen('cat /proc/net/wireless | grep '+interface, shell=True, stdout=subprocess.PIPE).stdout.read()
  a= a.split()  #turn string into list of words
  rssi= int(float(a[3]))
  noise= int(float(a[4]))
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
