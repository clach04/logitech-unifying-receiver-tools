# Logitech Unifying-tools

Misc tools for dealing with **Logitech Unifying Receivers** as used for 
wireless mice and keyboards (etc.). Allows Linux to pair Logitech 
Unifying Receivers with new devices. Should work with Mac OSX and 
Windows too. Check out the 
[wiki here](https://bitbucket.org/clach04/logitech-unifying-receiver-tools/wiki/Home)
Basically pools together all the original tools and notes for 
Logitech Unifying receivers and devices.

## portable_unify_pairing_tool

Portable, pure Python script that relies only on PyUSB.

This would not exist if it where not for the original pairing_tool and PyUnify.

Also consider:

  * Linux only, but mmore advanced(/recent) [ltunify](https://lekensteyn.nl/logitech-unifying.html#ltunify)
  * the more recent Python based [Solaar](http://pwr.github.io/Solaar/) which has more requirements and
dependencies but it supports more advanced operations like viewing paired
devices and unpairing.

## pairing_tool

Linux only - command line tool written in C (so it needs some compiling).

## PyUnify

Linux only - Python script.