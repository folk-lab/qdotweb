""" a short module to handle the creation and checking of lockfile for qdotweb """

# need to keep track of a unique process id and some information 
# about what interface is being locked out

# for a gpib interface, all intstruments on a given interface
# should be locked out -- i think
# for a serial port, i just need to block that particular port

# seems pretty likely that I will need to create different filesystems (windows, unix)

# functions:

import time

create_pid():
    return str(int(time.time()*1000.0))

# check_pid(portid)

# lock_port(portid)

# unlock_port(portid)