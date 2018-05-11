from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf
import socket
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject

class Discovery(GObject.GObject):

    __GSignals={'ampli-found':(GObject.SIGNAL_RUN_FIRST,None,(str,))}
    def __init__(self,log,*arg):
        GObject.GObject.__init__(self)
        self.logger = log
        self.service_name = "SC-LX86._http._tcp.local."

    def add_service(self, zeroconf, type, name):
        if (name == self.service_name):
            try:
                info = zeroconf.get_service_info(type, name)
                self.address =  socket.inet_ntoa(info.address)
                self.logger.debug("Service found with address "+self.address)
            except AttributeError:
                self.logger.debug ("Service: " + name + "Not have an address" + " info service " + str(info))
            except:
                self.logger.debug("Service: " + name + "Unknow error")
            else:
                self.logger.debug("Service found at : " + self.address + "zeroconf will close")
                self.emit('ampli-found')
                zeroconf.close()
                return



class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        try:
            info = zeroconf.get_service_info(type, name)
            print("Service %s added, at address: %s " % (name, socket.inet_ntoa(info.address)))
        except AttributeError:
            print ("Service: " + name + "Not have an address" + " info service " + str(info))
        except:
            print("Service: " + name + "Unknow error " +sys.exc_info()[0])



zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()