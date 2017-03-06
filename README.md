# qdotweb

At it's core, qdotweb is a Flask wrapper for the PyVISA communication package. 

The goal is to build a system where all instrument control is done via HTTP methods. 

The requirements are fairly loose; the number of instruments is relatively small (<10), no more than a few clients need access to the instruments, and the request rates are no more than 100/second. 

## Benefits


1. Clients can write instrument control software in any language with access to HTTP. 
2. Multiple clients can access the same hardware without conflict over which client controls the resource.
3. Multiple requests can be sent asyncronously on the client side to speed up data collection. 

### What works:

Basic communication (connect, close, read, write, query) and client access using the Flask Development server on OSX.

### What needs to be done:

0. Hardware
  1. Test Raspberry Pi as possible server. Can it be setup to run a Linux distribution with: python 3.x + pyvisa (preferably using the pyvisa-py, not NI-VISA, backend)? Also needs to run a USB/Serial hub (could be some driver conflict there).
  2. Is the Raspberry Pi powerful enough to run a flask applicaiton deployed with Apache?
1. Software
  1. Blocking using file creation/process IDs to prevent multiple clients from trying to access the same VISA resource. You should only have to wait if the instrument you want to use (or GPIB interface you want to use) is blocked by a lock file.
  2. Functions to handle reading of lists from instruments (wrap those that already exist in VISA). 
3. Security. 
  4. Since these instruments are connected to thousands of dollars of equipment and irreplaceable samples, we need some decent security. Maybe some sort of username, password, session id type of system. Or maybe we only make the system accessible locally, meaning if you want to use it outside of the lab, you'll need to use a VPN client.

