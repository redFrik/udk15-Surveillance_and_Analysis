#linux only
#make sure to install pyosc
#edit interface below to match your network
#need to run as sudo to get all networks
import subprocess
from OSC import OSCClient, OSCMessage, OSCClientError
from time import sleep

cli= OSCClient()
cli.connect(('192.168.1.2', 34567))  #send address

interface= 'wlan0'  #edit to match your network interface

while True:
  a= subprocess.Popen('iwlist wlan0 scanning | egrep "Address|Frequency|ESSID"', shell=True, stdout=subprocess.PIPE).stdout.read()
  a= a.splitlines()
  b= []
  for i in range(len(a)):
    if i%3==0:
      b.append(a[i+2]+a[i+1]+a[i+0])
  a= b
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
      print 'could not send to '+str(cli.client_address)
    i= i+1
  sleep(4)  #update rate
