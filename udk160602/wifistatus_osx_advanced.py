#osx only
#make sure to install pyosc
import objc
from OSC import OSCClient, OSCMessage, OSCClientError
from time import sleep

cli= OSCClient()
cli.connect(('127.0.0.1', 12345))  #send address

objc.loadBundle('CoreWLAN', bundle_path= '/System/Library/Frameworks/CoreWLAN.framework', module_globals= globals())
print CWInterface.interfaceNames()
interface= CWInterface.interfaceWithName_('en0')  #edit to match your network interface

while True:
  rssi= int(interface.rssi());
  noise= int(interface.noise());
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
