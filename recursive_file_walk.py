#!/usr/bin/python
import usb.core
import usb.util
import fcntl
import struct
import time
import threading
import sys
import os
import hashlib

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

def delete_file(path):
    # if file exists, delete it
    if os.path.isfile(path):
        os.remove(path)
    else:    ## Show an error ##
        print("Error: %s file not found" % myfile)
##
# returns a recursive file list as an array, starting from path. Additionally
# to the full path of the file, the size and md5 checksum are provided, the
# values are comma separated. 
# Example:
# '98c662d9e5d2306c04016e53898bc8fc,36429,./playground/python/webapp/css/jquery.mobile.structure-1.1.0.min.css'
##
def get_file_list(path):
    files = []
    for dirname, dirnames, filenames in os.walk('.'):

        # print path to all filenames.
        for filename in filenames:
            fullpath = os.path.join(dirname, filename)
            checksum = hashfile(open(fullpath, 'rb'), hashlib.md5())
            filesize = str(os.path.getsize(fullpath))
            files.append( checksum + "," + filesize + "," + fullpath)

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')

    return files

def write_to_usb(path, ep_out):
    with open(path, "rb") as f:
        byte = f.read(1)
        while byte:
            try:
                length = ep_out.write(byte, timeout = 30)
                print("%d bytes written" % length)
                time.sleep(0.5)
            except usb.core.USBError:
                print("error in writer thread")
                break
            byte = f.read(1)
        f.close()
    return

def send_file(path, ep_out):
    writer_thread = threading.Thread(target = writer_to_usb, args = (path, ep_out, ))
    writer_thread.start()



print get_file_list('.')