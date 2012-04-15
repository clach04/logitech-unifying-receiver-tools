#import pyusb stuff
import usb.core
import usb.util
#lets us run system commands
import os
#get sleep
from time import sleep

#mount debug fs and turn off usbhid
os.system('sudo mount -t debugfs none_debugfs /sys/kernel/debug')
os.system('modprobe usbmon')
os.system('cat /sys/kernel/debug/usb/usbmon/u0')
os.system('sudo modprobe -r usbhid')

# find our device 046d:c52b, logitech unifying receiver
dev = usb.core.find(idVendor=0x046d, idProduct=0xc52b)

#if the device was not found, print so
if dev is None:
    raise ValueError('Device not found')
#if the device was found, print so
else:
	print ('logitech unifying receiver found')

#Send the first control transfer
dev.ctrl_transfer(0x21,0x09,0x0210,0x0002, [0x10,0xff,0x80,0xb2,0x01,0x50,0x3c])

#Send the receive data request
dev.read(0x83,0x7,2)

#Now you are in pairing mode!
print("in pairing mode for 5 seconds")
sleep(5)

#leave pairing mode and turn back on usbhid
os.system('sudo modprobe usbhid')
print("left pairing mode!  Test to see if your device works.")

