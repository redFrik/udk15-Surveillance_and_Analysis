#osx only
import objc
objc.loadBundle('CoreWLAN', bundle_path= '/System/Library/Frameworks/CoreWLAN.framework', module_globals= globals())
print CWInterface.interfaceNames()
interface= CWInterface.interfaceWithName_('en0')  #edit to match your network interface
print interface.ssid()
print interface.countryCode()
print interface.transmitRate()
print interface.transmitPower()
print interface.channel()
print interface.rssi()
print interface.noise()
