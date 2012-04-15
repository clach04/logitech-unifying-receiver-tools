#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys
import time

# Import pyusb, source from https://github.com/walac/pyusb
# main web site http://sourceforge.net/apps/trac/pyusb/
# clone that contains version attribute
#   https://github.com/clach04/pyusb/
import usb
import usb.meta
import usb.core


assert usb.meta.version_tuple >= (1, 0, 0)


USB_VENDOR_ID_LOGITECH = 0x046d
USB_DEVICE_ID_UNIFYING_RECEIVER = 0xc52b

UNIFY_PAIR_MESSAGE = [0x10, 0xff, 0x80, 0xb2, 0x01, 0x50, 0x3c]


def start_pairing_mode(dev):
    """Enable pairing mode in Logitech Unifying reciever.
    Pair mode is enabled for 5 secs and is handled entirely by the
    hardware firmware.
    Once pairing mode is enabled turn on Logitech device to pair.
    
        dev is the pyusb device to use
    """
    # Sanity checks, should be real if statements rather than asserts..
    assert dev.idVendor == USB_VENDOR_ID_LOGITECH
    assert dev.idProduct == USB_DEVICE_ID_UNIFYING_RECEIVER
    
    # Send the first control transfer
    dev.ctrl_transfer(0x21, 0x09, 0x0210, 0x0002, UNIFY_PAIR_MESSAGE)

    # Send the receive data request
    dev.read(0x83, 0x7, 2)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    # find device logitech unifying receiver 046d:c52b
    dev = usb.core.find(idVendor=USB_VENDOR_ID_LOGITECH, idProduct=USB_DEVICE_ID_UNIFYING_RECEIVER)

    if dev is None:
        raise ValueError('Device not found')

    print 'logitech unifying receiver found'
    for attr_name in ['iManufacturer', 'iProduct', 'iSerialNumber', 'idProduct', 'idVendor']:
        tmp_val = getattr(dev, attr_name)
        print '\t', attr_name, hex(tmp_val), tmp_val

    interface = 2
    print 'taking sole access to device'
    # NOTE sometimes one of these fails and needs to be re-ran.
    # I've not yet worked out a robust way to deal with this :-(
    try:
        dev.set_configuration()
    except usb.core.USBError, info:
        pass  # assume everything is OK
    try:
        dev.detach_kernel_driver(interface)
    except usb.core.USBError, info:
        pass  # assume everything is OK
    except AttributeError, info:
        # Ignore under Windows, missing with libusb-0.1
        # NOTE no backend check below, just platform
        if self._platform != 'nt':
            raise
            
    print 'about to pair'
    start_pairing_mode(dev)
    print 'pairing stops in 5 seconds, power on device to pair'
    print '    if device already on, power off/on'
    time.sleep(5)
    print 'pairing mode ENDED'
    
    """DO NOT REATTACH! End up with
    #dev.attach_kernel_driver(interface)  # reattach 
    
Traceback (most recent call last):
  File "./logitech_find.py", line 112, in <module>
    sys.exit(main())
  File "./logitech_find.py", line 85, in main
    dev.attach_kernel_driver(interface)  # reattach
  File "/home/clach04/dev/python/pyusb_git/usb/core.py", line 728, in attach_kernel_driver
    self._ctx.get_interface(self, interface).bInterfaceNumber)
  File "/home/clach04/dev/python/pyusb_git/usb/backend/libusb10.py", line 617, in attach_kernel_driver
    _check(_lib.libusb_attach_kernel_driver(dev_handle, intf))
  File "/home/clach04/dev/python/pyusb_git/usb/backend/libusb10.py", line 403, in _check
    raise USBError(_str_error[ret], ret, _libusb_errno[ret])
usb.core.USBError: [Errno 16] Resource busy


    at this point had to unplug and re-add reciever into usb port.
    at that point the old and new device worked but this script crashed out
    """

    #print dev.is_kernel_driver_active(interface=1)  # NOTE this requires root access, no idea why
    return 0


if __name__ == "__main__":
    sys.exit(main())
