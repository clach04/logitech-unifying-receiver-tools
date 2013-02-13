# Simple cli-pairing tool for Logitech unifying technology

Originally posted by Benjamin Tissoires to Linux kernel mailing list.

Allows adding a new device to a Logitech Unifying Receiver under Linux.

> NOTE this will remove the previous pairing the device had previously. This code does not remove a pairing or list pairsings for the receiver.

## HOW TO
To determine the parameter to pairing_tool, check with the following commands:

`ls /sys/class/hidraw/hidraw*/device/uevent`
`cat /sys/class/hidraw/hidraw*/device/uevent`

Power off the device to pair.

Then issue:
`sudo ./pairing_tool /dev/DEVICENAME_FROM_ABOVE`
For example:
`sudo ./pairing_tool /dev/hidraw2`

A prompt will come up to power on the device, at this point the receiver
is pairing mode for (not sure how many) ? seconds. Once in pairing mode
pairing_tool exits and the pairing is handled by the device/receiver
firmware.
