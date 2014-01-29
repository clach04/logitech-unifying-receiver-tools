# portable Tool for pairing Logitech devices with a Unifying receiver

## Setup

Ensure PyUSB version 1.0.0 or greater is installed and available:

    pip install pyusb

## How to enable pairing mode on a Logitech Unifying (USB) receiver

 * Ensure new (target) usb unifying receiver device is plugged in.
 * Ensure old (current) usb unifying receiver device is unplugged.
 * Device (mouse, keyboard, gamepad, etc.) should be powered off.

NOTE the examples below are running as root, for example rules that
remove the need to run as root see Peter Wu's rule file
https://git.lekensteyn.nl/ltunify/tree/udev/42-logitech-unify-permissions.rules

Unix/Linux Usage:

    sudo python pairing_tool.py

Or if using pyusb that is not installed:

    sudo env PYTHONPATH=/path/to/python/usb/pyusb/trunk  python ./pairing_tool.py

Then turn on device, there is a 5 second window between running the tool
and powering on the device.

After pairing, unplug and then replugin in the usb unifying receiver.
