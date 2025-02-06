import os
import socket
import sys
from threading import Thread
from time import sleep


def usage():
    my_program_name = os.path.basename(sys.argv[0])
    print(f"Usage: ${my_program_name} HOST PORT")
    print(f"         HOST hostname or address")
    print(f"         PORT portnumber to connect to")


def error(message, print_usage=True, exit=None):
    print(f"ERROR: ${message}")
    if print_usage:
        print()
        usage()
    if exit is not None:
        sys.exit(exit)


def recv(sock):
    while True:
        try:
            msg = sock.recv(1024)
            print(msg.decode("utf-8"))
            print("> ", end="", flush=True)
        except TimeoutError:
            continue


def main():
    if len(sys.argv) != 3:
        error("Wrong number of arguments", exit=1)

    hostname = sys.argv[1]
    port = sys.argv[2]
    try:
        port = int(port)
    except:
        error("Port must be numerical", exit=2)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    sock.settimeout(0.5)

    rx = Thread(target = recv, args = (sock,))
    rx.start()

    while True:
        try:
            data = input("> ")
        except KeyboardInterrupt:
            sock.sendall(b"quit")
            sock.close()
            exit(0)
        sock.sendall(data.encode("utf-8"))

    sock.close()


if __name__ == "__main__":
    main()
