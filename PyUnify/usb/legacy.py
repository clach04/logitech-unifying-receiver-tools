# Copyright (C) 2009-2011 Wander Lairson Costa 
# 
# The following terms apply to all files associated
# with the software unless explicitly disclaimed in individual files.
# 
# The authors hereby grant permission to use, copy, modify, distribute,
# and license this software and its documentation for any purpose, provided
# that existing copyright notices are retained in all copies and that this
# notice is included verbatim in any distributions. No written agreement,
# license, or royalty fee is required for any of the authorized uses.
# Modifications to this software may be copyrighted by their authors
# and need not follow the licensing terms described here, provided that
# the new terms are clearly indicated on the first page of each file where
# they apply.
# 
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.

import usb.core as core
import usb.util as util
import usb._interop as _interop
import usb.control as control

__author__ = 'Wander Lairson Costa'

USBError = core.USBError

CLASS_AUDIO = 1
CLASS_COMM = 2
CLASS_DATA = 10
CLASS_HID = 3
CLASS_HUB = 9
CLASS_MASS_STORAGE = 8
CLASS_PER_INTERFACE = 0
CLASS_PRINTER = 7
CLASS_VENDOR_SPEC = 255
DT_CONFIG = 2
DT_CONFIG_SIZE = 9
DT_DEVICE = 1
DT_DEVICE_SIZE = 18
DT_ENDPOINT = 5
DT_ENDPOINT_AUDIO_SIZE = 9
DT_ENDPOINT_SIZE = 7
DT_HID = 33
DT_HUB = 41
DT_HUB_NONVAR_SIZE = 7
DT_INTERFACE = 4
DT_INTERFACE_SIZE = 9
DT_PHYSICAL = 35
DT_REPORT = 34
DT_STRING = 3
ENDPOINT_ADDRESS_MASK = 15
ENDPOINT_DIR_MASK = 128
ENDPOINT_IN = 128
ENDPOINT_OUT = 0
ENDPOINT_TYPE_BULK = 2
ENDPOINT_TYPE_CONTROL = 0
ENDPOINT_TYPE_INTERRUPT = 3
ENDPOINT_TYPE_ISOCHRONOUS = 1
ENDPOINT_TYPE_MASK = 3
ERROR_BEGIN = 500000
MAXALTSETTING = 128
MAXCONFIG = 8
MAXENDPOINTS = 32
MAXINTERFACES = 32
RECIP_DEVICE = 0
RECIP_ENDPOINT = 2
RECIP_INTERFACE = 1
RECIP_OTHER = 3
REQ_CLEAR_FEATURE = 1
REQ_GET_CONFIGURATION = 8
REQ_GET_DESCRIPTOR = 6
REQ_GET_INTERFACE = 10
REQ_GET_STATUS = 0
REQ_SET_ADDRESS = 5
REQ_SET_CONFIGURATION = 9
REQ_SET_DESCRIPTOR = 7
REQ_SET_FEATURE = 3
REQ_SET_INTERFACE = 11
REQ_SYNCH_FRAME = 12
TYPE_CLASS = 32
TYPE_RESERVED = 96
TYPE_STANDARD = 0
TYPE_VENDOR = 64

class Endpoint(object):
    r"""Endpoint descriptor object."""
    def __init__(self, ep):
        self.address = ep.bEndpointAddress
        self.interval = ep.bInterval
        self.maxPacketSize = ep.wMaxPacketSize
        self.type = util.endpoint_type(ep.bmAttributes)

class Interface(object):
    r"""Interface descriptor object."""
    def __init__(self, intf):
        self.alternateSetting = intf.bAlternateSetting
        self.interfaceNumber = intf.bInterfaceNumber
        self.iInterface = intf.iInterface
        self.interfaceClass = intf.bInterfaceClass
        self.interfaceSubClass = intf.bInterfaceSubClass
        self.interfaceProtocol = intf.bInterfaceProtocol
        self.endpoints = [Endpoint(e) for e in intf]

class Configuration(object):
    r"""Configuration descriptor object."""
    def __init__(self, cfg):
        self.iConfiguration = cfg.iConfiguration
        self.maxPower = cfg.bMaxPower << 2
        self.remoteWakeup = (cfg.bmAttributes >> 5) & 1
        self.selfPowered = (cfg.bmAttributes >> 6) & 1
        self.totalLength = cfg.wTotalLength
        self.value = cfg.bConfigurationValue
        self.interfaces = [
                            list(g) for k, g in _interop._groupby(
                                    _interop._sorted(
                                        [Interface(i) for i in cfg],
                                        key=lambda i: i.interfaceNumber
                                    ),
                                    lambda i: i.alternateSetting)
                        ]

class DeviceHandle(object):
    def __init__(self, dev):
        self.dev = dev
        self.__claimed_interface = -1

    def bulkWrite(self, endpoint, buffer, timeout = 100):
        r"""Perform a bulk write request to the endpoint specified.

            Arguments:
                endpoint: endpoint number.
                buffer: sequence data buffer to write.
                        This parameter can be any sequence type.
                timeout: operation timeout in miliseconds. (default: 100)
                         Returns the number of bytes written.
        """
        return self.dev.write(endpoint, buffer, self.__claimed_interface, timeout)

    def bulkRead(self, endpoint, size, timeout = 100):
        r"""Performs a bulk read request to the endpoint specified.

            Arguments:
                endpoint: endpoint number.
                size: number of bytes to read.
                timeout: operation timeout in miliseconds. (default: 100)
            Return a tuple with the data read.
        """
        return self.dev.read(endpoint, size, self.__claimed_interface, timeout)

    def interruptWrite(self, endpoint, buffer, timeout = 100):
        r"""Perform a interrupt write request to the endpoint specified.

            Arguments:
                endpoint: endpoint number.
                buffer: sequence data buffer to write.
                        This parameter can be any sequence type.
                timeout: operation timeout in miliseconds. (default: 100)
                         Returns the number of bytes written.
        """
        return self.dev.write(endpoint, buffer, self.__claimed_interface, timeout)

    def interruptRead(self, endpoint, size, timeout = 100):
        r"""Performs a interrupt read request to the endpoint specified.

            Arguments:
                endpoint: endpoint number.
                size: number of bytes to read.
                timeout: operation timeout in miliseconds. (default: 100)
            Return a tuple with the data read.
        """
        return self.dev.read(endpoint, size, self.__claimed_interface, timeout)

    def controlMsg(self, requestType, request, buffer, value = 0, index = 0, timeout = 100):
        r"""Perform a control request to the default control pipe on a device.

        Arguments:
            requestType: specifies the direction of data flow, the type
                         of request, and the recipient.
            request: specifies the request.
            buffer: if the transfer is a write transfer, buffer is a sequence 
                    with the transfer data, otherwise, buffer is the number of
                    bytes to read.
            value: specific information to pass to the device. (default: 0)
                   index: specific information to pass to the device. (default: 0)
            timeout: operation timeout in miliseconds. (default: 100)
        Return the number of bytes written.
        """
        return self.dev.ctrl_transfer(
                    requestType,
                    request,
                    wValue = value,
                    wIndex = index,
                    data_or_wLength = buffer,
                    timeout = timeout
                )

    def clearHalt(self, endpoint):
        r"""Clears any halt status on the specified endpoint.

        Arguments:
            endpoint: endpoint number.
        """
        cfg = self.dev.get_active_configuration()
        intf = util.find_descriptor(cfg, bInterfaceNumber = self.__claimed_interface)
        e = util.find_descriptor(intf, bEndpointAddress = endpoint)
        control.clear_feature(self.dev, control.ENDPOINT_HALT, e)

    def claimInterface(self, interface):
        r"""Claims the interface with the Operating System.

        Arguments:
            interface: interface number or an Interface object.
        """
        util.claim_interface(self.dev, interface)
        self.__claimed_interface = interface

    def releaseInterface(self):
        r"""Release an interface previously claimed with claimInterface."""
        util.release_interface(self.dev, self.__claimed_interface)
        self.__claimed_interface = -1

    def reset(self):
        r"""Reset the specified device by sending a RESET
            down the port it is connected to."""
        self.dev.reset()

    def resetEndpoint(self, endpoint):
        r"""Reset all states for the specified endpoint.

        Arguments:
            endpoint: endpoint number.
        """
        self.clearHalt(endpoint)

    def setConfiguration(self, configuration):
        r"""Set the active configuration of a device.

        Arguments:
            configuration: a configuration value or a Configuration object.
        """
        self.dev.set_configuration(configuration)

    def setAltInterface(self, alternate):
        r"""Sets the active alternate setting of the current interface.

        Arguments:
            alternate: an alternate setting number or an Interface object.
        """
        self.dev.set_interface_altsetting(self.__claimed_interface, alternate)

    def getString(self, index, length, langid = None):
        r"""Retrieve the string descriptor specified by index
            and langid from a device.

        Arguments:
            index: index of descriptor in the device.
            length: number of bytes of the string
            langid: Language ID. If it is omittedi, will be
                    used the first language.
        """
        return util.get_string(self.dev, length, index, langid).encode('ascii')

    def getDescriptor(self, desc_type, desc_index, length, endpoint = -1):
        r"""Retrieves a descriptor from the device identified by the type
        and index of the descriptor.

        Arguments:
            desc_type: descriptor type.
            desc_index: index of the descriptor.
            len: descriptor length.
            endpoint: ignored.
        """
        return control.get_descriptor(self.dev, length, desc_type, desc_index)

    def detachKernelDriver(self, interface):
        r"""Detach a kernel driver from the interface (if one is attached,
            we have permission and the operation is supported by the OS)

        Arguments:
            interface: interface number or an Interface object.
        """
        self.dev.detach_kernel_driver(interface)

class Device(object):
    r"""Device descriptor object"""
    def __init__(self, dev):
        self.deviceClass = dev.bDeviceClass
        self.deviceSubClass = dev.bDeviceSubClass
        self.deviceProtocol = dev.bDeviceProtocol
        self.deviceVersion = dev.bcdDevice
        self.devnum = None
        self.filename = ''
        self.iManufacturer = dev.iManufacturer
        self.iProduct = dev.iProduct
        self.iSerialNumber = dev.iSerialNumber
        self.idProduct = dev.idProduct
        self.idVendor = dev.idVendor
        self.maxPacketSize = dev.bMaxPacketSize0
        self.usbVersion = dev.bcdUSB
        self.configurations = [Configuration(c) for c in dev]
        self.dev = dev

    def open(self):
        r"""Open the device for use.

        Return a DeviceHandle object
        """
        return DeviceHandle(self.dev)

class Bus(object):
    r"""Bus object."""
    def __init__(self):
        self.dirname = ''
        self.localtion = 0
        self.devices = [Device(d) for d in core.find(find_all=True)]

def busses():
    r"""Return a tuple with the usb busses."""
    return (Bus(),)

