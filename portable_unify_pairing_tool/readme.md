# portable Tool for pairing Logitech devices with a Unifying receiver

## HOW-To
Enable pairing mode on a Logitech Unifying (USB) receiver.

* Ensure new (target) usb device is plugged in.
*  Ensure old (current) usb device is unplugged.
*  Device (mouse, keyboard, gamepad, etc.) should be powered off.

Unix/Linux Usage:

    `sudo python pairing_tool.py`

Or if using pyusb that is not installed:

    `sudo env PYTHONPATH=/path/to/python/usb/pyusb/trunk  python ./pairing_tool.py`

Then turn on device, there is a 5 second window between running the tool
and powering on the device.